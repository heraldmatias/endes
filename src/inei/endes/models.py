# -*- coding: utf-8 -*-
__author__ = 'holivares'

from django.db import models
from inei.auth.models import User


class Cuestionario(models.Model):
    usuario = models.CharField(max_length=20, db_index=True)
    proyecto = models.CharField(max_length=50, db_index=True)
    parte1_pregunta1 = models.TextField(null=True, blank=True)
    parte1_pregunta2 = models.TextField(null=True, blank=True)
    parte1_pregunta3 = models.TextField(null=True, blank=True)
    parte1_pregunta4 = models.CharField(max_length=2, null=True, blank=True,
                                        default='NO')
    parte1_pregunta5 = models.TextField(null=True, blank=True)
    parte1_pregunta6 = models.TextField(null=True, blank=True)
    parte1_pregunta7 = models.TextField(null=True, blank=True)
    parte1_tiempo = models.IntegerField(null=True, blank=True)
    parte2_pregunta1 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta2 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta3 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta4 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta5 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta6 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta7 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta8 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta9 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta10 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta11 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta12 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta13 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta14 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta15 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta16 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta17 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta18 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta19 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta20 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta21 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta22 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta23 = models.CharField(max_length=2, null=True, blank=True)
    parte2_pregunta24 = models.CharField(max_length=2, null=True, blank=True)
    parte2_tiempo = models.IntegerField(null=True, blank=True)
    parte3_pregunta1 = models.IntegerField(null=True, blank=True)
    parte3_pregunta2 = models.IntegerField(null=True, blank=True)
    parte3_pregunta3 = models.IntegerField(null=True, blank=True)
    parte3_pregunta4 = models.IntegerField(null=True, blank=True)
    parte3_pregunta5 = models.IntegerField(null=True, blank=True)
    parte3_pregunta6 = models.IntegerField(null=True, blank=True)
    parte3_pregunta7 = models.IntegerField(null=True, blank=True)
    parte3_pregunta8 = models.IntegerField(null=True, blank=True)
    parte3_pregunta9 = models.IntegerField(null=True, blank=True)
    parte3_pregunta10 = models.IntegerField(null=True, blank=True)
    parte3_tiempo = models.IntegerField(null=True, blank=True)

    def get_estado1(self):
        puntaje = ''
        if self.parte1_pregunta4 == 'NO':
            puntaje = 'NO EVALUADO'
        return puntaje

    def get_estado3(self):
        puntaje = ''
        pregunta1 = -1 if self.parte3_pregunta1 is None else self.parte3_pregunta1
        pregunta2 = -1 if self.parte3_pregunta2 is None else self.parte3_pregunta2
        pregunta3 = -1 if self.parte3_pregunta3 is None else self.parte3_pregunta3
        pregunta4 = -1 if self.parte3_pregunta4 is None else self.parte3_pregunta4
        pregunta5 = -1 if self.parte3_pregunta5 is None else self.parte3_pregunta5
        pregunta6 = -1 if self.parte3_pregunta6 is None else self.parte3_pregunta6
        pregunta7 = -1 if self.parte3_pregunta7 is None else self.parte3_pregunta7
        pregunta8 = -1 if self.parte3_pregunta8 is None else self.parte3_pregunta8
        pregunta9 = -1 if self.parte3_pregunta9 is None else self.parte3_pregunta9
        pregunta10 = -1 if self.parte3_pregunta10 is None else self.parte3_pregunta10
        resultado = pregunta1 + pregunta2 + pregunta3+ pregunta4+pregunta5+pregunta6+pregunta7+pregunta8+pregunta9
        if resultado >= 10 and pregunta10 in (1, 2):
            if resultado >= 10 and resultado <= 14:
                puntaje = 'EPISODIO DEPRESIVO MAYOR LEVE'
            elif resultado >= 15 and resultado <= 19:
                puntaje = 'EPISODIO DEPRESIVO MAYOR MODERADA'
            elif resultado >= 20 and resultado <= 27:
                puntaje = 'EPISODIO DEPRESIVO MAYOR SEVERA'
        elif (resultado>=0 and pregunta10 < 10) and pregunta10 == 3:
            puntaje = 'NO TIENE DEPRESIÓN'
        else:
            puntaje = 'NO COMPLETO EL CUESTIONARIO'
        return puntaje

    def get_estado2(self):
        puntaje = ''
        puntaje += '1 - ' + self.get_tipo(self.parte2_pregunta1) + '<br>'
        puntaje += '2 - ' + self.get_tipo(self.parte2_pregunta2) + '<br>'
        puntaje += '3 - ' + self.get_tipo(self.parte2_pregunta3) + '<br>'
        puntaje += '4 - ' + self.get_tipo(self.parte2_pregunta4) + '<br>'
        puntaje += '5 - ' + self.get_tipo(self.parte2_pregunta5) + '<br>'
        puntaje += '6 - ' + self.get_tipo(self.parte2_pregunta6) + '<br>'
        puntaje += '7 - ' + self.get_tipo(self.parte2_pregunta7) + '<br>'
        puntaje += '8 - ' + self.get_tipo(self.parte2_pregunta8) + '<br>'
        puntaje += '9 - ' + self.get_tipo(self.parte2_pregunta9) + '<br>'
        puntaje += '10 - ' + self.get_tipo(self.parte2_pregunta10) + '<br>'
        puntaje += '11 - ' + self.get_tipo(self.parte2_pregunta11) + '<br>'
        puntaje += '12 - ' + self.get_tipo(self.parte2_pregunta12) + '<br>'
        puntaje += '13 - ' + self.get_tipo(self.parte2_pregunta13) + '<br>'
        puntaje += '14 - ' + self.get_tipo(self.parte2_pregunta14) + '<br>'
        puntaje += '15 - ' + self.get_tipo(self.parte2_pregunta15) + '<br>'
        puntaje += '16 - ' + self.get_tipo(self.parte2_pregunta16) + '<br>'
        puntaje += '17 - ' + self.get_tipo(self.parte2_pregunta17) + '<br>'
        puntaje += '18 - ' + self.get_tipo(self.parte2_pregunta18) + '<br>'
        puntaje += '19 - ' + self.get_tipo(self.parte2_pregunta19) + '<br>'
        puntaje += '20 - ' + self.get_tipo(self.parte2_pregunta20) + '<br>'
        puntaje += '21 - ' + self.get_tipo(self.parte2_pregunta21) + '<br>'
        puntaje += '22 - ' + self.get_tipo(self.parte2_pregunta22) + '<br>'
        puntaje += '23 - ' + self.get_tipo(self.parte2_pregunta23) + '<br>'
        puntaje += '24 - ' + self.get_tipo(self.parte2_pregunta24) + '<br>'
        return puntaje

    def get_tipo(self, valor):
        return 'Sinceridad' if valor == 'S' else 'Extraversión' if valor == 'E' else 'Neurotismo' if valor == 'N' else 'Psicotismo' if valor == 'P' else '-'