# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-13 20:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArduinoVeri',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='ekleme tarihi')),
                ('adet', models.IntegerField(verbose_name='Toplam Adet')),
                ('saglam_adet', models.IntegerField(verbose_name=' Sağlam Adet')),
                ('saglam_olmayan', models.IntegerField(verbose_name='Çürük Adet')),
                ('saglam_agirlik', models.FloatField(verbose_name='Sağlam Ağırlık (kg)')),
                ('saglam_olmayan_agirlik', models.FloatField(verbose_name='Çürük Ağırlık (kg)')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MeyveCesitleri',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True, verbose_name='Meyve Adi')),
                ('image', models.ImageField(upload_to='uploads/', verbose_name='Meyve Gorseli')),
            ],
        ),
        migrations.CreateModel(
            name='UserRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='Kullanici Adi')),
                ('password', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='arduinoveri',
            name='fruit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gzshome.MeyveCesitleri'),
        ),
    ]
