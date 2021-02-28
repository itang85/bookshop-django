# Generated by Django 3.1.6 on 2021-02-18 22:20

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_shippingaddressmodel'),
        ('mall', '0005_delete_ordermodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, verbose_name='订单号')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('sort', models.IntegerField(default=1, verbose_name='排序')),
                ('remark', models.CharField(blank=True, max_length=255, null=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')),
                ('deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('order_status', models.IntegerField(choices=[(0, '已关闭'), (1, '已下单'), (2, '待发货'), (3, '已完成')], default=1, verbose_name='订单状态')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='address_order', to='users.shippingaddressmodel', verbose_name='收获地址')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='buyer_order', to='users.usermodel', verbose_name='买家')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='seller_order', to='users.usermodel', verbose_name='卖家')),
                ('selling_product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='selling_product_order', to='mall.sellingproductmodel', verbose_name='对应商品')),
            ],
            options={
                'verbose_name': '订单信息表',
                'verbose_name_plural': '订单信息表',
                'db_table': 'order_info_table',
            },
        ),
    ]