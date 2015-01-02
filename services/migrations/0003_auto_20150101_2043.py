# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_police911response_initial_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='police911response',
            name='cad_event_number',
            field=models.BigIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='police911response',
            name='initial_group',
            field=models.CharField(default=b'', max_length=75, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='police911response',
            name='initial_subgroup',
            field=models.CharField(default=b'', max_length=75, blank=True),
            preserve_default=True,
        ),
    ]
