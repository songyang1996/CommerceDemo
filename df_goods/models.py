from django.db import models
from db.base_model import BaseModel
from tinymce.models import HTMLField
from df_goods.enums import *

# Create your models here.
# 10.27 15：25第一次迁移文件生成列表时 报出NoneType object Is not callable 错误 可能是哪个模块导入错误

class GoodsManager(models.Manager):
    '''商品模型管理器类'''
    # sort='new' 按照创建时间进行排序
    # sort='hot' 按照商品销量进行排序
    # sort='price' 按照商品价格进行排序
    # sort 按照默认排序进行查询
    def get_goods_by_type(self, type_id, limit=None, sort='default'):
        '''根据商品的类型id查询商品信息'''
        if sort == 'new':
            order_by = ('-create_time',)
        elif sort == 'hot':
            order_by = ('-sales',)
        elif sort == 'price':
            order_by = ('price',)
        else:
            order_by = ('-pk',)

        # 查询数据
        goods_li = self.filter(type_id=type_id).order_by(*order_by)

        if limit:
            # 限制查询结果集
            goods_li = goods_li[:limit]

        # 返回数据
        return goods_li

    def get_goods_by_id(self, goods_id):
        '''根据商品的id查询商品信息'''
        try:
            goods = Goods.objects.get(id=goods_id)
        except Goods.DoesNotExist:
            # 商品不存在
            goods = None
        return goods


class Goods(BaseModel):
    '''商品模型类'''
    # status_choices = (
    #     (0, '下线商品'),
    #     (1, '上线商品')
    # )

    # goods_type_choices = (
    #     (1, '新鲜水果'),
    #     (2, '海鲜水产'),
    #     (3, '猪牛羊肉'),
    #     (4, '禽类蛋品'),
    #     (5, '新鲜蔬菜'),
    #     (6, '速冻食品')
    # )

    status_choices = ((k,v) for k,v in STATUS_CHOICES.items())
    goods_type_choices = ((k,v) for k,v in GOODS_TYPE.items())

    type_id = models.SmallIntegerField(default=FRUIT, choices=goods_type_choices, verbose_name='商品种类')
    name = models.CharField(max_length=20, verbose_name='商品名称')
    desc = models.CharField(max_length=128, verbose_name='商品简介')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    unite = models.CharField(max_length=20, verbose_name='商品单位')
    stock = models.IntegerField(default=1, verbose_name='商品库存')
    sales = models.IntegerField(default=0, verbose_name='商品销量')
    detail = HTMLField(verbose_name='商品详情')
    image = models.ImageField(upload_to='goods', verbose_name='商品图片')
    status = models.SmallIntegerField(default=ONLINE, choices=status_choices, verbose_name='商品状态')

    objects = GoodsManager()

    class Meta:
        db_table = 's_goods'


class ImageManager(models.Manager):
    '''商品图片模型管理器类'''
    pass


class GoodsImage(models.Model):
    '''商品图片模型类'''
    goods = models.ForeignKey('Goods', verbose_name='所属商品')
    image = models.ImageField(upload_to='goods', verbose_name='图片路径')

    objects = ImageManager()

    class Meta:
        db_table = 's_goods_image'
