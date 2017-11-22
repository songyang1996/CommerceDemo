from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from df_goods.models import Goods
from df_goods.enums import *
from django.core.paginator import Paginator
from django_redis import get_redis_connection

# Create your views here.

# /index/
def index(request):
    '''首页视图'''
    # 需要查出每个商品种类销量前四和新品前三的商品
    hotlist = []
    newlist = []
    # 获取到销量列表
    for temp in GOODS_TYPE.keys():
        hotlist.append(Goods.objects.get_goods_by_type(type_id=temp, limit=4, sort="hot"))

    for temp in GOODS_TYPE.keys():
        newlist.append(Goods.objects.get_goods_by_type(type_id=temp, limit=3, sort='new'))

    content = {
        'fruit_hot':hotlist[0],
        'seafood_hot':hotlist[1],
        'meat_hot':hotlist[2],
        'eggs_hot':hotlist[3],
        'vegetables_hot':hotlist[4],
        'frozen_hot':hotlist[5],
        'fruit_new':newlist[0],
        'seafood_new':newlist[1],
        'meat_new':newlist[2],
        'eggs_new':newlist[3],
        'vegetables_new':newlist[4],
        'frozen_new':newlist[5]
        }
    # fruit_hot = Goods.objects.get_goods_by_type(type_id=FRUIT, limit=4, sort='hot')
    # fruit_new = Goods.objects.get_goods_by_type(type_id=FRUIT, limit=3, sort='new')
    return render(request, "df_goods/index.html", content)


# /goods/detail/(goods_id)/
def detail(request, goods_id):
    '''商品详情页'''
    goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
    goods_new = Goods.objects.get_goods_by_type(type_id=goods.type_id, limit=2, sort="new")
    # 设置面包屑导航
    type_title = GOODS_TYPE[goods.type_id]
    if goods is None:
        # 商品不存在
        return redirect(reverse('goods:index'))
    # 每次用户访问详情页后 需要记录历史访问记录
    if request.session.has_key('islogin'):
        con = get_redis_connection('default')  # 连接redis
        # 缓存格式为
        # history_用户id: [1, 2, 3, 4, 5]
        key = 'history_%d'%request.session["user_id"]
        # 从key中移除goods_id
        con.lrem(key, 0, goods_id)
        # 添加goods_id到队首
        con.lpush(key, goods_id)
        # 截取前五个元素
        con.ltrim(key, 0, 4)
    return render(request, "df_goods/detail.html", {"good":goods, "type_title":type_title, "goods_new":goods_new, "type_id": goods.type_id})
# /goods/list/type_id/page/?sort=排序方式
def list(request, type_id, page):
    # 验证type_id
    if int(type_id) not in GOODS_TYPE.keys():
        return redirect(reverse("goods:index"))
    # 根据分类查询商品信息 并排序 如过没有获取到 默认为default
    sort = request.GET.get('sort', "default")

    goods_li = Goods.objects.get_goods_by_type(type_id=type_id, sort=sort)
    # 分页
    paginator = Paginator(goods_li, 10)
    # 获取分页总页数
    num_pages = paginator.num_pages
    # 验证传入的page参数 ~ 为空或大于总页数
    if page == '' or int(page) > num_pages:
        page = 1
    else:
        page = int(page)
    # 获取对应页的内容
    goods_li = paginator.page(page)
    # 处理页码
    # num_pages < 5: 显示所有页码
    # 当前页是前3页: 显示1-5页
    # 当前页是后3页: 显示后5页
    # 其他情况: 显示当前页的前2页，当前页，后两页
    if num_pages < 5:
        pages = range(1, num_pages+1)
    elif page <= 3:
        pages = range(1, 6)
    elif num_pages - page <= 2:
        pages = range(num_pages-4, num_pages+1)
    else:
        pages = range(page-2, page+3)
    # 获取新品推荐
    goods_new = Goods.objects.get_goods_by_type(type_id=type_id, limit=2, sort='new')
    # 面包屑导航
    type_title = GOODS_TYPE[int(type_id)]
    # 定义模板上下文
    context = {
        'goods_li': goods_li,
        'goods_new': goods_new,
        'type_id': type_id,
        'type_title': type_title,
        'sort': sort,
        'pages': pages
    }
    return render(request, "df_goods/list.html", context)
