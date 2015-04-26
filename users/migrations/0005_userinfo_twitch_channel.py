# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20150329_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='twitch_channel',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
