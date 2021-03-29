from django.urls import path
from apps.mall.views import *

app_name = 'mall'

urlpatterns = [
    path('category/', CategoryView.as_view(), name="类别"),
    path('product/', ProductView.as_view(), name="商品"),
    path('sellingProduct/', SellingProductView.as_view(), name="在售商品"),
    path('goods/', GoodsView.as_view(), name="在售商品"),
    path('rate/', RateView.as_view(), name="评分"),
    path('cart/', CartView.as_view(), name="购物车"),
    path('order/', OrderView.as_view(), name="订单"),
]
