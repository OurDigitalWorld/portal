"""
Django settings for Portal project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys, os
#some debug code=============
#print("__name__ =", __name__)
#print("__file__ =", __file__)
#print("os.getpid() =", os.getpid())
#print("os.getcwd() =", os.getcwd())
#print("os.curdir =", os.curdir)
#print("sys.path =", repr(sys.path))
#print("sys.modules.keys() =", repr(sys.modules.keys()))
#if 'Portal' in sys.modules:
#  print("sys.modules['Portal'].__name__ =", sys.modules['Portal'].__name__)
#  print("sys.modules['Portal'].__file__ =", sys.modules['Portal'].__file__)
#  print("os.environ['DJANGO_SETTINGS_MODULE'] =", os.environ.get('DJANGO_SETTINGS_MODULE', None))

#====end debug code ====

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y_3usk(029@kl(&iexj(yio9k$lxb+8*hm4*gxd@z*8+79+&i@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
    "E:/django/Portal/templates"
)

STATICFILES_DIRS = (
    "E:/django/Portal/static",
)

FIXTURE_DIRS = (
    'E:/django/Portal/fixtures/',
)
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #extra modules via pip
    'south',
    #local apps
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
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'Portal',
        'USER': 'postgres',
        'PASSWORD': 'HalM$10',
        'HOST': '127.0.0.1',
        'PORT': '10864',
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
SOLR_URL = 'http://localhost:8082/solr481/'
XSL_PATH = 'E:/django/static/Portal/'

SITE_ID = 1