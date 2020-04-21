# Generated by Django 3.0.5 on 2020-04-20 19:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('filemanager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercices', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='correction',
            name='enonce',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='corrections', to='filemanager.Exercice'),
        ),
        migrations.AddField(
            model_name='correction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='corrections', to=settings.AUTH_USER_MODEL),
        ),
    ]
