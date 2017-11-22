# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('type_id', models.SmallIntegerField(default=1, choices=[(1, '新鲜水果'), (2, '海鲜水产'), (3, '猪牛羊肉'), (4, '禽类蛋品'), (5, '新鲜蔬菜'), (6, '速冻食品')], verbose_name='商品种类')),
                ('name', models.CharField(verbose_name='商品名称', max_length=20)),
                ('desc', models.CharField(verbose_name='商品简介', max_length=128)),
                ('price', models.DecimalField(verbose_name='商品价格', decimal_places=2, max_digits=10)),
                ('unite', models.CharField(verbose_name='商品单位', max_length=20)),
                ('stock', models.IntegerField(verbose_name='商品库存', default=1)),
                ('sales', models.IntegerField(verbose_name='商品销量', default=0)),
                ('detail', tinymce.models.HTMLField(verbose_name='商品详情')),
                ('image', models.ImageField(verbose_name='商品图片', upload_to='goods')),
                ('status', models.SmallIntegerField(default=1, choices=[(0, '下线商品'), (1, '上线商品')], verbose_name='商品状态')),
            ],
            options={
                'db_table': 's_goods',
            },
        ),
        migrations.CreateModel(
            name='GoodsImage',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('image', models.ImageField(verbose_name='图片路径', upload_to='goods')),
                ('goods', models.ForeignKey(verbose_name='所属商品', to='df_goods.Goods')),
            ],
            options={
                'db_table': 's_goods_image',
            },
        ),
    ]
