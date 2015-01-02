"""
Django settings for seattlestats project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd+at&v5pz3#)fv4w!11kz&h(j&!jf!^x05s&9(9&xobb7ysj74'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'seattlestats',
        'USER': 'lindsayrgwatt',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + "/logs/debug_log",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        '': { # Empty as want to make available to all apps
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}