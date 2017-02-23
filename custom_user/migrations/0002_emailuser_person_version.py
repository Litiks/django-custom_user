# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_auto_20150630_1640'),
        ('custom_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailuser',
            name='person_version',
            field=models.OneToOneField(related_name='user', null=True, blank=True, to='person.PersonVersion'),
        ),
    ]
