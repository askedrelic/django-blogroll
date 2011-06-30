from common import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SERVER_HOST = "http://localhost:8000/"

## Database Setup
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = SITE_ROOT / 'db' / 'production.sqlite3'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'apps.index',
    'apps.reader',
)
