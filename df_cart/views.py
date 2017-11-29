from django.shortcuts import render
from django.http import JsonResponse
from django_redis import get_redis_connection
from df_goods.models import Goods
from utils.decorators import login_required
# Create your views here.

#/cart/add
def cart_add(request):
    '''post 提交到购物车'''
    # 登录判断 ajax请求不能用装饰器 因为无法跳转
    # 传入商品id 购买个数
    goods_id = request.POST.get('goods_id')
    count = request.POST.get('goods_count')
    if not request.session.has_key('islogin'):
        # 用户未登录
        return JsonResponse({'res':0, 'errmsg':'用户未登录'})

    # 判断是否为空
    if not all([goods_id, count]):
        return JsonResponse({'res':1, 'errmsg':'数据为空'})
    # 数据是否在表内
    goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
    if not goods:
        return JsonResponse({'res':2, 'errmsg':'数据不存在'})
    # 转为整数并判断库存
    try:
        count = int(count)
    except Exception as e:
        return JsonResponse({'res':3, 'errmsg':'商品数目非法'})
    # 获取redis连接
    conn = get_redis_connection('default')
    cart_key = 'cart_%d'%request.session.get('user_id')
    res = conn.hget(cart_key, goods_id)
    # 对之前购物车的数据进行累加
    if not res:
        res = count
    else:
        res = count + int(res)
    # 判断库存
    if res > goods.stock:
        return JsonResponse({'res':4, 'errmsg':"商品库存不足"})
    # 保存到缓存中
    conn.hset(cart_key, goods_id, res)
    return JsonResponse({'res':5})

# /count/
def cart_count(request):
    '''获取用户购物车中商品的总数'''
    # 进行登录判断
    if not request.session.has_key('islogin'):
        # 用户未登录
        return JsonResponse({'res': 0})

    # 获取用户购物车中商品的总数
    conn = get_redis_connection('default')
    cart_key = 'cart_%d'%request.session.get('user_id')

    # res = conn.hgetall(cart_key)
    # # print(res)
    # # 遍历计算商品的总数
    # count = 0
    # for i in res.values():
    #     count += int(i)

    res = conn.hvals(cart_key)
    count = 0
    # 遍历每一种商品
    for temp in res:
        count += int(temp)
    return JsonResponse({'res':count})


# /cart
@login_required
def cart_show(request):
    '''购物车页面显示'''
    conn = get_redis_connection('default')
    cart_key = 'cart_%d'%request.session["user_id"]
    res_dict = conn.hgetall(cart_key)
    print(res_dict)

    # 用户购物车中商品的总数
    total_count = 0
    # 所有商品的总价
    total_price = 0
    #
    # # 用户购物车中商品的信息，商品的数目，已经小计
    goods_li = []
    for id,count in res_dict.items():
        # 根据商品id获取商品的信息
        goods = Goods.objects.get_goods_by_id(goods_id=id)
        # 动态给goods增加属性，记录商品的小计
        goods.amount = goods.price*int(count)
        # 动态给goods增加属性count, 记录商品的数目
        goods.count = count
        goods_li.append(goods)

        total_count += int(count)
        total_price += goods.amount

    # 组织模板上下文
    context = {'goods_li':goods_li, 'total_count':total_count,
               'total_price':total_price}

    return render(request, 'df_cart/cart.html', context)
    return render(request, "df_cart/cart.html")

# /cart/update/
def cart_update(request):
    '''更新购物车商品的数目'''
    # 进行登录判断
    if not request.session.has_key('islogin'):
        # 用户未登录
        return JsonResponse({'res': 0, 'errmsg': '请先登录'})

    # 接收数据
    goods_id = request.POST.get('goods_id')
    goods_count = request.POST.get('goods_count')

    # 数据校验
    if not all([goods_id, goods_count]):
        return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

    goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
    if goods is None:
        return JsonResponse({'res': 2, 'errmsg': '商品不存在'})

    try:
        count = int(goods_count)
    except Exception as e:
        return JsonResponse({'res': 3, 'errmsg': '商品数目必须为数字'})

    # 更新购物车商品的数目
    conn = get_redis_connection('default')
    cart_key = 'cart_%d'%request.session.get('user_id')

    # 判断商品的库存
    if count > goods.stock:
        return JsonResponse({'res':4, 'errmsg':'商品库存不足'})

    # 更新操作
    conn.hset(cart_key, goods_id, count)
    return JsonResponse({'res':5})

# /cart/del/
def cart_del(request):
    '''商品用户购物车记录'''
    # 进行登录判断
    if not request.session.has_key('islogin'):
        # 用户未登录
        return JsonResponse({'res': 0, 'errmsg': '请先登录'})

    # 接收数据
    goods_id = request.POST.get('goods_id')

    # 进行校验
    if not all([goods_id]):
        return JsonResponse({'res':1, 'errmsg':'数目不完整'})

    goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
    if goods is None:
        return JsonResponse({'res':2, 'errmsg':'商品不存在'})

    # 删除redis中对应的记录
    conn = get_redis_connection('default')
    cart_key = 'cart_%d'%request.session.get('user_id')

    conn.hdel(cart_key, goods_id)

    # 返回结果
    return JsonResponse({'res':3})
