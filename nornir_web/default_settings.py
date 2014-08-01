"""
Django settings for webview project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#VOLUME_DIR = 'C:/' + os.path.join('Temp', 'Testoutput', 'IDocBuildTest')
VOLUME_DIR = BASE_DIR
print("VOLUME_DIR=" + VOLUME_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fmwj#4qz6sh+5p*n7m_pf*873xher%ntraw^sh)l0p5q9pi2v5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'nornir_web', 'volume_server', 'templates')]
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'nornir_web.volume_server',
    'nornir_djangomodel'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'nornir_web.urls'

WSGI_APPLICATION = 'nornir_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# 
# DATABASES SHOULD BE DEFINED IN THE VOLUME_SETTINGS.py file
DATABASES = "DATABASES SHOULD BE DEFINED IN THE VOLUME_SETTINGS.py file stored in the root directory of the nornir volume"
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'nornir_web',
#         'USER': 'django_test',
#         'PASSWORD': 'testpassword',
#         'HOST': 'localhost',
#         'PORT': '3306'
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'C:/inetpub/wwwroot/volume_server/static/'

VOLUME_IMPORTER_VOLUMEDIRMEDIA = ['C:\\temp\\TestOutput']
VOLUME_IMAGE_SERVER_VOLUMEDIR = VOLUME_IMPORTER_VOLUMEDIRMEDIA