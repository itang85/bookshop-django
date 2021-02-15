class CustomerError(BaseException):
    def __init__(self, errno=None, errmsg=None, **kwargs):
        self.errno = errno
        self.errmsg = errmsg
        self.kwargs = kwargs

    def __str__(self):
        return repr(self.__class__.__name__)
