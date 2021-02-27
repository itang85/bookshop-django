from django.urls import path
from apps.mall.views import *

app_name = 'mall'

urlpatterns = [
    path('category/', CategoryView.as_view(), name="类别"),
    path('product/', ProductView.as_view(), name="商品"),
    path('sellingProduct/', SellingProductView.as_view(), name="在售商品"),
]
