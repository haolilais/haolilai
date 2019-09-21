# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-09-16 16:18
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='addressdetail',
            fields=[
                ('rid', models.AutoField(primary_key=True, serialize=False)),
                ('receivename', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.CharField(blank=True, max_length=1000, null=True)),
                ('receivetime', models.DateTimeField(blank=True, null=True)),
                ('isdel', models.SmallIntegerField(blank=True, null=True)),
                ('iscontribute', models.SmallIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'addressdetail',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('ccid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
                ('paytime', models.DateTimeField(blank=True, null=True)),
                ('unit_price', models.IntegerField(blank=True, null=True)),
                ('total_price', models.IntegerField(blank=True, null=True)),
                ('num', models.IntegerField(blank=True, null=True)),
                ('isdel', models.SmallIntegerField(blank=True, null=True)),
                ('iscollect', models.SmallIntegerField(blank=True, null=True)),
                ('arrt', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'cart',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('cid', models.AutoField(primary_key=True, serialize=False)),
                ('cname', models.CharField(max_length=60)),
                ('parentid', models.IntegerField()),
                ('compere', models.CharField(blank=True, max_length=30, null=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('orderby', models.IntegerField(blank=True, null=True)),
                ('namestyle', models.CharField(blank=True, max_length=10, null=True)),
                ('logo', models.CharField(blank=True, max_length=200, null=True)),
                ('themenum', models.IntegerField(blank=True, null=True)),
                ('replynum', models.IntegerField(blank=True, null=True)),
                ('lastpost', models.CharField(blank=True, max_length=600, null=True)),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Collections',
            fields=[
                ('coid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.DateField(blank=True, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('isdel', models.SmallIntegerField(blank=True, null=True)),
                ('iscart', models.SmallIntegerField(blank=True, null=True)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'collections',
            },
        ),
        migrations.CreateModel(
            name='Friendlink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.CharField(max_length=100)),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('logo', models.CharField(blank=True, max_length=300, null=True)),
                ('orderby', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'db_table': 'friendlink',
            },
        ),
        migrations.CreateModel(
            name='Lockip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=20)),
                ('starttime', models.DateTimeField(blank=True, null=True)),
                ('endtime', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'lockip',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('oid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('ordernumber', models.IntegerField()),
                ('money', models.IntegerField()),
                ('create_time', models.DateTimeField(blank=True, null=True)),
                ('paytime', models.DateTimeField(blank=True, null=True)),
                ('paytype', models.SmallIntegerField(blank=True, null=True)),
                ('unit_price', models.IntegerField(blank=True, null=True)),
                ('total_price', models.IntegerField(blank=True, null=True)),
                ('num', models.IntegerField(blank=True, null=True)),
                ('isdel', models.SmallIntegerField(blank=True, null=True)),
                ('iscart', models.SmallIntegerField(blank=True, null=True)),
                ('status', models.SmallIntegerField(blank=True, null=True)),
                ('mark', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=600)),
                ('content', models.TextField(blank=True, null=True)),
                ('size', models.CharField(blank=True, max_length=100, null=True)),
                ('pscore', models.IntegerField(blank=True, default=100, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('hits', models.IntegerField(blank=True, null=True)),
                ('istop', models.IntegerField(blank=True, null=True)),
                ('iscart', models.IntegerField(blank=True, null=True)),
                ('ishot', models.IntegerField(blank=True, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('isdel', models.SmallIntegerField(blank=True, null=True)),
                ('publishtime', models.DateTimeField(blank=True, null=True)),
                ('ccid', models.ForeignKey(blank=True, db_column='ccid', null=True, on_delete=django.db.models.deletion.CASCADE, to='App.Cart')),
                ('cid', models.ForeignKey(blank=True, db_column='cid', null=True, on_delete=django.db.models.deletion.CASCADE, to='App.Category')),
                ('coid', models.ForeignKey(blank=True, db_column='coid', null=True, on_delete=django.db.models.deletion.CASCADE, to='App.Collections')),
                ('oid', models.ForeignKey(blank=True, db_column='oid', null=True, on_delete=django.db.models.deletion.CASCADE, to='App.Order')),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='Siteinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sitename', models.CharField(blank=True, max_length=100, null=True)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('reference', models.CharField(blank=True, max_length=200, null=True)),
                ('isclose', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'siteinfo',
            },
        ),
        migrations.CreateModel(
            name='Userdetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('qq', models.CharField(blank=True, max_length=15, null=True)),
                ('signature', models.CharField(blank=True, max_length=200, null=True)),
                ('quesstion', models.CharField(blank=True, max_length=100, null=True)),
                ('answer', models.CharField(blank=True, max_length=200, null=True)),
                ('grade', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'userdetail',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('portrait', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.IntegerField(blank=True, null=True)),
                ('usertype', models.IntegerField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
                ('autologin', models.IntegerField(blank=True, null=True)),
                ('regtime', models.DateTimeField(blank=True, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='userdetail',
            name='uid',
            field=models.ForeignKey(blank=True, db_column='uid', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='uid',
            field=models.ForeignKey(blank=True, db_column='uid', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cart',
            name='uid',
            field=models.ForeignKey(blank=True, db_column='uid', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='addressdetail',
            name='oid',
            field=models.ForeignKey(blank=True, db_column='oid', null=True, on_delete=django.db.models.deletion.CASCADE, to='App.Order'),
        ),
        migrations.AddField(
            model_name='addressdetail',
            name='uid',
            field=models.ForeignKey(blank=True, db_column='uid', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]