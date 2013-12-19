__author__ = 'holivares'

from django.views.generic import FormView, TemplateView
from django.http.response import HttpResponseRedirect, HttpResponse
from inei.endes.forms import LoginForm
from django.contrib.auth import login, authenticate
from inei.endes.base import JSONResponseMixin
import json


class IndexView(FormView):
    template_name = 'index.html'
    form_class = LoginForm
    success_url = '/cuestionario/1/'

    def form_valid(self, form):
        username = form.data['username']
        password = form.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponseRedirect(self.get_success_url())
            else:
                #cuenta deshabilitada
                return self.render_to_response(self.get_context_data(form=form))
        else:
            #login invalido
            return self.render_to_response(self.get_context_data(form=form))


class Cuestionario1View(TemplateView):
    template_name = 'cuestionario/cuestionario1.html'

    def post(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps(self.save()), content_type="application/json")
        return response

    def save(self):
        return {
            'success': True,
            'error': None,
            'data': 'Todo bien'
        }


class Cuestionario2View(TemplateView):
    template_name = 'cuestionario/cuestionario2.html'

    def post(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps(self.save()), content_type="application/json")
        return response

    def save(self):
        return {
            'success': True,
            'error': None,
            'data': 'Todo bien'
        }


class Cuestionario3View(TemplateView):
    template_name = 'cuestionario/cuestionario3.html'

    def post(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps(self.save()), content_type="application/json")
        return response

    def save(self):
        return {
            'success': True,
            'error': None,
            'data': 'Todo bien'
        }


class Cuestionario4View(TemplateView):
    template_name = 'cuestionario/cuestionario4.html'

    def post(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps(self.save()), content_type="application/json")
        return response

    def save(self):
        return {
            'success': True,
            'error': None,
            'data': 'Todo bien'
        }