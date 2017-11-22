from django.conf.urls import url
from df_goods import views

urlpatterns = [
    url(r"^index", views.index, name="index"),  # 网站首页
    url(r"^goods/detail/(?P<goods_id>\d+)/$", views.detail, name="detail"), # /goods/detail/(goods_id) 网站详情页
    url(r"^list/(?P<type_id>\d+)/(?P<page>\d+)/$", views.list, name="list"), # 列表详情
]
