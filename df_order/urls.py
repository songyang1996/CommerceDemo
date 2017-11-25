from django.conf.urls import url
from df_order import views

urlpatterns = [
    url(r"^place/$", views.order_place, name="place")  # 显示订单提交页面
]
