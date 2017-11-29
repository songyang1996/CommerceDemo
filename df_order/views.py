from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from utils.decorators import login_required
from df_user.models import PassportInfo
from df_goods.models import Goods
from df_order.models import OrderGoods, OrderInfo
from django_redis import get_redis_connection
from django.http import JsonResponse
from django.db import transaction
from datetime import datetime
# Create your views here.

# /order/place/
@login_required
def order_place(request):
    "显示地址订单页"
    goods_ids = request.POST.getlist("goods_ids")
    print(goods_ids)
    if not all(goods_ids):
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
    cart_key = "cart_%d" % user_id
    # 用户所要购买的商品信息，数目，和小计
    for temp in goods_ids:
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
        total_price += amount

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

# 创建订单时候
# 订单信息表(s_order_info)中插入信息: 1条信息
# 订单商品表(s_order_goods)中插入信息: 订单买了多少个商品，插入几条信息


# 用户点击提交订单的时候, 需要发送的数据:
# 1.收货地址 2.支付方式 3.用户所要购买的商品id

# 订单生成的过程:要成功都成功，要失败都失败
# 事务: 原子性:要么成功，要么回滚
# mysql
# 开启事务: begin;
# 事务回滚: rollback;
# 设置事务保存点: savepoint 保存点;
# 回滚到某一个保存点: rollback to 保存点。
# 事务提交: commit;

# 放在事务中
    # 1.向s_order_info添加一条记录
    # 2.遍历项s_order_goods添加记录
        # 2.1 增加商品销量，减少库存
        # 2.2 累计计算商品的总数目和总金额
    # 3. 更新s_order_info对应数据的总数目和总金额
# 4. 清除购物车对应数据
# /order/handle/
# @login_required 由于是ajax请求 无法使用此装饰器跳转

	# "addr_id": addr_id,
	# "pay_method": pay_method,
	# "goods_id": goods_id,
	# "csrfmiddlewaretoken": csrf
@transaction.atomic
def order_handle(request):
    "订单生成处理"
    # 判断用户是否存在
    if not request.session.has_key("user_id"):
        return JsonResponse({
            "res": 0,
            "errmsg": "用户未登录"
    })
    addr_id = request.POST.get("addr_id")
    pay_method = request.POST.get("pay_method")
    goods_ids = request.POST.get("goods_ids")
    print(addr_id, pay_method, goods_ids)
    # 校验数据
    if not all([addr_id, pay_method, goods_ids]):
        return JsonResponse({
            "res": 1,
            "errmsg": "数据不完整"
    })
    try:
        addr = PassportInfo.objects.get(id=addr_id)
    except Exception as e:
        return JsonResponse({
            "res": 2,
            "errmsg": "地址信息错误"
    })

    if int(pay_method) not in OrderInfo.PAY_METHODS_ENUM.values():
        return JsonResponse({
            "res": 3,
            "errmsg": "不支持的支付方式"
    })

    # 生成订单
    user_id = request.session.get("user_id")
    utime = datetime.now().strftime("%Y%m%d%H%M%S")
    order_id = utime + str(user_id)

    # 订单运费
    transit_price = 10
    # 商品总数目，总金额
    total_count = 0
    total_price = 0
    # 事务保存点
    sid = transaction.savepoint()

    conn = get_redis_connection("default")
    # goods_ids = goods_ids.split(",")
    cart_key = "cart_%d" % user_id
    print(goods_ids, cart_key)
    print("123456")
    try:
        # 向订单信息表添加记录
        print("123456")
        order = OrderInfo.objects.create(
            order_id=order_id,
            passport_id=user_id,
            addr_id=addr_id,
            total_count=total_count,
            total_price=total_price,
            transit_price=transit_price,
            pay_method=pay_method
        )
        print(type(goods_ids))

        # 遍历goods_ids
        for id in eval(goods_ids):
            # 根据商品的id获取每一个商品的信息

            goods = Goods.objects.get_goods_by_id(goods_id=int(id))
            if goods is None:
                transaction.savepoint_rollback(sid)
                return JsonResponse({
                    "res": 4,
                    "errmsg": "商品信息错误"
            })
            count = conn.hget(cart_key, id)
            print(count)
            print("*"*20)
            # 判断商品库存
            if int(count) > goods.stock:
                transaction.savepoint_rollback(sid)
                return JsonResponse({
                    "res": 5,
                    "errmsg": "库存不足"
            })
            # 向订单商品表中添加记录
            OrderGoods.objects.create(
                order_id=order_id,
                goods_id=goods.id,
                count=count,
                price=goods.price
            )
            goods.sales += int(count)
            goods.stock -= int(count)
            goods.save()
            # print("goods%d,save") %goods.id
            # 累加商品总价和总数
            total_count += int(count)
            total_price += int(count)*goods.price
        # 更新订单信息中商品的总数目和总金额
        order.total_count = total_count
        order.total_price = total_price
        order.save()
    except Exception as e:
        print (e)
        transaction.savepoint_rollback(sid)
        return JsonResponse({"res": 7, "errmsg": "订单提交失败"})
    # 清除redis数据库中的购物车信息
    print("*"*30)
    print(cart_key)
    conn.hdel(cart_key, *eval(goods_ids))
    print("+"*30)
    # 提交事务
    transaction.savepoint_commit(sid)
    return JsonResponse({"res": 6, "next_url": reverse("user:order")})
