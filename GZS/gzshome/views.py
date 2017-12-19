from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, MeyveCesidiForm
from .models import UserRegister, MeyveCesitleri, ArduinoVeri
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login
from django.contrib.auth.decorators import login_required
import serial


arduino_data = serial.Serial('COM3', 9600)


def home(request):
    title = 'Ana Sayfa'

    return render(request, 'home.html', {'title':title})

def uygula(request):
    title = 'Uygulama Sayfası'

    return render(request, 'uygula.html', {'title':title})



def login(request):
    title = 'Giriş Sayfası'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        if not username or password :
            messages.add_message(request, messages.INFO, ("Kullanıcı adı ve Parola Boş Bırakılamaz!"))

        user = User.objects.filter(username=username).first
        if not user:
            messages.add_message(request, messages.INFO, ('Kullanıcı Bulunamadı'))

        user = authenticate(username=username,password=password)
        if (user is not None):
           if user.is_active:
               dj_login(request, user)

               return redirect('arduino')


    return render(request, 'login.html', {'title':title})



def register(request):
    title = 'Kayıt Sayfası'
    form = RegistrationForm(request.POST)
    if(request.POST.get('username') and request.POST.get('password') and request.POST.get('confirm')):
        if(request.POST.get('password') == request.POST.get('confirm')):
            user = User.objects.create_user(form)
            user.username = request.POST.get('username')
            user.password = request.POST.get('password')
            user.set_password(user.password)
            user.save()
            return redirect('login')
        else:
            print('sifre hatasi') # Hata mesajları verilecek
    else:
        print('else')
    return render(request, 'register.html', {'title':title})


