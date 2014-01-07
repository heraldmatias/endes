# -*- coding: utf-8 -*-
__author__ = 'holivares'

from django.db import models
from inei.auth.models import Usuario


class Cuestionario(models.Model):
    usuario = models.ForeignKey(Usuario, db_index=True)
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
    parte3_pregunta10 = models.IntegerField(null=True, blank=True, default=3)
    parte3_tiempo = models.IntegerField(null=True, blank=True)

    def get_estado1(self):
        puntaje = ''
        if self.parte1_pregunta4 == 'NO' or self.parte1_pregunta4 == '' or self.parte1_pregunta4 is None:
            puntaje = 'NO ACEPTADO'
        else:
            puntaje += 'Preg. 3 = ' + self.parte1_pregunta3 + '<br><br>'
            puntaje += 'Preg. 6 = ' + self.parte1_pregunta6
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
                puntaje = 'EPISODIO DEPRESIVO MAYOR LEVE = ' + str(resultado)
            elif resultado >= 15 and resultado <= 19:
                puntaje = 'EPISODIO DEPRESIVO MAYOR MODERADA = ' + str(resultado)
            elif resultado >= 20 and resultado <= 27:
                puntaje = 'EPISODIO DEPRESIVO MAYOR SEVERA = ' + str(resultado)
        elif (resultado >= 0 and resultado < 10) or (resultado > 10 and pregunta10 == 3) or (resultado == 0 and pregunta10 == 3):
            puntaje = 'NO TIENE DEPRESIÓN = ' + str(resultado)
        else:
            puntaje = 'NO COMPLETO EL CUESTIONARIO'
        return puntaje

    def get_estado2(self):
        puntaje = ''
        puntaje = ''
        n_count = self.count_rpta(self.parte2_pregunta1, 'N') + self.count_rpta(self.parte2_pregunta9, 'N') + \
              self.count_rpta(self.parte2_pregunta11, 'N') + self.count_rpta(self.parte2_pregunta14, 'N') + \
              self.count_rpta(self.parte2_pregunta18, 'N') + self.count_rpta(self.parte2_pregunta21, 'N')
        e_count = self.count_rpta(self.parte2_pregunta2, 'E') + self.count_rpta(self.parte2_pregunta4, 'E') + \
              self.count_rpta(self.parte2_pregunta13, 'E') + self.count_rpta(self.parte2_pregunta15, 'E') + \
              self.count_rpta(self.parte2_pregunta20, 'E') + self.count_rpta(self.parte2_pregunta23, 'E')
        s_count = self.count_rpta(self.parte2_pregunta5, 'S') + self.count_rpta(self.parte2_pregunta7, 'S') + \
              self.count_rpta(self.parte2_pregunta10, 'S') + self.count_rpta(self.parte2_pregunta17, 'S') + \
              self.count_rpta(self.parte2_pregunta19, 'S') + self.count_rpta(self.parte2_pregunta24, 'S')
        p_count = self.count_rpta(self.parte2_pregunta3, 'P') + self.count_rpta(self.parte2_pregunta6, 'P') + \
              self.count_rpta(self.parte2_pregunta8, 'P') + self.count_rpta(self.parte2_pregunta12, 'P') + \
              self.count_rpta(self.parte2_pregunta16, 'P') + self.count_rpta(self.parte2_pregunta22, 'P')
        puntaje += 'N = ' + str(n_count) + '<br>'
        puntaje += 'E = ' + str(e_count) + '<br>'
        puntaje += 'S = ' + str(s_count) + '<br>'
        puntaje += 'P = ' + str(p_count) + '<br>'
        return puntaje

    def count_rpta(self, rpta, value=''):
        if rpta is not None:
            return 1 if rpta == value else 0
        return 0

    def get_tipo(self, valor):
        return 'Sinceridad' if valor == 'S' else 'Extraversión' if valor == 'E' else 'Neurotismo' if valor == 'N' else 'Psicotismo' if valor == 'P' else '-'