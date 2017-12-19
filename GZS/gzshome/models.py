from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify


class UserRegister(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(max_length=50, verbose_name='Kullanici Adi', unique=True)
    password = models.CharField(max_length=50)



class MeyveCesitleri(models.Model):
    name = models.CharField(max_length=25, verbose_name='Meyve Adi', unique=True)
    image = models.ImageField(verbose_name='Meyve Gorseli', upload_to='uploads/')


class ArduinoVeri(models.Model):
    fruit = models.ForeignKey(MeyveCesitleri)
    date = models.DateTimeField(verbose_name='ekleme tarihi', default=timezone.now)
    adet = models.IntegerField(verbose_name='Toplam Adet')
    saglam_adet = models.IntegerField(verbose_name=' Sağlam Adet')
    saglam_olmayan = models.IntegerField(verbose_name='Çürük Adet')
    saglam_agirlik  = models.DecimalField(verbose_name='Sağlam Ağırlık (kg)', max_digits=10, decimal_places=2)
    saglam_olmayan_agirlik  = models.DecimalField(verbose_name='Çürük Ağırlık (kg)', max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.date)
        super(ArduinoVeri, self).save(*args, **kwargs)
