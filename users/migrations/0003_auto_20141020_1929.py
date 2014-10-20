# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_auto_20141020_1834'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('github_profile', models.URLField(null=True, blank=True)),
                ('subscribed_users', models.ManyToManyField(related_name=b'subscribers', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(related_name=b'data', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='userdata',
            name='subscribed_users',
        ),
        migrations.RemoveField(
            model_name='userdata',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserData',
        ),
    ]
