import datetime
from typing import List, Any

from drf_yasg import openapi
from drf_yasg.openapi import Parameter, IN_PATH, IN_QUERY, TYPE_INTEGER, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils.module_loading import import_string

from utils.preprocessing import warm_hug, protect
from utils.exception import CustomerError
from utils.jwtAuth import JWTAuthentication
from utils.pagination import Pagination
# 自定义的JWT配置 公共插件
from utils.utils import jwt_decode_handler, jwt_encode_handler, jwt_payload_handler, jwt_payload_handler, jwt_response_payload_handler, VisitThrottle

from apps.mall.models import *
from apps.mall.serializers import *


class ProductView(generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)

    @warm_hug()
    def get(self, request, *args, **kwargs):
        request_data = kwargs.get('data')
        get_data = import_string('get_' + request_data.get('tag') + '_data')
        data = get_data(request_data)
        return data

    @warm_hug()
    def post(self, request, *args, **kwargs):
        request_data = kwargs.get('data')
        obj_product = ProductModel.objects.create(
            name=request_data.get('name'),
            introduction=request_data.get('introduction'),
            detail=request_data.get('detail'),
            cover=request_data.get('cover'),
            price=request_data.get('price'),
            publisher=request_data.get('publisher'),
        )
        obj_product.category.set(request_data.get('category_list'))

        obj_sp = SellingProductModel.objects.create(
            selling_price=request_data['_data']['selling_price'],
            count=request_data.get('count'),
            product=obj_product,
            seller=request_data['_data']['seller']
        )

        ProductImageModel.objects.bulk_create(
            [ProductImageModel(image=img, selling_product=obj_sp) for img in request_data.get('img_list')]
        )

    @staticmethod
    def get_recommend_data(params):
        key = params.get('key')
        page = params.get('page')
        page_size = params.get('page_size')
        qset_product = ProductModel.objects.filter(
            Q(name__icontains=key) |
            Q(introduction__icontains=key) |
            Q(publisher__icontains=key)
        )
        product_list = list(qset_product)
        for i in len(product_list):
            product_list[i]['category_list'] = [c.category_list for c in qset_product[i].category.all()]
            product_list[i]['price'] = str(product_list[i]['price'])
        res = Pagination.pagination_filter(product_list, page, page_size)
        return res

    @staticmethod
    def get_new_data(params):
        key = params.get('key')
        page = params.get('page')
        page_size = params.get('page_size')
        now_time = datetime.datetime.now()
        month_ago = datetime.timedelta(days=30)
        qset_product = ProductModel.objects.order_by('-create_time').filter(
            Q(name__icontains=key) |
            Q(introduction__icontains=key) |
            Q(publisher__icontains=key),
            create_time__range=(now_time, month_ago)
        )
        product_list = list(qset_product)
        for i in len(product_list):
            product_list[i]['category_list'] = [c.category_list for c in qset_product[i].category.all()]
            product_list['price'] = str(product_list['price'])
        res = Pagination.pagination_filter(product_list, page, page_size)
        return res

    @staticmethod
    def get_price_data(params):
        pass


class CartView(generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)

    @warm_hug()
    def get(self, request, *args, **kwargs):
        request_data = kwargs.get('data')
        user = kwargs.get('user')
        obj_cart = CartModel.objects.select_related('selling_product__product').filter(buyer_id=user.id)
        res = [{
            'id': o.id,
            'count': o.count,
            'name': o.selling_product.product.name,
            'introduction': o.selling_product.product.introduction,
            'detail': o.selling_product.product.detail,
            'cover': o.selling_product.product.cover,
            'price': str(o.selling_product.product.price),
            'publisher': o.selling_product.product.publisher,
            'category_list': o.selling_product.product.category.category_list
        } for o in obj_cart]
        return res

    @warm_hug()
    def post(self, request, *args, **kwargs):
        request_data = kwargs.get('data')
        user = kwargs.get('user')
        selling_product_id = request_data.get('selling_product_id')
        seller_id = request_data.get('seller_id')
        CartModel.objects.create(
            count=request_data.get('count'),
            selling_product=SellingProductModel.objects.get(id=selling_product_id),
            seller=UserModel.objects.get(id=seller_id),
            buyer=UserModel.objects.get(id=user.id),
        )

    @warm_hug()
    def put(self, request, *args, **kwargs):
        request_data = kwargs.get('data')
        CartModel.objects.filter(id=request_data.get('cart_id')).update(count=request_data.get('count'))

    @warm_hug()
    def delete(self, request, *args, **kwargs):
        request_data = kwargs.get('data')
        CartModel.objects.filter(id=request_data.get('cart_id')).delete()


class CategoryView(generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)

    @warm_hug()
    def get(self, request, *args, **kwargs):
        obj_category = CategoryModel.objects.filter().values('id', 'category', 'description')
        res = list(obj_category)
        for r in res:
            r['defaultIndex'] = r.pop('id')
        return res


class SellingProductView(generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)

    @warm_hug()
    def get(self, request, *args, **kwargs):
        user = kwargs['data']['_data']['user']
        obj_category = SellingProductModel.objects.select_related('product').filter(seller_id=user.id)

        res = list()

        for obj in obj_category:
            res.append({
                'id': obj.id,
                'selling_price': obj.selling_price,
                'count': obj.count,
                'name': obj.product.name,
                'introduction': obj.product.introduction,
                'detail': obj.product.detail,
                'cover': obj.product.cover,
                'price': obj.product.price,
                'publisher': obj.product.publisher,
                'category_list': list(obj.product.category.all().values('id', 'category', 'description')),
            })
        return res

    @warm_hug()
    def put(self, request, *args, **kwargs):
        request_data = kwargs.get('data')
        user = request_data['_data']['user']
        name = request_data.get('name')
        introduction = request_data.get('introduction')
        detail = request_data.get('detail')
        cover = request_data.get('cover')
        price = request_data.get('price')
        publisher = request_data.get('publisher')
        category_list = request_data.get('category_list')
        img_list = request_data.get('img_list')
        count = request_data.get('count')

        obj_sp = SellingProductModel.objects.filter(id=request_data.get('id')).first()

        if not obj_sp:
            raise CustomerError(errno=1004, errmsg='商品不存在')

        if name: obj_sp.name = name
        if introduction: obj_sp.product.introduction = introduction
        if detail: obj_sp.product.detail = detail
        if cover: obj_sp.product.cover = cover
        if price:
            obj_sp.product.price = price
            obj_sp.selling_price = price
        if publisher: obj_sp.product.publisher = publisher
        if count: obj_sp.count = count

        if category_list:
            obj_sp.product.category.clear()
            obj_sp.product.category.set(category_list)

        obj_sp.save()

        return


