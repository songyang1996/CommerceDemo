from django.conf.urls import url
from df_cart import views
urlpatterns = [
    url(r"^add/$", views.cart_add, name="add"),  # 购物车增加选项
    url(r'^$', views.cart_show, name='show'),  # /cart显示购物车页面
    url(r"^count/$", views.cart_count, name='count'),  # 显示购物车总数
    url(r"^update/$", views.cart_update, name="update"),  # 更新
    url(r"^del/$", views.cart_del, name="delete")
]
