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

    @protect()
    def get(self, request, *args, **kwargs):
        activeName = request.GET.get('activeName')
        key = request.GET.get('key')
        page = int(request.GET.get('page'))
        page_size = int(request.GET.get('page_size'))

        if activeName == 'recommend':
            data = self.get_recommend_data(key, page, page_size)
        elif activeName == 'new':
            data = self.get_new_data(key, page, page_size)
        elif activeName == 'selling':
            data = self.get_selling_data(key, page, page_size)
        else:
            data = []
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
    def get_recommend_data(key, page, page_size):
        qset_product = SellingProductModel.objects.select_related('product', 'seller').filter(
            Q(product__name__icontains=key) |
            Q(product__introduction__icontains=key) |
            Q(product__publisher__icontains=key)
        )
        res = []
        products = Pagination.pagination_filter(qset_product, page, page_size)
        for p in products:
            res.append({
                'id': p.id,
                'pid': p.product.id,
                'seller_id': p.seller.id,
                'count': p.count,
                'selling_price': str(p.selling_price),
                'name': p.product.name,
                'introduction': p.product.introduction,
                'detail': p.product.detail,
                'cover': p.product.cover,
                'price': str(p.product.price),
                'publisher': p.product.publisher,
                'category': [c.category_list for c in p.product.category.all()],
            })

        return res

    @staticmethod
    def get_new_data(key, page, page_size):
        now_time = datetime.datetime.now()
        month_ago = now_time - datetime.timedelta(days=30)
        qset_product = SellingProductModel.objects.select_related('product', 'seller').order_by("-create_time").filter(
            # Q(name__icontains=key) |
            # Q(introduction__icontains=key) |
            # Q(publisher__icontains=key),
            create_time__range=(month_ago, now_time)
        )
        res = []
        products = Pagination.pagination_filter(qset_product, page, page_size)
        for p in products:
            res.append({
                'id': p.id,
                'pid': p.product.id,
                'seller_id': p.seller.id,
                'count': p.count,
                'selling_price': str(p.selling_price),
                'name': p.product.name,
                'introduction': p.product.introduction,
                'detail': p.product.detail,
                'cover': p.product.cover,
                'price': str(p.product.price),
                'publisher': p.product.publisher,
                'category': [c.category_list for c in p.product.category.all()],
            })

        return res

    @staticmethod
    def get_selling_data(key, page, page_size):
        return []


class GoodsView(generics.GenericAPIView):

    @protect()
    def get(self, request, *args, **kwargs):
        pid = request.GET.get('pid')
        obj_product = ProductModel.objects.filter(id=pid).first()
        obj_img = ProductImageModel.objects.filter(selling_product__product_id=pid).values('id', 'image')
        res = [{
                'id': obj_product.id,
                'name': obj_product.name,
                'introduction': obj_product.introduction,
                'detail': obj_product.detail,
                'cover': obj_product.cover,
                'price': str(obj_product.price),
                'publisher': obj_product.publisher,
                'category_list': [c.category_list for c in obj_product.category.all()],
                'image_list': list(obj_img)
            }]
        print(res)
        return res


