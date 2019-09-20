# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-09-17 21:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_auto_20190917_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressdetail',
            name='iscontribute',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='addressdetail',
            name='isdel',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='iscollect',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='isdel',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='collections',
            name='iscart',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='collections',
            name='isdel',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='collections',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='iscart',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='isdel',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='iscart',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='isdel',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='ishot',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='score',
            field=models.IntegerField(blank=True, default=100, null=True),
        ),
    ]
