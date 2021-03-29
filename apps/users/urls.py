from django.urls import path
from apps.users.views import *

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='登录'),
    path('signup/', SignupView.as_view(), name='注册'),
    path('info/', UserView.as_view(), name='用户信息'),
    path('address/', ShippingAddressView.as_view(), name='地址管理'),
    path('addr/', ChooseAddressView.as_view(), name='地址选择'),

]
