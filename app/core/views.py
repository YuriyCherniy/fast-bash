import shlex

from core.utils import SCRIPTS_DIR, read_script, build_script_entry, iter_script_files

from django.conf import settings
from django.http import HttpResponse, Http404
from django.views import View
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        creds = f"{settings.BASIC_AUTH_USER}:{settings.BASIC_AUTH_PASSWORD}"
        context.update(
            scripts=[
                build_script_entry(path)
                for path in iter_script_files()
            ],
            curl_auth=f" -u {shlex.quote(creds)}",
        )
        return context


class ServeScriptView(View):
    @staticmethod
    def _inline_common(content):
        if 'source common.sh' not in content:
            return content
        common_path = SCRIPTS_DIR / 'common.sh'
        if not common_path.is_file():
            return content
        return content.replace(
            'source common.sh', common_path.read_text(encoding='utf-8')
        )

    def get(self, request, filename):
        if not filename.endswith('.sh'):
            raise Http404()

        yaml_path = None
        for ext in ('.yml', '.yaml'):
            candidate = SCRIPTS_DIR / (filename.removesuffix('.sh') + ext)
            if candidate.resolve().parent != SCRIPTS_DIR.resolve():
                raise Http404()
            if candidate.is_file():
                yaml_path = candidate
                break

        if yaml_path is None:
            raise Http404()

        data = read_script(yaml_path)
        content = data.get('content')
        if content is None:
            raise Http404()

        return HttpResponse(
            self._inline_common(content),
            content_type='text/plain'
        )
