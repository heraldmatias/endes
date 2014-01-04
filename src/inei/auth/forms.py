from inei.auth.models import User

__author__ = 'holivares'

from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'instruccion': forms.Select(attrs={'class': 'span12'}),
            'profesion': forms.Select(attrs={'class': 'span12'}),
            'civil': forms.Select(attrs={'class': 'span12'}),
            'puesto': forms.Select(attrs={'class': 'span12'}),
            'eproyectos_inei': forms.Select(attrs={'class': 'span6', 'readonly': 'readonly'}),
        }

        # def __init__(self, *args, **kwargs):
        #     super(UserForm, self).__init__(*args, **kwargs)
        #     for field in self.fields:
        #         self.fields[field].required = True