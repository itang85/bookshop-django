from django.core.files.storage import FileSystemStorage


class GoodFileStorage(FileSystemStorage):
    from django.conf import settings

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):

        super().__init__(location, base_url)

    def _save(self, name, content):
        import os, time, random
        ext = os.path.splitext(name)[1]
        fname = '{}_{}_{}'.format(os.path.splitext(name)[0], time.strftime('%Y%m%d%H%M%S'), random.randint(100000, 999999))
        name = os.path.join((fname + ext))
        return super()._save(name, content)
