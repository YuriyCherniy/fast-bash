from core.utils import SCRIPTS_DIR, read_script, build_script_entry

from django.http import HttpResponse, Http404
from django.views import View
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(scripts=[
            build_script_entry(path)
            for path in sorted(SCRIPTS_DIR.glob('*.yaml'))
        ])
        return context


class ServeScriptView(View):
    @staticmethod
    def _inline_common(content):
        if 'source common.sh' not in content:
            return content
        common_path = SCRIPTS_DIR / 'common.sh'
        if not common_path.is_file():
            return content
        return content.replace('source common.sh', common_path.read_text(encoding='utf-8'))

    def get(self, request, filename):
        if not filename.endswith('.sh'):
            raise Http404()

        yaml_path = SCRIPTS_DIR / (filename.removesuffix('.sh') + '.yaml')

        if yaml_path.resolve().parent != SCRIPTS_DIR.resolve():
            raise Http404()
        if not yaml_path.is_file():
            raise Http404()

        data = read_script(yaml_path)
        content = data.get('content')
        if content is None:
            raise Http404()

        return HttpResponse(
            self._inline_common(content),
            content_type='text/plain'
        )
