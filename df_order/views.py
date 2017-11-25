from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from utils.decorators import login_required
from df_user.models import PassportInfo
from df_goods.models import Goods
from django_redis import get_redis_connection
# Create your views here.

# /order/place/
@login_required
def order_place(request):
    "显示地址订单页"
    goods_ids = request.POST.getlist("goods_id")
    print(goods_ids)
    if not all goods_ids:
        # 数据不完整则跳转回购物车页面
        return redirect(reverse("cart:show"))
    # 获取登录用户的id
    user_id = request.session.get("user_id")
    # 查询用户默认的收货地址
    passport_info = PassportInfo.objects.get_address(passport_id=user_id)

    # 商品的总数目，总金额
    total_count = 0
    total_price = 0
    goods_li =list()

    conn = get_redis_connection('default')
    cart_key = "cart_%d" %user_id
    # 用户所要购买的商品信息，数目，和小计
    for temp in goodes_ids:
        # 根据商品id获取商品信息
        goods = Goods.objects.get_goods_by_id(goods_id=temp)
        # redis服务器中获取id对应的商品的数目
        count = conn.hget(cart_key, temp)
        goods.count = count
        # 计算商品的小计
        amount = int(count)*goods.price
        goods.amount = amount
        goods_li.append(goods)
        total_count += int(count)
        total_price == amount

    # 运费 需要修改 这里全部设为10元
    transit_price = 10
    # 实际付款
    total_pay = total_price + transit_price
    # 模板上下文
    context = {
        "passport_info": passport_info,
        "goods_li": goods_li,
        "total_count": total_count,
        "total_price": total_price,
        "total_pay": total_pay,
        "goods_ids": goods_ids,
        "transit_price": transit_price
    }
    return render(request, "df_order/place_order.html", context=context)
