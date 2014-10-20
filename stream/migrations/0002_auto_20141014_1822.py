# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stream',
            name='series',
            field=models.ForeignKey(to='stream.StreamSeries', null=True),
        ),
    ]
