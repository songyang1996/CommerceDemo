from django.shortcuts import render, redirect
from df_user.models import Passport, PassportInfo
from django.http import JsonResponse, HttpResponse
import re
from django.core.urlresolvers import reverse
from celery_tasks.tasks import send_active_email
from django.conf import settings
from utils.decorators import login_required
from itsdangerous import TimedJSONWebSignatureSerializer
# 导入限制请求方法的装饰器
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django_redis import get_redis_connection
from df_goods.models import Goods
# Create your views here.
# /user/register/
def register(request):
    '''显示用户注册页面'''
    return render(request, 'df_user/register.html')

@require_POST
# /register_handle
def register_handle(request):
    '''进行用户信息的注册'''
    # 1.接收数据
    username = request.POST["user_name"]
    password = request.POST["pwd"]
    email = request.POST["email"]
    # 2.进行数据的校验
    # 判断数据不能为空
    if not all([username, password, email]):
        return render(request, "df_user/register.html", {"errmsg":"参数不能为空"})
    # 判断邮箱是否合法
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, "df_user/register.html", {"errmsg":"邮箱格式不正确"})

    # 判断用户名是否存在
    passport = Passport.objects.get_account(username=username)
    if passport:
        return render(request, "df_user/register.html", {"errmsg":"用户名已存在"})
    # 3.进行业务逻辑的处理:注册
    # 向数据表中添加用户的信息
    passport = Passport.objects.save_account(username=username, password=password, email=email)
    # 生成用户激活的token
    token = passport.generate_active_token()
    # 发送激活邮件 可以使用celery send_active_email.delay(a, b, c)
    send_active_email(email, username, token)
    # 4.返回应答
    # 反向解析函数
    return redirect(reverse("user:login"))

# http://127.0.0.1:8000/user/active/%s
def register_active(request, token):
    serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 3600)
    info = serializer.loads(token)
    accountid = info['confirm']
    # 查找id为accountid的用户 并激活保存
    passport = Passport.objects.get(id=accountid)
    passport.is_activate = True
    passport.save()

    # 跳转到登陆
    return redirect(reverse('user:login'))


# check_user_exist
def check_user_exist(request):
    username = request.GET["username"]
    # print(username)
    if Passport.objects.get_account(username):
        return JsonResponse({"res":1})
    else:
        return JsonResponse({"res":0})

# /user/login/
def login(request):
    return render(request, 'df_user/login.html')

# /user/login_handle
@require_POST
def login_handle(request):
    '''登录验证'''
    username = request.POST["username"]
    password = request.POST["password"]
    remember = request.POST["remember"]
    # 验证是否为空
    if not all([username, password]):
        return JsonResponse({"res":2})
    # try:
    #     Passport.object.get(username=request.POST[user_name]) and Passport.object.get(password=request.POST[pwd])
    # 通过帐号密码查找用户
    passport = Passport.objects.get_account(username=username, password=password)
    if passport:
        next_url = request.session.get("url_path", reverse("goods:index"))  # 读取登录页面之前的路径保存地址 如果没有则跳转到首页
        jres = JsonResponse({"res":1, "next_url":next_url})
        # 判断是否记住用户名
        if remember == "true":
            jres.set_cookie("username", username, 3600*24*7)
            # 设置cookie过期时间
        else:
            jres.delete_cookie("username")
        # session记录用户的登录状态
        request.session["islogin"] = True
        request.session["username"] = username
        request.session["user_id"] = passport.id
        return jres
    else:
        return JsonResponse({"res":0})  # 登录失败

@login_required
def center_info(request):
    '''用户中心'''
    user_id = request.session["user_id"]
    address = PassportInfo.objects.get_address(passport_id=user_id)
    # print(address.name)
    con = get_redis_connection("default")
    key = "history_%d"%user_id
    history_li = con.lrange(key, 0, 4)  # 取出前五组数据
    # [b'12', b'11', b'3', b'10']  数据格式为货物编号
    goods_li = []
    for temp in history_li:
        goods = Goods.objects.get_goods_by_id(goods_id=temp)
        goods_li.append(goods)
    # print(goods_li)
    context = {
        "address": address,
        "page": "user",
        "history": goods_li,
    }
    return render(request, "df_user/user_center_info.html", context)

@login_required
def center_order(request):
    '''订单详情页视图'''
    return render(request, "df_user/user_center_order.html", {'page':'order'})

@login_required
def center_site(request):
    '''用户地址编辑视图'''
    if request.method == "GET":
        address = PassportInfo.objects.get_address(passport_id=request.session["user_id"])
        # 北京市 海淀区 东北旺西路8号中关村软件园 （李思 收） 182****7528
        # 拼接字符串 , 'addr_con':addr_con
        try:
            addr_con = "%s (%s 收) %s" %(address.addr, address.name, address.phone)
        except:
            addr_con = "无"
        return render(request, "df_user/user_center_site.html", {'page':'address', 'addr_con':addr_con})
    elif request.method == "POST":
            name = request.POST["name"]
            addr = request.POST["addr"]
            zip_code = request.POST["zip_code"]
            phone = request.POST["phone"]
            # 验证是否为空
            if not all([name, addr, zip_code, phone]):
                return HttpResponse("数据不能为空")
            address = PassportInfo.objects.save_address(passport_id=request.session["user_id"], name=name, addr=addr, zip_code=zip_code, phone=phone)
            return redirect(reverse("user:address"))




def logout(request):
    # 清空用户相关的session信息
    request.session.flush()
    # 跳转到登录页
    return redirect(reverse('user:login'))
