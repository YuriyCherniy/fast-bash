import os, sys
from pathlib import Path

import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env_file = os.path.join(BASE_DIR, '.env')
environ.Env.read_env(env_file)

USER = env('USER')


sys.path.insert(0, f'/var/www/{USER}/data/www/faq-reg.ru/project_name')
sys.path.insert(1, f'/var/www/{USER}/data/.venv/lib/python3.12/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'fast_bash.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()