import logging, json
from django.http import QueryDict
from django.utils.deprecation import MiddlewareMixin

# logger = logging.getLogger('django')


class CustomerMiddleware(MiddlewareMixin):
    request_data = None
    response_data = None

    def process_request(self, request):
        pass
        # body_content = request.body
        # if 'file' not in request.path:
        #     self.request_data = getattr(request, '_body', request.body).decode("utf-8") or json.dumps(dict(request.GET))

    def process_response(self, request, response):
        # if not 'admin' in request.path and \
        #         not 'swagger' in request.path and \
        #         not 'file' in request.path:
        #
        #     res = json.loads(response.content.decode("utf-8"))
        #
        #     if res.get('errno') == None:
        #         res = {
        #             'errno': 0,
        #             'errmsg': 'SUCCESS',
        #             'data': {
        #                 'result': res if type(res) == list else [res]
        #             }
        #         }
        #
        #     response.content = json.dumps(res).encode("utf-8")
        #
        #     log = "|| bookshop-log-access || " \
        #           "scheme={} || " \
        #           "path={} || " \
        #           "method={} || " \
        #           "cookies={} || " \
        #           "content_type={} || " \
        #           "charset={} || " \
        #           "server_host={} || " \
        #           "remote_addr={} || " \
        #           "request={} || " \
        #           "response={} ||".format(
        #         request.scheme,
        #         request.path,
        #         request.method,
        #         request.COOKIES,
        #         request.content_type,
        #         request.META.get('LC_CTYPE'),
        #         request.META.get('HTTP_HOST'),
        #         request.META.get('REMOTE_ADDR'),
        #         self.request_data,
        #         response.content.decode()
        #     )
        #     # logger.info(log)
        #     print(log)

        return response
