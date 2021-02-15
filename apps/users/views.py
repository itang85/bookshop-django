import datetime
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
from utils.utils import jwt_decode_handler, jwt_encode_handler, jwt_payload_handler, jwt_payload_handler, jwt_response_payload_handler, VisitThrottle

from apps.users.models import *
from apps.users.serializers import *


class LoginView(generics.GenericAPIView):
    serializer_class = LoginViewSerializer

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
            return token_data
        else:
            raise CustomerError(errno=1002, errmsg='密码错误')


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
