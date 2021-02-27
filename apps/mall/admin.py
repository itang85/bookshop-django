from django.contrib import admin
from . import models
# Register your models here.

base_fields = ['sort', 'remark', 'create_time', 'update_time', 'deleted']

@admin.register(models.CategoryModel)
class AuthModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'description']
    list_display.extend(base_fields)
    list_per_page = 20
    admin_order_field = 'id'
