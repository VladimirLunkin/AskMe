# Generated by Django 3.1.2 on 2020-11-17 00:29

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='answer',
            managers=[
                ('objects1', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='likequestion',
            managers=[
                ('objects1', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='like',
            field=models.IntegerField(default=0),
        ),
    ]
