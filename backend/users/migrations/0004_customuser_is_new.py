# Generated by Django 2.2.7 on 2020-09-20 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200808_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_new',
            field=models.BooleanField(default=False),
        ),
    ]
