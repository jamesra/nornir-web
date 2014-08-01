'''
Created on Aug 1, 2014

@author: u0490822
'''

from nornir_web.volume_settings import *


VOLUME_DIR = "C:\\src\\git\\nornir-testdata\\PlatformRaw\\IDOC\\IDocBuildTest"
print("VOLUME_DIR=" + VOLUME_DIR)
VOLUME_NAME = 'IDocBuildTest'
print("VOLUME NAME= %s" % VOLUME_NAME)

STATIC_URL = '/static/'
STATIC_ROOT = 'C:/inetpub/wwwroot/volume_server/static/'
 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nornir_web_test',
        'USER': 'django_test',
        'PASSWORD': 'testpassword',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}

VOLUME_SERVER_TILE_CACHE_ENABLED = False