# Generated by Django 2.2.7 on 2020-08-09 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filemanager', '0004_auto_20200802_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='correction',
            name='file',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=''),
        ),
    ]
