from django.contrib import admin
from .models import UserRegister, MeyveCesitleri, ArduinoVeri


class UserRegisterAdmin(admin.ModelAdmin):
    list_display = ['username','password']


class MeyveCesitleriAdmin(admin.ModelAdmin):
    list_display = ['name','image']

class ArduinoVeriAdmin(admin.ModelAdmin):
    list_display = ['fruit','slug','date', 'adet', 'saglam_adet' , 'saglam_olmayan', 'saglam_agirlik', 'saglam_olmayan_agirlik']



admin.site.register(UserRegister,UserRegisterAdmin)
admin.site.register(MeyveCesitleri,MeyveCesitleriAdmin)
admin.site.register(ArduinoVeri,ArduinoVeriAdmin)