# Generated by Django 3.1.2 on 2021-01-12 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20210112_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tag',
            field=models.CharField(max_length=32, unique=True, verbose_name='Тег'),
        ),
    ]
