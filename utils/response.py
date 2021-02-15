from rest_framework.response import Response


def json_response(errno=None, errmsg=None, result=None, status=200, **kwargs):
    data = {
        'errno': errno or 0,
        'errmsg': errmsg or 'SUCCESS',
        'data': {
            'result': result if type(result) == list else [result]
        }
    }

    data['data'].update(kwargs)

    resp = Response(data=data, status=status)

    token = kwargs.get('token')
    if token:
        resp.set_cookie('Token', token)

    return resp
