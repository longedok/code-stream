# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0008_remove_technology_streams'),
    ]

    operations = [
        migrations.AddField(
            model_name='technology',
            name='streams',
            field=models.ManyToManyField(related_name=b'technologies', to='stream.Stream'),
            preserve_default=True,
        ),
    ]
