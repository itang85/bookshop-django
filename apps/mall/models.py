import uuid

from django.db import models
from apps.base.models import BaseModel, SoftDeleteObject
from apps.users.models import UserModel, ShippingAddressModel
from storage.astorage import GoodFileStorage


class CategoryModel(SoftDeleteObject, BaseModel):
    category = models.CharField(max_length=255, verbose_name='类别')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='描述')

    class Meta:
        db_table = 'product_category_table'
        verbose_name = '商品类别表'
        verbose_name_plural = verbose_name

    @property
    def category_list(self):
        return {
            'id': self.id,
            'category': self.category,
            'description': self.description
        }


class ProductModel(SoftDeleteObject, BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='商品名称')
    introduction = models.CharField(max_length=255, blank=True, null=True, verbose_name='简介')
    detail = models.TextField(blank=True, null=True, verbose_name='详细介绍')
    cover = models.URLField(blank=True, null=True, verbose_name='封面')
    price = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True, verbose_name='推荐价格')
    publisher = models.CharField(max_length=255, blank=True, null=True)
    category = models.ManyToManyField(
        CategoryModel,
        verbose_name='类别',
        related_name='category_product'
    )

    class Meta:
        db_table = 'product_info_table'
        verbose_name = '商品信息表'
        verbose_name_plural = verbose_name


class SellingProductModel(SoftDeleteObject, BaseModel):
    selling_price = models.DecimalField(max_digits=30, decimal_places=2, verbose_name='售价')
    count = models.IntegerField(default=1, verbose_name='数量')
    product = models.ForeignKey(
        ProductModel,
        on_delete=models.DO_NOTHING,
        verbose_name='商品',
        related_name='selling_product'
    )
    seller = models.ForeignKey(
        UserModel,
        on_delete=models.DO_NOTHING,
        verbose_name='卖家',
        related_name='seller_product'
    )

    class Meta:
        db_table = 'selling_product_table'
        verbose_name = '在售商品表'
        verbose_name_plural = verbose_name


class ProductImageModel(SoftDeleteObject, BaseModel):
    image = models.URLField(verbose_name='商品图片')
    selling_product = models.ForeignKey(
        SellingProductModel,
        on_delete=models.DO_NOTHING,
        verbose_name='在售商品',
        related_name='selling_product_image'
    )

    class Meta:
        db_table = 'product_image_table'
        verbose_name = '商品图片表'
        verbose_name_plural = verbose_name


class OrderModel(SoftDeleteObject, BaseModel):
    ORDER_STATUS_CHOICE = (
        (0, '已关闭'),
        (1, '已下单'),
        (2, '待发货'),
        (3, '已完成'),
    )
    order_id = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, verbose_name='订单号')
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICE, default=1, verbose_name='订单状态')
    count = models.IntegerField(default=1, verbose_name='数量')
    total_fee = models.DecimalField(max_digits=30, decimal_places=2, verbose_name='总价')
    selling_product = models.ForeignKey(
        SellingProductModel,
        on_delete=models.DO_NOTHING,
        verbose_name='对应商品',
        related_name='selling_product_order'
    )
    seller = models.ForeignKey(
        UserModel,
        on_delete=models.DO_NOTHING,
        verbose_name='卖家',
        related_name='seller_order'
    )
    buyer = models.ForeignKey(
        UserModel,
        on_delete=models.DO_NOTHING,
        verbose_name='买家',
        related_name='buyer_order'
    )
    address = models.ForeignKey(
        ShippingAddressModel,
        on_delete=models.DO_NOTHING,
        verbose_name='收获地址',
        related_name='address_order'
    )

    class Meta:
        db_table = 'order_info_table'
        verbose_name = '订单信息表'
        verbose_name_plural = verbose_name


class CartModel(SoftDeleteObject, BaseModel):
    count = models.IntegerField(verbose_name='数量')
    selling_product = models.ForeignKey(
        SellingProductModel,
        on_delete=models.DO_NOTHING,
        verbose_name='对应商品',
        related_name='selling_product_cart'
    )
    seller = models.ForeignKey(
        UserModel,
        on_delete=models.DO_NOTHING,
        verbose_name='卖家',
        related_name='seller_cart'
    )
    buyer = models.ForeignKey(
        UserModel,
        on_delete=models.DO_NOTHING,
        verbose_name='买家',
        related_name='buyer_cart'
    )

    class Meta:
        db_table = 'cart_table'
        verbose_name = '购物车信息表'
        verbose_name_plural = verbose_name


class RateModel(SoftDeleteObject, BaseModel):
    fraction = models.IntegerField(verbose_name='数量')
    product = models.ForeignKey(
        ProductModel,
        on_delete=models.DO_NOTHING,
        verbose_name='对应商品',
        related_name='product_rate'
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.DO_NOTHING,
        verbose_name='评分人',
        related_name='user_rate'
    )

    class Meta:
        db_table = 'rate_table'
        verbose_name = '商品评分表'
        verbose_name_plural = verbose_name
