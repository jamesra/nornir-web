'''
Created on Aug 1, 2014

@author: James Anderson

This file should be copied to the root nornir volume directory we will be serving images for.
 
Then specify this settings file when starting the web server using with the --settings=volume_settings
flag or setting the DJANGO_SETTINGS_MODULE environment variable.  The nornir volume root must be on 
the python path
'''

import os
from nornir_web.default_settings import *


VOLUME_DIR = os.path.basename(__file__)
print("VOLUME_DIR=" + VOLUME_DIR)
VOLUME_NAME = os.path.basename(__file__)
print("VOLUME NAME= %s" % VOLUME_NAME)

STATIC_URL = '/static/'
STATIC_ROOT = 'C:/inetpub/wwwroot/volume_server/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': VOLUME_NAME,
        'USER': 'django_test',
        'PASSWORD': 'testpassword',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}