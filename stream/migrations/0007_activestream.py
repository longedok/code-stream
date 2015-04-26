# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0006_auto_20150329_2056'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveStream',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stream', models.ForeignKey(to='stream.Stream')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
