# Generated by Django 3.0.5 on 2020-08-02 18:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('filemanager', '0002_auto_20200720_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='correction',
            name='mean_rating',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='correction',
            name='rated_by',
            field=models.ManyToManyField(related_name='rated_correcs', to=settings.AUTH_USER_MODEL),
        ),
    ]
