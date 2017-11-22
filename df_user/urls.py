from django.conf.urls import url
from df_user import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'), # 用户注册页面
    url(r"^login/$", views.login, name="login"),  # 登录
    url(r"^register_handle/$", views.register_handle, name="register_handle"),  # 注册处理页面
    url(r"^check_user_exist/$", views.check_user_exist, name="check_user_exist"),  # 验证注册的用户名是否已存在
    url(r'^active/(?P<token>.*)/$', views.register_active, name="active"),  # 用户激活视图
    url(r"^login_handle/$", views.login_handle, name="login_handle"),  # 登录验证视图
    url(r"^center/info/$", views.center_info, name="user"),  # 用户中心页
    url(r"^center/order/$", views.center_order, name="order"),
    url(r"^center/site/$", views.center_site, name="address"),
    url(r"^logout/$", views.logout, name="logout")
]
