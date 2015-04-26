# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0007_activestream'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stream',
            name='technologies',
            field=models.ManyToManyField(to=b'stream.Technology', null=True, blank=True),
        ),
    ]
