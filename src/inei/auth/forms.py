# -*- coding: utf-8 -*-
from __future__ import division
from django.core.exceptions import ValidationError
from inei.auth.models import User

__author__ = 'holivares'

from django import forms


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ('eproyectos_inei', 'vive_otro', 'edades', 'ozei', 'hijos', 'is_admin', 'eotro',
                             'anos_eotro', 'meses_eotro', 'institucion_eotro', 'anos_einei', 'meses_einei', 'einei'):
                self.fields[field].required = True
        if self.data.get('experiencia_inei') == '1':
            self.fields['eproyectos_inei'].required = True
        if self.data.get('vive') == '6':
            self.fields['vive_otro'].required = True


    def clean_edades(self):
        cleaned_data = self.cleaned_data
        hijos = cleaned_data['hijos']
        if 'edad' in cleaned_data:
            edad = (cleaned_data['edad']-10)
            edades = cleaned_data['edades'].split(',')
            if hijos > 0:
                if hijos != len(edades):
                    raise ValidationError('corregir edades')
                for hedad in edades:
                    if int(hedad) > edad:
                        raise ValidationError('corregir edades')
        return hijos

    def clean_anos_experiencia(self):
        cleaned_data = self.cleaned_data
        experiencia = cleaned_data['anos_experiencia']
        if 'edad' in cleaned_data:
            edad = (cleaned_data['edad']-18)
            if experiencia > edad:
                raise ValidationError('corregir los años de experiencia')
        return experiencia

    # def clean_meses_experiencia(self):
    #     cleaned_data = self.cleaned_data
    #     mexperiencia = cleaned_data['meses_experiencia']
    #     aexperiencia = cleaned_data['anos_experiencia']*12
    #     experiencia = (mexperiencia+aexperiencia) / 12
    #     if 'edad' in cleaned_data:
    #         edad = (cleaned_data['edad']-18)
    #         if experiencia > edad:
    #             raise ValidationError('corregir los años de experiencia')
    #     return mexperiencia
    #
    # def clean_anos_einei(self):
    #     cleaned_data = self.cleaned_data
    #     aexperiencia = cleaned_data['anos_einei']
    #     if 'anos_experiencia' in cleaned_data:
    #         experiencia = cleaned_data['anos_experiencia']
    #         if aexperiencia > experiencia:
    #             raise ValidationError('corregir los años de experiencia')
    #     return aexperiencia

    class Meta:
        model = User
        widgets = {
            'instruccion': forms.Select(attrs={
                'class': 'span12 lista',
                'data-original-title': u'Escoja su grado de instrucción',
                'data-placement': 'top',
            }),
            'profesion': forms.Select(attrs={
                'class': 'span12 lista',
                'data-original-title': u'Escoja su profesión',
                'data-placement': 'top'
            }),
            'civil': forms.Select(attrs={
                'class': 'span12 lista',
                'data-original-title': u'Escoja su estado civil',
                'data-placement': 'top',
            }),
            'puesto': forms.Select(attrs={
                'class': 'span12 lista',
                'data-original-title': u'Escoja el puesto al que postula',
                'data-placement': 'top',
            }),
            'eproyectos_inei': forms.Select(attrs={
                'class': 'span6',
                'readonly': 'readonly'
            }),
            'apellido_paterno': forms.TextInput(attrs={
                'class': 'span12 texto',
                'data-original-title': 'Escriba su apellido paterno',
                'data-placement': 'top',
                'placeholder': 'Escriba su apellido paterno'
            }),
            'apellido_materno': forms.TextInput(attrs={
                'class': 'span12 texto',
                'data-original-title': 'Escriba su apellido materno',
                'data-placement': 'top',
                'placeholder': 'Escriba su apellido materno'
            }),
            'nombres': forms.TextInput(attrs={
                'class': 'span12 texto',
                'data-original-title': 'Escriba su(s) nombre(s)',
                'data-placement': 'top',
                'placeholder': 'Escriba su(s) nombre(s)'
            }),
            'edad': forms.TextInput(attrs={
                'class': 'span5',
                'data-original-title': 'Escriba su edad. Debe ser mayor a 18',
                'data-placement': 'top',
                'placeholder': 'Edad',
                'maxlength': 2
            }),
            'hijos': forms.TextInput(attrs={
                'class': 'span5',
                'data-original-title': 'Escriba el número de hijos',
                'data-placement': 'top',
                'placeholder': 'Hijos',
                'maxlength': 2
            }),
            'edades': forms.TextInput(attrs={
                'class': 'span12',
                'data-original-title': 'Escriba la(s) edad(es) de su(s) hijo(s) separadas por comas. La cantidad de edades ingresadas debe ser la misma que la cantidad de hijos',
                'data-placement': 'top',
                'placeholder': 'Edad(es)',
                'disabled': 'disabled'
            }),
            'vive_otro': forms.TextInput(attrs={
                'class': 'span5 texto',
                'data-original-title': 'Escriba con quien vive',
                'data-placement': 'top',
                'placeholder': 'Escriba con quien vive',
                'disabled': 'disabled'
            }),
            'anos_experiencia': forms.TextInput(attrs={
                'class': 'span5 numero',
                'data-original-title': 'Escriba el número de años de experiencia laboral',
                'data-placement': 'top',
                'placeholder': 'Años',
                'maxlength': 2
            }),
            'meses_experiencia': forms.TextInput(attrs={
                'class': 'span5 numero',
                'data-original-title': 'Escriba el número de meses de experiencia laboral. Debe ser menor a 12.',
                'data-placement': 'top',
                'placeholder': 'Meses',
                'maxlength': 2
            }),
            'odei': forms.Select(attrs={
                'class': 'span6',
                'data-original-title': 'Escoja la ODEI a la que postula',
                'data-placement': 'top',
                'placeholder': 'ODEI'
            }),
            'anos_einei': forms.TextInput(attrs={
                'class': 'span2 numero',
                'data-original-title': 'Escriba el número de años de experiencia laboral en INEI',
                'data-placement': 'top',
                'placeholder': 'Años',
                'disabled': 'disabled',
                'maxlength': 2
            }),
            'meses_einei': forms.TextInput(attrs={
                'class': 'span2 numero',
                'data-original-title': 'Escriba el número de meses de experiencia laboral en INEI. Debe ser menor a 12.',
                'data-placement': 'top',
                'placeholder': 'Meses',
                'disabled': 'disabled',
                'maxlength': 2
            }),
            'anos_eotro': forms.TextInput(attrs={
                'class': 'span2 numero',
                'data-original-title': 'Escriba el número de años de experiencia laboral en otra institución',
                'data-placement': 'top',
                'placeholder': 'Años',
                'disabled': 'disabled',
                'maxlength': 2
            }),
            'meses_eotro': forms.TextInput(attrs={
                'class': 'span2 numero',
                'data-original-title': 'Escriba el número de meses de experiencia laboral en otra institución. Debe ser menor a 12.',
                'data-placement': 'top',
                'placeholder': 'Meses',
                'disabled': 'disabled',
                'maxlength': 2
            }),
            'institucion_eotro': forms.TextInput(attrs={
                'class': 'span5 texto',
                'data-original-title': 'Escriba el nombre de la institución donde laboro',
                'data-placement': 'top',
                'placeholder': 'Nombre de la Institución',
                'disabled': 'disabled'
            }),
        }