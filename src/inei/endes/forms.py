__author__ = 'holivares'

from django import forms
from inei.endes.models import Cuestionario


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=10)


class CuestionarioForm(forms.ModelForm):
    class Meta:
        model = Cuestionario