@login_required
def arduino(request):
    title = 'Arduino Kullanımı'
    form = MeyveCesidiForm(request.POST)
    fruit = MeyveCesitleri.objects.all().order_by()
    if (request.POST.get('basla')):
        #mesafe = int(arduino_data.readline()) #mesafe kontrol] yapilacak ona g,re if else yaparak meyve secilecek
        mesafe = 11
        #print('mesafe')
        print(mesafe)
        if mesafe < 15:
            meyve = request.POST.get('select')
            print(meyve)
            messages.add_message(request, messages.INFO, ("Seçtiğiniz meyve "+ meyve + " uygulama bu meyve için başlamıştır!"))
            #if elif ile seçilen meyveyi arduinoya gönderme işlemini burada yapacağız
            if meyve == 'Portakal': #Portakal tanimasi icin sorguyu yapiyoruz
                led = "1"
                arduino_data.write(led.encode('utf-8'))
                #ard = int(arduino_data.readline().decode('utf-8'))
                #print(ard)
                #Lcd icin bilgiler gonderilecek


            elif meyve == 'Yeşil Elma':
                print('yesil elma led 2')
                led = '2'
                arduino_data.write(led.encode('utf-8'))
                #Lcd icin bilgiler gonderilecek

            elif meyve == 'Kırmızı Elma':
                led = '3'
                arduino_data.write(led.encode('utf-8'))
                #Lcd icin bilgiler gonderilecek
            elif meyve == 'Mandalina':
                led = '4'
                arduino_data.write(led.encode('utf-8'))
                #Lcd icin bilgiler gonderilecek

            elif meyve == 'Armut':
                led = '5' # bu kisimlar arduino kodu ile duzenlenecek
                arduino_data.write(led.encode('utf-8'))
                #Lcd icin bilgiler gonderilecek

            elif meyve == 'Muz':
                led = '6'
                arduino_data.write(led.encode('utf-8'))
                #Lcd icin bilgiler gonderilecek
            return redirect(arduino)

        else:
            messages.add_message(request, messages.INFO, ("Mesafe fazla! Mesafeyi küçülterek tekrar Başlayınız!"))
            return redirect(arduino)

    if (request.POST.get('bitir')):
        messages.add_message(request, messages.INFO, ("Uygulama bitmiştir!"))
        meyve = request.POST.get('select')
        if(meyve=='Portakal'):
            gidenVeri = 'P'
            print(gidenVeri)
            arduino_data.write(gidenVeri.encode('utf-8'))
            meyveveri = MeyveCesitleri.objects.get(name=meyve)
            meyveismi = meyveveri.name
            gelen_veri = arduino_data.readline().decode("utf-8").strip('\n').strip('\r')
            dizi = gelen_veri.split(";")
            saglam = int(dizi[0])
            saglam_olmayan = int(dizi[1])
            toplam = saglam + saglam_olmayan
            saglamkg = saglam * 0.166
            curukkg = saglam_olmayan * 0.166
            veri_kayit = ArduinoVeri(fruit=meyveveri,adet=toplam,saglam_adet=saglam, saglam_olmayan=saglam_olmayan,saglam_agirlik=saglamkg,saglam_olmayan_agirlik=curukkg)
            veri_kayit.save() #Arduinodan gelen verileri modelimize ekledik
            print(veri_kayit.slug)
            return redirect('veri_sayfasi', slug=veri_kayit.slug)

        elif(meyve == 'Yeşil Elma'):
            gidenVeri = 'Y'
            print(gidenVeri)
            arduino_data.write(gidenVeri.encode('utf-8'))
            meyveveri = MeyveCesitleri.objects.get(name=meyve)
            gelen_veri = arduino_data.readline().decode("utf-8").strip('\n').strip('\r')
            dizi = gelen_veri.split(";")
            saglam = int(dizi[0])
            saglam_olmayan = int(dizi[1])
            toplam = saglam + saglam_olmayan
            saglamkg = saglam * 0.166
            curukkg = saglam_olmayan * 0.166
            veri_kayit = ArduinoVeri(fruit=meyveveri,adet=toplam,saglam_adet=saglam, saglam_olmayan=saglam_olmayan,saglam_agirlik=saglamkg,saglam_olmayan_agirlik=curukkg)
            veri_kayit.save() #Arduinodan gelen verileri modelimize ekledik

            return redirect('veri_sayfasi', slug=veri_kayit.slug)

        elif(meyve == 'Kırmızı Elma'):
            gidenVeri = 'K'
            print(gidenVeri)
            arduino_data.write(gidenVeri.encode('utf-8'))
            meyveveri = MeyveCesitleri.objects.get(name=meyve)
            meyveismi = meyveveri.name
            gelen_veri = arduino_data.readline().decode("utf-8").strip('\n').strip('\r')
            dizi = gelen_veri.split(";")
            saglam = int(dizi[0])
            saglam_olmayan = int(dizi[1])
            toplam = saglam + saglam_olmayan
            saglamkg = saglam * 0.166
            curukkg = saglam_olmayan * 0.166
            veri_kayit = ArduinoVeri(fruit=meyveveri,adet=toplam,saglam_adet=saglam, saglam_olmayan=saglam_olmayan,saglam_agirlik=saglamkg,saglam_olmayan_agirlik=curukkg)
            veri_kayit.save() #Arduinodan gelen verileri modelimize ekledik

            return redirect('veri_sayfasi', slug=veri_kayit.slug)

        elif(meyve == 'Mandalina'):
            gidenVeri = 'M'
            print(gidenVeri)
            arduino_data.write(gidenVeri.encode('utf-8'))
            meyveveri = MeyveCesitleri.objects.get(name=meyve)
            gelen_veri = arduino_data.readline().decode("utf-8").strip('\n').strip('\r')
            dizi = gelen_veri.split(";")
            saglam = int(dizi[0])
            saglam_olmayan = int(dizi[1])
            toplam = saglam + saglam_olmayan
            saglamkg = saglam * 0.166
            curukkg = saglam_olmayan * 0.166
            veri_kayit = ArduinoVeri(fruit=meyveveri,adet=toplam,saglam_adet=saglam, saglam_olmayan=saglam_olmayan,saglam_agirlik=saglamkg,saglam_olmayan_agirlik=curukkg)
            veri_kayit.save() #Arduinodan gelen verileri modelimize ekledik

            return redirect('veri_sayfasi', slug=veri_kayit.slug)

        elif(meyve == 'Muz'):
            gidenVeri = 'U'
            print(gidenVeri)
            arduino_data.write(gidenVeri.encode('utf-8'))
            meyveveri = MeyveCesitleri.objects.get(name=meyve)
            gelen_veri = arduino_data.readline().decode("utf-8").strip('\n').strip('\r')
            dizi = gelen_veri.split(";")
            saglam = int(dizi[0])
            saglam_olmayan = int(dizi[1])
            toplam = saglam + saglam_olmayan
            saglamkg = saglam * 0.166
            curukkg = saglam_olmayan * 0.166
            veri_kayit = ArduinoVeri(fruit=meyveveri,adet=toplam,saglam_adet=saglam, saglam_olmayan=saglam_olmayan,saglam_agirlik=saglamkg,saglam_olmayan_agirlik=curukkg)
            veri_kayit.save() #Arduinodan gelen verileri modelimize ekledik

            return redirect('veri_sayfasi', slug=veri_kayit.slug)

        elif(meyve == 'Armut'):
            gidenVeri = 'R'
            print(gidenVeri)
            arduino_data.write(gidenVeri.encode('utf-8'))
            meyveveri = MeyveCesitleri.objects.get(name=meyve)
            gelen_veri = arduino_data.readline().decode("utf-8").strip('\n').strip('\r')
            dizi = gelen_veri.split(";")
            saglam = int(dizi[0])
            saglam_olmayan = int(dizi[1])
            toplam = saglam + saglam_olmayan
            saglamkg = saglam * 0.166
            curukkg = saglam_olmayan * 0.166
            veri_kayit = ArduinoVeri(fruit=meyveveri,adet=toplam,saglam_adet=saglam, saglam_olmayan=saglam_olmayan,saglam_agirlik=saglamkg,saglam_olmayan_agirlik=curukkg)
            veri_kayit.save() #Arduinodan gelen verileri modelimize ekledik

            return redirect('veri_sayfasi', slug=veri_kayit.slug)


    return render(request, 'arduinouygulama.html', {'title':title, 'form':form ,'fruit':fruit})


def veri_sayfasi(request, slug):
    instance = get_object_or_404(ArduinoVeri, slug=slug)
    fruit = instance.fruit.name
    fruit_img = instance.fruit

    #dıger verılerı htmle ekleyecegız


    return render(request, 'veri_sayfa.html' ,{'instance':instance, 'user':fruit, 'img':fruit_img})
