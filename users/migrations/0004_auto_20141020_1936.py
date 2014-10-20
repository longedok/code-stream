# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20141020_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='subscribed_users',
            field=models.ManyToManyField(related_name=b'subscribers', to=b'users.UserInfo'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user',
            field=models.OneToOneField(related_name=b'info', to=settings.AUTH_USER_MODEL),
        ),
    ]
