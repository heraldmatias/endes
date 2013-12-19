__author__ = 'holivares'

from django.conf.urls import patterns, url
from inei.endes.views import (IndexView, Cuestionario1View, Cuestionario2View, Cuestionario3View, Cuestionario4View)

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'^cuestionario/1/$', Cuestionario1View.as_view(), name='cuestionario1'),
                       url(r'^cuestionario/2/$', Cuestionario2View.as_view(), name='cuestionario2'),
                       url(r'^cuestionario/3/$', Cuestionario3View.as_view(), name='cuestionario3'),
                       url(r'^cuestionario/4/$', Cuestionario4View.as_view(), name='cuestionario4')
)