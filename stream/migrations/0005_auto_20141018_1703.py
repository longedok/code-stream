# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stream', '0004_auto_20141014_1842'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='stream',
            name='end',
        ),
        migrations.AddField(
            model_name='stream',
            name='finished',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='streamseries',
            name='github_repo',
            field=models.CharField(default='none', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='streamseries',
            name='subscribers',
            field=models.ManyToManyField(related_name=b'subscribed_streams', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='technology',
            name='subscribers',
            field=models.ManyToManyField(related_name=b'subscribed_technologies', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='technology',
            name='creator',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
