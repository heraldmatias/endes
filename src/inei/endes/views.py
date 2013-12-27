from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from inei.endes.models import Cuestionario
from django.views.generic import FormView, TemplateView
from django.http.response import HttpResponseRedirect, HttpResponse
from inei.endes.forms import LoginForm
from django.contrib.auth import login, authenticate
from inei.endes.forms import CuestionarioForm
import json


__author__ = 'holivares'

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
                id = user.id or 1
                if Cuestionario.objects.filter(usuario=id).exists():
                    return HttpResponseRedirect('/agradecimiento/')
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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Cuestionario1View, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        id = self.request.user.id or 1
        if Cuestionario.objects.filter(usuario=id).exists():
            return HttpResponseRedirect('/agradecimiento/')
        return super(Cuestionario2View, self).dispatch(*args, **kwargs)

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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        id = self.request.user.id or 1
        if Cuestionario.objects.filter(usuario=id).exists():
            return HttpResponseRedirect('/agradecimiento/')
        return super(Cuestionario3View, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps(self.save()), content_type="application/json")
        return response

    def save(self):
        cuestionario = self.request.session.get('cuestionario', dict())
        cuestionario.update(self.request.POST)
        self.request.session['cuestionario'] = cuestionario
        return {
            'success': True,
            'error': None,
            'data': 'Todo bien'
        }


class Cuestionario4View(TemplateView):
    template_name = 'cuestionario/cuestionario4.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        id = self.request.user.id or 1
        if Cuestionario.objects.filter(usuario=id).exists():
            return HttpResponseRedirect('/agradecimiento/')
        return super(Cuestionario4View, self).dispatch(*args, **kwargs)

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
            id = self.request.user.id or 1
            if not Cuestionario.objects.filter(usuario=id).exists():
                cuestionario = self.request.session.get('cuestionario', dict())
                cuestionario.update(self.request.POST)
                cuestionario['usuario'] = id
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
            else:
                response['data'] = 'Usted ya ha completado el cuestionario'
        except Exception as e:
            response['success'] = False
            response['error'] = True
            response['data'] = e
        return response


class AgradecimientoView(TemplateView):
    template_name = 'cuestionario/agradecimiento.html'

    def save(self):
        response = {
            'success': True,
            'error': None,
            'data': 'Todo bien'
        }
        try:
            id = self.request.user.id or 1
            if not Cuestionario.objects.filter(usuario=id).exists():
                cuestionario = self.request.session.get('cuestionario', dict())
                cuestionario.update(self.request.POST)
                cuestionario['usuario'] = id
                cuestionario['proyecto'] = self.request.user.proyecto or 'NINGUNO'
                #aqui guardar
                for field, v in cuestionario.items():
                    if field.startswith('parte1'):
                        cuestionario[field] = v[0]
                    if field.startswith('parte2'):
                        cuestionario[field] = v[0]
                    elif field.startswith('parte3'):
                        cuestionario[field] = int(v[0])
                form = CuestionarioForm(cuestionario)
                form.save()
                del self.request.session['cuestionario']
            else:
                response['data'] = 'Usted ya ha completado el cuestionario'
        except Exception as e:
            response['success'] = False
            response['error'] = True
            response['data'] = e
        return response

    def post(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps(self.save()), content_type="application/json")
        return response

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AgradecimientoView, self).dispatch(*args, **kwargs)