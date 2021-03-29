import datetime

from drf_yasg import openapi
from drf_yasg.openapi import Parameter, IN_PATH, IN_QUERY, TYPE_INTEGER, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from utils.preprocessing import warm_hug, protect
from utils.exception import CustomerError
from utils.jwtAuth import JWTAuthentication
from utils.pagination import Pagination
# 自定义的JWT配置 公共插件
from utils.utils import jwt_decode_handler, jwt_encode_handler, jwt_payload_handler, jwt_payload_handler, \
    jwt_response_payload_handler, VisitThrottle, get_region_cn

from apps.users.models import *
from apps.users.serializers import *


class LoginView(generics.GenericAPIView):
    # serializer_class = postLoginViewSerializer

    @warm_hug()
    def post(self, request, *args, **kwargs):
        '''
        登录
        '''
        request_data = kwargs.get('data')
        username = request_data.get('username')
        password = request_data.get('password')

        obj_user = UserModel.objects.filter(Q(username=username) | Q(mobile=username) | Q(email=username)).first()
        if not obj_user:
            raise CustomerError(errno=1002, errmsg='用户不存在')

        if obj_user.password == password:
            token_data = jwt_response_payload_handler(jwt_encode_handler(payload=jwt_payload_handler(obj_user)), obj_user, request)
            obj_user.last_login = datetime.datetime.now()
            obj_user.save()
            token_data.update({'uid': obj_user.id})
            return token_data
        else:
            raise CustomerError(errno=1002, errmsg='密码错误')


class SignupView(generics.GenericAPIView):

    @warm_hug()
    def post(self, request, *args, **kwargs):
        request_data = kwargs.get('data')
        UserModel.objects.create(
            username=request_data.get('username'),
            password=request_data.get('password'),
            email=request_data.get('email'),
            nick_name=request_data.get('nick_name'),
            group=GroupModel.objects.filter(group_type='NormalUser').first(),
            auth=AuthModel.objects.filter(auth_type='NormalUser').first()
        )
        return


class UserView(generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)

    polygon_view_get_desc = '获取用户信息'
    polygon_view_get_parm = [
        Parameter(name='token', in_=IN_QUERY, description='token', type=TYPE_STRING, required=True)
    ]

    @swagger_auto_schema(operation_description=polygon_view_get_desc, manual_parameters=polygon_view_get_parm)
    @warm_hug()
    def get(self, request, *args, **kwargs):
        data = kwargs['data']['_data']
        data['region_cn'] = get_region_cn(data['region'])
        return data

    @warm_hug()
    def put(self, request, *args, **kwargs):
        request_data = kwargs.get('data')
        obj = UserModel.objects.get(id=request_data.pop('id'))
        for key in request_data:
            if request_data[key]: setattr(obj, key, request_data[key])
        obj.save()
        return


class ShippingAddressView(generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)

    @warm_hug()
    def get(self, request, *args, **kwargs):
        data = kwargs['data']['_data']
        return data

    @warm_hug()
    def post(self, request, *args, **kwargs):
        request_data = kwargs.get('data')
        receiver = request_data['_data']['receiver']
        ShippingAddressModel.objects.create(
            addressDetail=request_data.get('addressDetail'),
            areaCode=request_data.get('areaCode'),
            city=request_data.get('city'),
            country=request_data.get('country'),
            county=request_data.get('county'),
            isDefault=request_data.get('isDefault'),
            name=request_data.get('name'),
            postalCode=request_data.get('postalCode'),
            province=request_data.get('province'),
            tel=request_data.get('tel'),
            receiver=receiver,
        )

    @warm_hug()
    def put(self, request, *args, **kwargs):
        request_data = kwargs.get('data')
        receiver = request_data['_data']['receiver']
        if request_data.get('isDefault'): ShippingAddressModel.objects.filter(receiver_id=receiver.id, isDefault=True).update(isDefault=False)
        ShippingAddressModel.objects.filter(id=request_data['id']).update(
            addressDetail=request_data.get('addressDetail'),
            areaCode=request_data.get('areaCode'),
            city=request_data.get('city'),
            country=request_data.get('country'),
            county=request_data.get('county'),
            isDefault=request_data.get('isDefault'),
            name=request_data.get('name'),
            postalCode=request_data.get('postalCode'),
            province=request_data.get('province'),
            tel=request_data.get('tel'),
            receiver=receiver,
        )
        return

    @warm_hug()
    def delete(self, request, *args, **kwargs):
        request_data = kwargs.get('data')
        ShippingAddressModel.objects.delete(id=request_data.get('id'))


class ChooseAddressView(generics.GenericAPIView):

    @warm_hug()
    def post(self, request, *args, **kwargs):
        request_data = kwargs.get('data')
        id = request_data.get('id')
        obj_addr = ShippingAddressModel.objects.filter(id=id).first()
        ShippingAddressModel.objects.filter(receiver_id=obj_addr.receiver.id).update(current=False)
        obj_addr.current = True
        obj_addr.save()


# class UserOrderView(generics.GenericAPIView):
#
#     @protect()
#     def get(self, request, *args, **kwargs):
#         uid = request.GET.get('uid')
#

class UserViewSet(ModelViewSet):
    """
    修改局部数据
    create:  创建用户
    retrieve:  检索某个用户
    update:  更新用户
    destroy:  删除用户
    list:  获取用户列表
    """
    queryset = UserModel.objects.filter(group__group_type__in=['NormalUser', 'Admin']).order_by('-create_time')
    authentication_classes = (JWTAuthentication,)
    # permission_classes = [BaseAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = ReturnUserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('username', 'mobile', 'email',)
    filter_fields = ('is_freeze', 'group', 'auth', )
    ordering_fields = ('id', 'update_time', 'create_time',)
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action in ['create']:
            return AddUserSerializer
        if self.action in ['update', 'partial_update']:
            return UpdateUserSerializer
        return ReturnUserSerializer
