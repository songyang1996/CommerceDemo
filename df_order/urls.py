from django.conf.urls import url
from df_order import views

urlpatterns = [
    url(r"^place/$", views.order_place, name="place"),  # 显示订单提交页面
    url(r"^handle/$", views.order_handle, name="handle")  # ajax提交订单接口
]
