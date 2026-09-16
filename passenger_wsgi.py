import os, sys

USER = os.getenv('USER')

sys.path.insert(0, f'/var/www/{USER}/data/www/tph.lzy.su/fast_bash')
sys.path.insert(1, f'/var/www/{USER}/data/.venv/lib/python3.12/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'fast_bash.settings'


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
