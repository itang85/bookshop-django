"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework import permissions

# 新版swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.users.views import LoginView, UserViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Django RESTfulAPI",
        default_version='v3.0',
        description="description",
        terms_of_service="",
        contact=openapi.Contact(email="itang85@163.com"),
        license=openapi.License(name="MIT License"),
    ),
    url="http://127.0.0.1:8000",
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# 使用 viewset 路由管理
router = DefaultRouter()
# 账号管理
router.register(r'user', UserViewSet, basename='账号管理')

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='Login'),

    path('users/', include('apps.users.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path(r'__debug__/', include(debug_toolbar.urls)))
