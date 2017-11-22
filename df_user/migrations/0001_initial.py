# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('username', models.CharField(verbose_name='用户名', max_length=20)),
                ('password', models.CharField(verbose_name='密码', max_length=40)),
                ('email', models.EmailField(verbose_name='邮箱', max_length=254)),
                ('is_activate', models.BooleanField(verbose_name='激活状态', default=False)),
            ],
            options={
                'db_table': 's_user_account',
            },
        ),
        migrations.CreateModel(
            name='PassportInfo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('name', models.CharField(verbose_name='收件人', max_length=20)),
                ('addr', models.CharField(verbose_name='详细地址', max_length=40)),
                ('zip_code', models.CharField(verbose_name='邮政编码', max_length=10)),
                ('phone', models.CharField(verbose_name='手机', max_length=20)),
                ('is_default', models.BooleanField(verbose_name='是否默认', default=False)),
                ('passport', models.ForeignKey(verbose_name='所属账户', to='df_user.Passport')),
            ],
            options={
                'db_table': 's_user_address',
            },
        ),
    ]
