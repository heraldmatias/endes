__author__ = 'holivares'

from django.views.generic import FormView, TemplateView
from django.http.response import HttpResponseRedirect, HttpResponse
from inei.endes.forms import LoginForm
from django.contrib.auth import login, authenticate
from inei.endes.forms import CuestionarioForm
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
                #print self.request.user
                login(self.request, user)
                #print self.request.user
                return HttpResponseRedirect(self.get_success_url())
            else:
                #cuenta deshabilitada
                return self.render_to_response(self.get_context_data(form=form))
        else:
            #login invalido
            return self.render_to_response(self.get_context_data(form=form))


class Cuestionario1View(TemplateView):
    template_name = 'cuestionario/cuestionario1.html'

    def get(self, request, *args, **kwargs):
        #print self.request.user.__dict__
        #print self.request.session['_auth_user_id']
        return super(Cuestionario1View, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps(self.save()), content_type="application/json")
        #print self.request.user.__dict__
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
        self.request.session['cuestionario'] = self.request.POST
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
        response = {
            'success': True,
            'error': None,
            'data': 'Todo bien'
        }
        try:
            cuestionario = self.request.session.get('cuestionario', dict())
            cuestionario.update(self.request.POST)
            cuestionario['usuario'] = self.request.user.id
            cuestionario['proyecto'] = self.request.user.proyecto or 'NINGUNO'
            #aqui guardar
            for field, v in cuestionario.items():
                if field.startswith('parte2'):
                    cuestionario[field] = v[0]
                elif field.startswith('parte3'):
                    cuestionario[field] = int(v[0])
            form = CuestionarioForm(cuestionario)
            form.save()
            del self.request.session['cuestionario']
        except Exception as e:
            response['success'] = False
            response['error'] = True
            response['data'] = e.message
        return response


class Cuestionario4View(TemplateView):
    template_name = 'cuestionario/cuestionario4.html'

    def post(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps(self.save()), content_type="application/json")
        return response

    def save(self):
        response = {
            'success': True,
            'error': None,
            'data': 'Todo bien'
        }
        try:
            cuestionario = self.request.session.get('cuestionario', dict())
            cuestionario.update(self.request.POST)
            cuestionario['usuario'] = self.request.user
            cuestionario['proyecto'] = self.request.user.proyecto
            #aqui guardar
            for field, v in cuestionario.items():
                if field.startswith('parte2'):
                    cuestionario[field] = v[0]
                elif field.startswith('parte3'):
                    cuestionario[field] = int(v[0])
            form = CuestionarioForm(cuestionario)
            form.save()
            del self.request.session['cuestionario']
        except Exception as e:
            response['success'] = False
            response['error'] = True
            response['data'] = e.message
        return response