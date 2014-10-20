# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0002_auto_20141014_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stream',
            name='owner',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='stream',
            name='series',
            field=models.ForeignKey(blank=True, to='stream.StreamSeries', null=True),
        ),
    ]
