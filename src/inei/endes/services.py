# -*- coding: utf-8 -*-
from inei.auth.models import Odei
import csv
from django.http import HttpResponse
from django.template import loader, Context
from xlwt import *

__author__ = 'holivares'


def response_csv(queryset, filename):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='application/excel')
    response['Content-Disposition'] = 'attachment; filename="%s.xls"' % filename

    fnt = Font()
    fnt.name = 'Arial'
    fnt.colour_index = 0
    #fnt.bold = True

    fnt_header = Font()
    fnt_header.name = 'Arial'
    fnt_header.colour_index = 4
    fnt_header.bold = True

    borders = Borders()
    borders.left = 6
    borders.right = 6
    borders.top = 6
    borders.bottom = 6

    al = Alignment()
    al.horz = Alignment.HORZ_CENTER
    al.vert = Alignment.VERT_CENTER

    style = XFStyle()
    style.font = fnt
    style.borders = borders
    style.alignment = al

    style_header = XFStyle()
    style_header.font = fnt_header
    style_header.borders = borders
    style_header.alignment = al

    wb = Workbook()
    ws0 = wb.add_sheet('sheet0')
    #ws1 = wb.add_sheet('sheet1')
    #ws2 = wb.add_sheet('sheet2')

    # for i in range(0, 0x200, 2):
    #     ws0.write_merge(i, i + 1, 1, 5, 'test %d' % i, style)
    odeis = get_odeis()
    r = 1

    ws0.col(0).width = 256 * 20
    ws0.col(1).width = 256 * 50
    ws0.col(2).width = 256 * 150
    ws0.col(3).width = 256 * 10
    ws0.col(4).width = 256 * 15
    ws0.col(5).width = 256 * 10
    ws0.col(6).width = 256 * 30
    ws0.write(0, 0, 'ODEI', style_header)
    ws0.write(0, 1, 'POSTULANTE', style_header)
    ws0.write(0, 2, 'PARTE 1', style_header)
    ws0.write(0, 3, 'PARTE 2', style_header)
    ws0.write(0, 4, 'DIAGNOSTICO', style_header)
    ws0.write(0, 5, 'PARTE 3', style_header)
    ws0.write(0, 6, 'DIAGNOSTICO', style_header)
    for odei in odeis:
        objects = queryset.filter(usuario__odei__odei=odei)
        c = 0
        items = (objects.count() * 4)-1
        if items < 0:
            continue
        ws0.write_merge(r, r+items, c, c, odei, style)
        for object in objects:
            c = 0
            c += 1
            ws0.write_merge(r, r + 3, c, c, object.usuario.get_full_name(), style)
            parte1 = get_estado1(object)
            parte2 = get_estado2(object)
            parte3 = get_estado3(object)
            c += 1
            for k, v in parte1.items():
                ws0.write_merge(r, r + 1, c, c, k + ' - ' + v, style)
                r += 2
            c += 1
            r -= 4
            for k, v in parte2.items():
                ws0.write(r, c, k + ' - ' + str(v), style)
                r += 1
            c += 1
            r -= 4
            ws0.write_merge(r, r + 3, c, c, '', style)
            c += 1
            for k, v in parte3.items():
                ws0.write_merge(r, r + 3, c, c, str(v), style)
                c += 1
                ws0.write_merge(r, r + 3, c, c, k, style)
            r += 4

    wb.save(response)
    return response


def get_estado1(cuestionario):
    puntaje = {}
    if cuestionario.parte1_pregunta4 == 'NO' or cuestionario.parte1_pregunta4 == '' or cuestionario.parte1_pregunta4 is None:
        puntaje['Preg. 3'] = u'%s' % cuestionario.parte1_pregunta3
        puntaje['NO ACEPTADO'] = '-'
    else:
        puntaje['Preg. 3'] = u'%s' % cuestionario.parte1_pregunta3
        puntaje['Preg. 6'] = u'%s' % cuestionario.parte1_pregunta6
    return puntaje


