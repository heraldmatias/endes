__author__ = 'holivares'

from django.conf.urls import patterns, url
from inei.endes.views import (IndexView, Cuestionario1View, Cuestionario2View,  Cuestionario3View, Cuestionario4View,
                              AgradecimientoView, InstructivoView, AdminView, ReporteView, Agradecimiento2View, OdeiView, Odei2View)

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'^cuestionario/1/$', Cuestionario1View.as_view(), name='cuestionario1'),
                       url(r'^cuestionario/2/$', Cuestionario2View.as_view(), name='cuestionario2'),
                       url(r'^cuestionario/3/$', Cuestionario3View.as_view(), name='cuestionario3'),
                       url(r'^cuestionario/4/$', Cuestionario4View.as_view(), name='cuestionario4'),
                       url(r'^agradecimiento/$', AgradecimientoView.as_view(), name='agradecimiento'),
                       url(r'^agradecimiento2/$', Agradecimiento2View.as_view(), name='agradecimiento2'),
                       url(r'^instructivo/$', InstructivoView.as_view(), name='instructivo'),
                       url(r'^admin/$', AdminView.as_view(), name='admin'),
                       url(r'^reporte/$', ReporteView.as_view(), name='reporte'),
                       url(r'^odeis/$', OdeiView.as_view(), name='odeis'),
                       url(r'^odeis2/$', Odei2View.as_view(), name='odeis2'),
)