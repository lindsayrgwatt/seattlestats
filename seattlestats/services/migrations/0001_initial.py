# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Police911Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('general_offense_number', models.BigIntegerField(unique=True)),
                ('description', models.CharField(max_length=75)),
                ('group', models.CharField(max_length=75)),
                ('subgroup', models.CharField(max_length=75)),
                ('date', models.DateTimeField()),
                ('address', models.CharField(max_length=75)),
                ('zone_beat', models.CharField(max_length=10)),
                ('district_sector', models.CharField(max_length=10)),
                ('point', django.contrib.gis.db.models.fields.PointField(help_text=b"Represented as 'POINT(longitude, latitude)'", srid=4326)),
            ],
            options={
                'ordering': ['-date', '-general_offense_number'],
            },
            bases=(models.Model,),
        ),
    ]
