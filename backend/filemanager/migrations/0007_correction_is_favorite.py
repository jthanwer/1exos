# Generated by Django 2.2.7 on 2020-08-18 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filemanager', '0006_auto_20200810_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='correction',
            name='is_favorite',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
