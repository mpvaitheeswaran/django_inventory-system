# Generated by Django 3.2.7 on 2021-11-15 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20211112_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='number',
            field=models.IntegerField(default=1),
        ),
    ]
