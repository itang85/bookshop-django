# Generated by Django 3.1.6 on 2021-02-15 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authmodel',
            name='routers',
            field=models.TextField(blank=True, null=True, verbose_name='前端路由'),
        ),
    ]
