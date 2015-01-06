from __future__ import absolute_import

from celery import shared_task
from services.models import Police911Response

@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param

@shared_task
def update_police_data():
    Police911Response.objects.update_data()
