# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0001_initial'),
        ('df_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('count', models.IntegerField(verbose_name='商品数量', default=1)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')),
                ('goods', models.ForeignKey(verbose_name='订单商品', to='df_goods.Goods')),
            ],
            options={
                'db_table': 's_order_goods',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('order_id', models.CharField(primary_key=True, max_length=64, verbose_name='订单编号', serialize=False)),
                ('total_count', models.IntegerField(verbose_name='商品总数', default=1)),
                ('total_price', models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品总价')),
                ('transit_price', models.DecimalField(max_digits=10, decimal_places=2, verbose_name='运费')),
                ('pay_method', models.SmallIntegerField(verbose_name='支付方式', default=1, choices=[(1, '货到付款'), (2, '微信支付'), (3, '支付宝'), (4, '银联支付')])),
                ('status', models.SmallIntegerField(verbose_name='订单状态', default=1, choices=[(1, '待支付'), (2, '待发货'), (3, '待收货'), (4, '待评价'), (5, '已完成')])),
                ('trade_id', models.CharField(max_length=100, verbose_name='支付编号', blank=True, null=True, unique=True)),
                ('addr', models.ForeignKey(verbose_name='收货地址', to='df_user.PassportInfo')),
                ('passport', models.ForeignKey(verbose_name='下单账户', to='df_user.Passport')),
            ],
            options={
                'db_table': 's_order_info',
            },
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(verbose_name='所属订单', to='df_order.OrderInfo'),
        ),
    ]
