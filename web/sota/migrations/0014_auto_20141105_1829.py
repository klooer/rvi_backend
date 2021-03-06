# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sota', '0013_auto_20141027_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retry',
            name='ret_status',
            field=models.CharField(default=b'PE', max_length=2, verbose_name=b'Retry Status', choices=[(b'PE', b'Pending'), (b'ST', b'Started'), (b'RU', b'Running'), (b'AB', b'Aborted'), (b'SU', b'Success'), (b'FA', b'Failed'), (b'WA', b'Waiting'), (b'RE', b'Rejected')]),
        ),
        migrations.AlterField(
            model_name='update',
            name='upd_status',
            field=models.CharField(default=b'PE', max_length=2, verbose_name=b'Update Status', choices=[(b'PE', b'Pending'), (b'ST', b'Started'), (b'RU', b'Running'), (b'AB', b'Aborted'), (b'SU', b'Success'), (b'FA', b'Failed'), (b'WA', b'Waiting'), (b'RE', b'Rejected')]),
        ),
    ]
