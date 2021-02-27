from django import forms
from django.views import View
from apps.base.models import FileModel

from utils.response import json_response


class FileSystemForm(forms.Form):
    file = forms.FileField(error_messages={"required": "file不能为空"})


class FileSystemView(View):

    def post(self, request, *args, **kwargs):
        print(request.POST)
        obj_form = FileSystemForm(request.POST, request.FILES)
        if obj_form.is_valid():
            request_data = obj_form.clean()
            obj_file = FileModel()
            obj_file.file = request_data.get('file')
            file = request_data.get('file')
            print(file.name)
            obj_file.save()
            res = {
                'file_path': obj_file.file_path
            }
            return json_response(res)
        else:
            return json_response(errno=1001, errmsg=obj_form.errors)
