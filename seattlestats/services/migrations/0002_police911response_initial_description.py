# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='police911response',
            name='initial_description',
            field=models.CharField(default=b'', max_length=75, blank=True),
            preserve_default=True,
        ),
    ]
