from base import *

SECRET_KEY = 'd+at&v5pz3#)fv4w!11kz&h(j&!jf!^x05s&9(9&xobb7ysj74'

DEBUG = False

TEMPLATE_DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'seattlestats',
        'USER': 'admin',
        'PASSWORD': 'iluvseattle',
        'HOST': '',
        'PORT': '',
    }
}