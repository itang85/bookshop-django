from django.contrib import admin
from . import models


base_fields = ['sort', 'remark', 'create_time', 'update_time', 'deleted']


@admin.register(models.UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'mobile', 'email', 'group', 'auth', 'last_login']
    list_display.extend(base_fields)
    list_per_page = 20
    admin_order_field = 'id'


@admin.register(models.GroupModel)
class GroupModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'group_type', 'group_type_cn', 'group_desc']
    list_display.extend(base_fields)
    list_per_page = 20
    admin_order_field = 'id'


@admin.register(models.AuthModel)
class AuthModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'auth_type', 'auth_desc', 'routers']
    list_display.extend(base_fields)
    list_per_page = 20
    admin_order_field = 'id'

