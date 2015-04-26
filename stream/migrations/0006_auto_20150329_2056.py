# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0005_auto_20141018_1703'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stream',
            old_name='name',
            new_name='title',
        ),
    ]
