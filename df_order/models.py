from django.db import models
from db.base_model import BaseModel
from df_user.models import PassportInfo
# from df_goods.models import Goods
# Create your models here.
class OrderInfoManager(models.Manager):
    "订单信息模型管理器类"
    def get_order_by_id(self, user_id):
        try:
            orders_li = self.filter(passport_id=user_id)
            return orders_li
        except Exception as e:
            print(e)

    # def save_order_info(self, passport_id, pay_method, goods_ids):
    #     goods_ids = goods_ids.split(",")
    #     order = self.create(
    #         passport_id = passport_id,
    #         pay_method = pay_method,
    #
    #     )



class OrderInfo(BaseModel):
    "订单信息模型类"

    PAY_METHOD_CHOICES = (
        (1, "货到付款"),
        (2, "微信支付"),
        (3, "支付宝"),
        (4, "银联支付")
    )

    PAY_METHODS_ENUM = {
        "CASH": 1,
        "WEIXIN": 2,
        "ALIPAY": 3,
        "UNIONPAY": 4,
    }

    ORDER_STATUS_CHOICES = (
        (1, "待支付"),
        (2, "待发货"),
        (3, "待收货"),
        (4, "待评价"),
        (5, "已完成"),
    )

    order_id = models.CharField(max_length=64, primary_key=True, verbose_name="订单编号")
    passport = models.ForeignKey("df_user.Passport", verbose_name="下单账户")
    addr = models.ForeignKey("df_user.PassportInfo", verbose_name="收货地址")
    total_count = models.IntegerField(default=1, verbose_name="商品总数")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品总价")
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="运费")
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=1, verbose_name="支付方式")
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name="订单状态")
    trade_id = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="支付编号")
    objects = OrderInfoManager()

    class Meta:
        db_table = "s_order_info"

class OrderGoodsManager(models.Manager):
    def save_order_goods(self):
        pass

    def get_order_goods_by_order_id(self, order_id):
        order_li = self.filter(order_id=order_id)
        return order_li

class OrderGoods(BaseModel):
    "订单商品模型类"
    order = models.ForeignKey("OrderInfo", verbose_name="所属订单")
    goods = models.ForeignKey("df_goods.Goods", verbose_name="订单商品")
    count = models.IntegerField(default=1, verbose_name="商品数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品价格")
    objects = OrderGoodsManager()

    class Meta:
        db_table = "s_order_goods"
