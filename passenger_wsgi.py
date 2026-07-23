import os, sys

from fast_bash.settings import USER


sys.path.insert(0, f'/var/www/{USER}/data/www/faq-reg.ru/project_name')
sys.path.insert(1, f'/var/www/{USER}/data/.venv/lib/python3.12/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'fast_bash.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()