def get_estado3(cuestionario):
    _puntaje = {}
    pregunta1 = -1 if cuestionario.parte3_pregunta1 is None else cuestionario.parte3_pregunta1
    pregunta2 = -1 if cuestionario.parte3_pregunta2 is None else cuestionario.parte3_pregunta2
    pregunta3 = -1 if cuestionario.parte3_pregunta3 is None else cuestionario.parte3_pregunta3
    pregunta4 = -1 if cuestionario.parte3_pregunta4 is None else cuestionario.parte3_pregunta4
    pregunta5 = -1 if cuestionario.parte3_pregunta5 is None else cuestionario.parte3_pregunta5
    pregunta6 = -1 if cuestionario.parte3_pregunta6 is None else cuestionario.parte3_pregunta6
    pregunta7 = -1 if cuestionario.parte3_pregunta7 is None else cuestionario.parte3_pregunta7
    pregunta8 = -1 if cuestionario.parte3_pregunta8 is None else cuestionario.parte3_pregunta8
    pregunta9 = -1 if cuestionario.parte3_pregunta9 is None else cuestionario.parte3_pregunta9
    pregunta10 = -1 if cuestionario.parte3_pregunta10 is None else cuestionario.parte3_pregunta10
    resultado = pregunta1 + pregunta2 + pregunta3 + pregunta4 + pregunta5 + pregunta6 + pregunta7 + pregunta8 + pregunta9
    if resultado >= 10 and pregunta10 in (1, 2):
        if 10 <= resultado <= 14:
            puntaje = 'EPISODIO DEPRESIVO MAYOR LEVE'
        elif 15 <= resultado <= 19:
            puntaje = 'EPISODIO DEPRESIVO MAYOR MODERADA'
        elif 20 <= resultado <= 27:
            puntaje = 'EPISODIO DEPRESIVO MAYOR SEVERA'
    elif (resultado >= 0 and resultado < 10) or (resultado > 10 and pregunta10 == 3) or (resultado == 0 and pregunta10 == 3):
        puntaje = u'NO TIENE DEPRESIÓN'
    else:
        puntaje = 'NO COMPLETO EL CUESTIONARIO'
    _puntaje[puntaje] = resultado if resultado >= 0 else None
    return _puntaje


def get_estado2(cuestionario):
    puntaje = {}
    n_count = count_rpta(cuestionario.parte2_pregunta1, 'N') + count_rpta(cuestionario.parte2_pregunta9, 'N') + \
              count_rpta(cuestionario.parte2_pregunta11, 'N') + count_rpta(cuestionario.parte2_pregunta14, 'N') + \
              count_rpta(cuestionario.parte2_pregunta18, 'N') + count_rpta(cuestionario.parte2_pregunta21, 'N')
    e_count = count_rpta(cuestionario.parte2_pregunta2, 'E') + count_rpta(cuestionario.parte2_pregunta4, 'E') + \
              count_rpta(cuestionario.parte2_pregunta13, 'E') + count_rpta(cuestionario.parte2_pregunta15, 'E') + \
              count_rpta(cuestionario.parte2_pregunta20, 'E') + count_rpta(cuestionario.parte2_pregunta23, 'E')
    s_count = count_rpta(cuestionario.parte2_pregunta5, 'S') + count_rpta(cuestionario.parte2_pregunta7, 'S') + \
              count_rpta(cuestionario.parte2_pregunta10, 'S') + count_rpta(cuestionario.parte2_pregunta17, 'S') + \
              count_rpta(cuestionario.parte2_pregunta19, 'S') + count_rpta(cuestionario.parte2_pregunta24, 'S')
    p_count = count_rpta(cuestionario.parte2_pregunta3, 'P') + count_rpta(cuestionario.parte2_pregunta6, 'P') + \
              count_rpta(cuestionario.parte2_pregunta8, 'P') + count_rpta(cuestionario.parte2_pregunta12, 'P') + \
              count_rpta(cuestionario.parte2_pregunta16, 'P') + count_rpta(cuestionario.parte2_pregunta22, 'P')
    puntaje['N'] = n_count
    puntaje['E'] = e_count
    puntaje['S'] = s_count
    puntaje['P'] = p_count
    return puntaje


def count_rpta(rpta, value=''):
    if rpta is not None:
        return 1 if rpta == value else 0
    return 0


def get_tipo(valor):
    return 'Sinceridad' if valor == 'S' else 'Extraversión' if valor == 'E' else 'Neurotismo' if valor == 'N' else 'Psicotismo' if valor == 'P' else '-'


def get_odeis():
    return [v[0] for v in Odei.objects.exclude(odei=None).distinct('odei').values_list('odei')]