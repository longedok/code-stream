# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0003_auto_20150505_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
