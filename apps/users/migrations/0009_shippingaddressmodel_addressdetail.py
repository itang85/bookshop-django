# Generated by Django 3.1.6 on 2021-02-28 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210228_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddressmodel',
            name='addressDetail',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='详细地址'),
        ),
    ]
