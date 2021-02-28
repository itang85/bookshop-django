import json

from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from apps.mall.models import *


class getProductViewSerializer(serializers.Serializer):
    _data = serializers.JSONField(required=False)
    def validate(self, attrs):
        now_user = self.context['request'].user
        attrs['_data'] = {}
        attrs['_data']['user'] = now_user
        return attrs


class postProductViewSerializer(serializers.Serializer):
    name = serializers.CharField()
    introduction = serializers.CharField()
    detail = serializers.CharField()
    cover = serializers.URLField()
    price = serializers.DecimalField(max_digits=30, decimal_places=2)
    publisher = serializers.CharField()
    category_list = serializers.JSONField()
    img_list = serializers.JSONField()
    count = serializers.IntegerField()
    _data = serializers.JSONField(required=False)

    def validate(self, attrs):
        now_user = self.context['request'].user
        attrs['_data'] = {}
        attrs['_data']['user'] = now_user
        attrs['_data']['seller'] = now_user
        attrs['_data']['selling_price'] = attrs.get('price')
        return attrs


class getCartViewSerializer(serializers.Serializer):
    _data = serializers.JSONField(required=False)

    def validate(self, attrs):
        now_user = self.context['request'].user
        attrs['_data'] = {}
        attrs['_data']['user'] = now_user
        return attrs


class postCartViewSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    selling_product_id = serializers.IntegerField()
    seller_id = serializers.IntegerField()
    _data = serializers.JSONField(required=False)

    def validate(self, attrs):
        now_user = self.context['request'].user
        attrs['_data'] = {}
        attrs['_data']['user'] = now_user
        return attrs


class putCartViewSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    count = serializers.IntegerField(required=False)


class deleteCartViewSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()


class getCategoryViewSerializer(serializers.Serializer):

    def validate(self, attrs):
        return attrs


class getSellingProductViewSerializer(serializers.Serializer):
    _data = serializers.JSONField(required=False)

    def validate(self, attrs):
        now_user = self.context['request'].user
        attrs['_data'] = {}
        attrs['_data']['user'] = now_user
        return attrs


class putSellingProductViewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=False)
    introduction = serializers.CharField(required=False)
    detail = serializers.CharField(required=False)
    cover = serializers.URLField(required=False)
    price = serializers.DecimalField(max_digits=30, decimal_places=2, required=False)
    publisher = serializers.CharField(required=False)
    category_list = serializers.JSONField(required=False)
    img_list = serializers.JSONField(required=False)
    count = serializers.IntegerField(required=False)
    _data = serializers.JSONField(required=False)

    def validate(self, attrs):
        now_user = self.context['request'].user
        attrs['_data'] = {}
        attrs['_data']['user'] = now_user
        return attrs
