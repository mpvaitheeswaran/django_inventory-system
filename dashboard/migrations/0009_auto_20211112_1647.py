# Generated by Django 3.2.7 on 2021-11-12 11:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20211112_1231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='customer',
        ),
        migrations.AddField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchase',
            name='purchase_price',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='supplier_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='customer_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
