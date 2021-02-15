import datetime
from rest_framework import generics

from django.db.models import Q

from utils.preprocessing import warm_hug, protect
from utils.exception import CustomerError
# 自定义的JWT配置 公共插件
from utils.utils import jwt_decode_handler, jwt_encode_handler, jwt_payload_handler, jwt_payload_handler, jwt_response_payload_handler

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
