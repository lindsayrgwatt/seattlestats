from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def get_env_setting(setting):
    try:
        return os.environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)

# set the default Django settings module for the 'celery' program.
# export DJANGO_SETTINGS_MODULE=seattlestats.settings.local
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{0}'.format(get_env_setting('DJANGO_SETTINGS_MODULE')))

app = Celery('seattlestats')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)