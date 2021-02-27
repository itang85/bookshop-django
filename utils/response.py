from django.http.response import JsonResponse


def json_response(result=None, errno=None, errmsg=None, status=200, **kwargs):
    data = {
        'errno': errno or 0,
        'errmsg': errmsg or 'SUCCESS',
        'data': {
            'result': result if type(result) == list else [result]
        }
    }

    data['data'].update(kwargs)

    resp = JsonResponse(data=data, status=status)

    if type(result) == dict and result.get('token'):
        resp.set_cookie('Token', result.get('token'))

    return resp
