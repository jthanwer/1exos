# Generated by Django 2.2.7 on 2020-08-18 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filemanager', '0007_correction_is_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='correction',
            name='gain',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]
