# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stream', '0004_series_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('title', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('description', models.TextField()),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('technology', models.ForeignKey(related_name=b'materials', to='stream.Technology')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
