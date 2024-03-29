# Generated by Django 3.1.6 on 2021-02-18 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0006_ordermodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorymodel',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='category_book', to='mall.categorymodel', verbose_name='类别'),
        ),
    ]
