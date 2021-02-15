import base64, json, re, jwt, datetime, time, hashlib, random

from calendar import timegm
# 导入谷歌验证码相关模块
# import pyotp

# 导入使用缓存的模块
# from django.core.cache import cache
from rest_framework.throttling import BaseThrottle

from utils.settings import api_settings


def jwt_payload_handler(account):
    payload = {
        'id': account.pk,
        'exp': datetime.datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA  # 过期时间
    }
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.datetime.utcnow().utctimetuple()
        )
    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE
    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER
    return payload


def jwt_get_user_id_from_payload_handler(payload):
    return payload.get('id')


def jwt_encode_handler(payload):
    return jwt.encode(
        payload,
        api_settings.JWT_PRIVATE_KEY or api_settings.JWT_SECRET_KEY,
        api_settings.JWT_ALGORITHM
    )


def jwt_decode_handler(token):
    options = {
        'verify_exp': api_settings.JWT_VERIFY_EXPIRATION,
    }
    return jwt.decode(
        token,
        api_settings.JWT_PUBLIC_KEY or api_settings.JWT_SECRET_KEY,
        [api_settings.JWT_ALGORITHM],
        options=options,
        verify=api_settings.JWT_VERIFY,
        leeway=api_settings.JWT_LEEWAY,
        audience=api_settings.JWT_AUDIENCE,
        issuer=api_settings.JWT_ISSUER
    )


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token
    }


# 频率组件
VISIT_RECORD = {}


class VisitThrottle(BaseThrottle):
    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        remote_addr = request.META.get('HTTP_X_REAL_IP')
        # print('请求的IP：',remote_addr)
        ctime = time.time()
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr] = [ctime,]
            return True
        history = VISIT_RECORD.get(remote_addr)
        self.history = history
        while history and history[-1] < ctime - 60:
            history.pop()
        print(VISIT_RECORD)
        if len(history) < 100:  # 限制的频数 设置同一IP该接口一分钟内只能被访问100次
            history.insert(0, ctime)
            return True
        else:
            return False

    def wait(self):
        ctime = time.time()
        return 60 - (ctime-self.history[-1])
