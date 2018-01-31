# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0050_telegramchats_last_message_update'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TeleGramChats',
        ),
        migrations.AddField(
            model_name='grouplevels',
            name='sort_num',
            field=models.IntegerField(null=True, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043a\u043e\u0432\u044b\u0439 \u043d\u043e\u043c\u0435\u0440', blank=True),
        ),
    ]
