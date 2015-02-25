"""
Django settings for Portal project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys, os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'y_3usk(029@kl(&iexj(yio9k$lxb+8*hm4*gxd@z*8+79+&i@'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
    "/Users/walter/PycharmProjects/Portal/templates"
)
STATICFILES_DIRS = (
    "/Users/walter/PycharmProjects/static",
)
FIXTURE_DIRS = (
    '/Users/walter/PycharmProjects/Portal/fixtures/',
)
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    # local apps
    'ODWPortal',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Portal.urls'

WSGI_APPLICATION = 'Portal.wsgi.application'


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request"
)

# Database

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'Portal',
        'USER': 'postgres',
        'PASSWORD': 'HalM$10',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-ca'

TIME_ZONE = 'America/Toronto'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = 'http://images.ourontario.ca/static/'
GRAPHICS_URL = 'http://graphics.OurOntario.ca/'
SOLR_URL = 'http://localhost:8983/solr481/'
XSL_PATH = '/Users/walter/Documents/Python/OOPortal/xslt/'

SITE_ID = 1