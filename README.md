# Django3.x-base
这是基于Django3.x的初始化项目

依赖
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple django django-cors-headers djangorestframework mysqlclient PyJWT django-filter drf-yasg django-debug-toolbar


添加用户
models.UserModel.objects.create(sort=1, username="root", password="140039", mobile="18280433213", group_id=1, auth_id=1)
id:  1-普通用户， 2-管理员， 3-超级管理员
