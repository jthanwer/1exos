# Generated by Django 3.0.5 on 2020-05-17 09:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Correction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=255, null=True, upload_to='')),
                ('prix', models.DecimalField(decimal_places=2, default=1, max_digits=5)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Exercice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=10)),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
                ('livre', models.CharField(blank=True, max_length=100, null=True)),
                ('num_page', models.IntegerField(blank=True, null=True)),
                ('num_exo', models.IntegerField(blank=True, null=True)),
                ('prix', models.DecimalField(decimal_places=2, default=1, max_digits=5)),
                ('date_limite', models.DateTimeField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
