from django.forms import ModelForm
from django import forms
from .models import UserRegister, ArduinoVeri, MeyveCesitleri



class RegistrationForm(ModelForm):
    username = forms.CharField(help_text="Please Enter a Name")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please Enter a Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), help_text="Verify Password")

    class Meta:
        model = UserRegister
        fields = ('username', 'password', 'password2')



class MeyveCesidiForm(ModelForm):

    class Meta:
        model = MeyveCesitleri
        fields = [
            'name',
        ]