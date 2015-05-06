# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0002_auto_20150504_1850'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Techonology',
            new_name='Technology',
        ),
    ]