class CartView(generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)

    @warm_hug()
    def get(self, request, *args, **kwargs):
        request_data = kwargs.get('data')
        user = request_data['_data']['user']
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
            'category_list': [c.category_list for c in o.selling_product.product.category.all()]
        } for o in obj_cart]
        return res

    @warm_hug()
    def post(self, request, *args, **kwargs):
        request_data = kwargs.get('data')
        user = request_data['_data']['user']
        selling_product_id = request_data.get('selling_product_id')
        seller_id = request_data.get('seller_id')
        obj_cart = CartModel.objects.filter(selling_product_id=selling_product_id, buyer_id=user.id).first()
        if obj_cart:
            obj_cart.count += 1
            obj_cart.save()
        else:
            CartModel.objects.create(
                count=1,
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


class RateView(generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)

    @protect()
    def get(self, request, *args, **kwargs):
        uid = int(request.GET.get('uid'))
        pid = int(request.GET.get('pid'))
        obj_rate = RateModel.objects.filter(user_id=uid, product_id=pid).first()
        if not obj_rate:
            return
        return [{
            'id': obj_rate.id,
            'fraction': obj_rate.fraction,
        }]

    @warm_hug()
    def post(self, request, *args, **kwargs):
        request_data = kwargs.get('data')
        uid = request_data.get('uid')
        pid = request_data.get('pid')
        fraction = request_data.get('fraction')
        RateModel.objects.update_or_create(
            user_id=uid,
            product_id=pid,
            defaults={
                'fraction': fraction
            }
        )


class OrderView(generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)

    @protect()
    def get(self, request, *args, **kwargs):
        uid = int(request.GET.get('uid'))
        status = int(request.GET.get('status'))
        order_status = [1,2,3,4,5] if status == 0 else [status]
        obj_order = OrderModel.objects\
            .select_related('selling_product__product', 'seller', 'buyer', 'address')\
            .filter(order_status__in=order_status).filter(Q(buyer_id=uid) | Q(seller_id=uid))
        return [{
            'order_id': o.order_id,
            'order_status': o.order_status,
            'count': o.count,
            'total_fee': o.total_fee,
            'product': {
                'id': o.selling_product.product.id,
                'name': o.selling_product.product.name,
                'introduction': o.selling_product.product.introduction,
                'detail': o.selling_product.product.detail,
                'cover': o.selling_product.product.cover,
                'price': str(o.selling_product.product.price),
                'publisher': o.selling_product.product.publisher,
                'category_list': [c.category_list for c in o.selling_product.product.category.all()],
            },
            'seller': {
                'id': o.seller.id,
                'mobile': o.seller.mobile,
                'email': o.seller.email,
                'nick_name': o.seller.nick_name,
                'region': o.seller.region,
                'avatar_url': o.seller.avatar_url,
                'gender': o.seller.gender,
            },
            'buyer': {
                'id': o.buyer.id,
                'mobile': o.buyer.mobile,
                'email': o.buyer.email,
                'nick_name': o.buyer.nick_name,
                'region': o.buyer.region,
                'avatar_url': o.buyer.avatar_url,
                'gender': o.buyer.gender,
            },
            'address': {
                'name': o.address.name,
                'tel': o.address.tel,
                'areaCode': o.address.areaCode,
                'country': o.address.country,
                'province': o.address.province,
                'city': o.address.city,
                'county': o.address.county,
                'addressDetail': o.address.addressDetail,
                'isDefault': o.address.isDefault,
                'postalCode': o.address.postalCode,
            }
        } for o in obj_order]

    @warm_hug()
    def post(self, request, *args, **kwargs):
        request_data = kwargs.get('data')
        order_id = request_data.get('order_id')
        sid = request_data.get('sid')
        seller_id = request_data.get('seller_id')
        order_status = request_data.get('order_status')
        count = request_data.get('count')
        total_fee = request_data.get('total_fee')
        buyer_id = request_data.get('buyer_id')
        address_id = request_data.get('address_id')
        if not address_id and address_id != 0:
            address = ShippingAddressModel.objects.get(receiver=buyer_id, current=True)
        else:
            address = ShippingAddressModel.objects.get(id=address_id)
        if not order_id:
            OrderModel.objects.create(
                order_status=order_status,
                count=count,
                total_fee=total_fee,
                selling_product=SellingProductModel.objects.get(id=sid),
                seller=UserModel.objects.get(id=seller_id),
                buyer=UserModel.objects.get(id=buyer_id),
                address=address,
            )
        else:
            request_data.pop('order_id')
            obj_order = OrderModel.objects.filter(order_id=order_id).first()
            for key in request_data:
                if request_data.get(key) or request_data.get(key) == 0:
                    setattr(obj_order, key, request_data[key])
            obj_order.save()
