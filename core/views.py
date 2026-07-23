from pathlib import Path

import yaml
from django.http import HttpResponse, Http404
from django.views import View
from django.views.generic import TemplateView

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / 'scripts'


def load_yaml_script(yaml_path: Path) -> dict:
    """Читает и валидирует YAML-файл скрипта.

    Бросает ValueError, если файл повреждён, имеет некорректную
    структуру или не содержит обязательное поле 'content'.
    """
    try:
        with open(yaml_path, encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML in '{yaml_path.name}': {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(
            f"'{yaml_path.name}' must contain a YAML mapping at the top level"
        )

    if not data.get('content'):
        raise ValueError(f"'{yaml_path.name}' is missing required 'content' field")

    return data


def normalize_tags(tags) -> list:
    """Приводит поле tags к списку строк независимо от того,
    как оно было записано в YAML (строка, список, число и т.д.)."""
    if not tags:
        return []
    if isinstance(tags, (list, tuple)):
        return [str(tag) for tag in tags]
    return [str(tags)]


class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        scripts = []
        for yaml_path in sorted(SCRIPTS_DIR.glob('*.yaml')):
            try:
                data = load_yaml_script(yaml_path)
            except ValueError as exc:
                # Один битый файл не должен ронять всю страницу.
                continue

            scripts.append({
                'name': yaml_path.stem + '.sh',
                'title': data.get('title') or yaml_path.stem,
                'description': data.get('description', ''),
                'author': data.get('author', ''),
                'version': str(data.get('version', '')),
                'tags': normalize_tags(data.get('tags')),
                'args': data.get('args', '')
            })

        context['scripts'] = scripts
        return context


class ServeScriptView(View):
    def get(self, request, filename):
        if (
            not filename.endswith('.sh')
            or '..' in filename
            or '/' in filename
            or '\\' in filename
        ):
            raise Http404()

        yaml_name = filename.removesuffix('.sh') + '.yaml'
        yaml_path = SCRIPTS_DIR / yaml_name

        # Защита от path traversal: даже если имя как-то обошло
        # проверки выше, итоговый путь обязан оставаться внутри SCRIPTS_DIR.
        if yaml_path.resolve().parent != SCRIPTS_DIR.resolve():
            raise Http404()

        if not yaml_path.is_file():
            raise Http404()

        try:
            data = load_yaml_script(yaml_path)
        except ValueError as exc:
            raise Http404()

        content = data['content']

        if 'source common.sh' in content:
            common_path = SCRIPTS_DIR / 'common.sh'
            if common_path.is_file():
                content = content.replace(
                    'source common.sh',
                    common_path.read_text(encoding='utf-8'),
                )

        return HttpResponse(content, content_type='text/plain')
