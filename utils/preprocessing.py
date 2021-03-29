import functools
from django.utils.module_loading import import_string

from utils.exception import CustomerError
from utils.response import json_response


# 请求预处理
def warm_hug():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, request, *args, **kwargs):
            # try:
            if not self.serializer_class:
                serializer_string = 'apps.' + request.resolver_match.app_name + '.serializers.' + func.__name__ + self.__class__.__name__ + 'Serializer'
                self.serializer_class = import_string(serializer_string)
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return json_response(errno=1001, errmsg=str(serializer.errors))

            data = serializer.data

            res = func(self, request, *args, data=data, **kwargs)

            return json_response(result=res)
            # except CustomerError as e:
            #     return json_response(errno=e.errno, errmsg=e.errmsg, **e.kwargs)
            # except Exception as e:
            #     return json_response(errno=-1, errmsg=str(e))
        return wrapper
    return decorator


# 静态方法预处理
def protect(errno=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
                return json_response(result=res)
            except CustomerError as e:
                return json_response(errno=e.errno, errmsg=e.errmsg, **e.kwargs)
            except Exception as e:
                return json_response(errno=-1, errmsg=str(e))
        return wrapper
    return decorator
