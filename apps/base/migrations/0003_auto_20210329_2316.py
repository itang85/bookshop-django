# Generated by Django 3.1.7 on 2021-03-29 23:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_filemodel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='filemodel',
            options={'verbose_name': '文件存储', 'verbose_name_plural': '文件存储'},
        ),
        migrations.AlterModelTable(
            name='filemodel',
            table='base_file',
        ),
    ]