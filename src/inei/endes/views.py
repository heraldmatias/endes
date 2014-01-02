from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from inei.endes.models import Cuestionario
from django.views.generic import FormView, TemplateView
from django.http.response import HttpResponseRedirect, HttpResponse
from inei.endes.forms import LoginForm
from django.contrib.auth import login, authenticate, logout
from inei.endes.forms import CuestionarioForm
import json
from inei.endes.services import response_csv

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
                id = user.id or 0
                login(self.request, user)
                if user.is_admin:
                    return HttpResponseRedirect('/admin/')
                if Cuestionario.objects.filter(usuario=id).exists():
                    return HttpResponseRedirect('/agradecimiento/')
                return HttpResponseRedirect(self.get_success_url())
            else:
                #cuenta deshabilitada
                return self.render_to_response(self.get_context_data(form=form))
        else:
            #login invalido
            return self.render_to_response(self.get_context_data(form=form))


class InstructivoView(TemplateView):
    template_name = 'instructivo.html'


class Cuestionario1View(TemplateView):
    template_name = 'cuestionario/cuestionario1.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Cuestionario1View, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(Cuestionario1View, self).get(request, *args, **kwargs)

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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        id = self.request.user.id or 0
        if Cuestionario.objects.filter(usuario=id).exists():
            return HttpResponseRedirect('/agradecimiento/')
        if self.request.session.has_key('parte1'):
            if not self.request.session.has_key('parte2'):
                return HttpResponseRedirect('/cuestionario/3/')
        return super(Cuestionario2View, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps(self.save()), content_type="application/json")
        return response

    def save(self):
        self.request.session['cuestionario'] = self.request.POST
        self.request.session['parte1'] = True
        return {
            'success': True,
            'error': None,
            'data': 'Todo bien'
        }


class Cuestionario3View(TemplateView):
    template_name = 'cuestionario/cuestionario3.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        id = self.request.user.id or 0
        if Cuestionario.objects.filter(usuario=id).exists():
            return HttpResponseRedirect('/agradecimiento/')
        if self.request.session.has_key('parte2'):
            if not 'parte3' in self.request.session:
                return HttpResponseRedirect('/cuestionario/4/')
        return super(Cuestionario3View, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps(self.save()), content_type="application/json")
        return response

    def save(self):
        cuestionario = self.request.session.get('cuestionario', dict())
        cuestionario.update(self.request.POST)
        self.request.session['cuestionario'] = cuestionario
        self.request.session['parte2'] = True
        return {
            'success': True,
            'error': None,
            'data': 'Todo bien'
        }


class Cuestionario4View(TemplateView):
    template_name = 'cuestionario/cuestionario4.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        id = self.request.user.id or 0
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
            id = self.request.user.id or 0
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
                self.request.session['parte3'] = True
                if self.request.session.has_key('cuestionario'):
                    del self.request.session['cuestionario']
            else:
                response['data'] = 'Usted ya ha completado el cuestionario'
        except Exception as e:
            response['success'] = False
            response['error'] = True
            response['data'] = e.message
        return response


class AgradecimientoView(TemplateView):
    template_name = 'cuestionario/agradecimiento.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(AgradecimientoView, self).get(request, *args, **kwargs)

    def save(self):
        response = {
            'success': True,
            'error': None,
            'data': 'Todo bien'
        }
        try:
            id = self.request.user.id or 0
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
                if self.request.session.has_key('cuestionario'):
                    del self.request.session['cuestionario']
            else:
                response['data'] = 'Usted ya ha completado el cuestionario'
        except Exception as e:
            response['success'] = False
            response['error'] = True
            response['data'] = e.message
        return response

    def post(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps(self.save()), content_type="application/json")
        return response

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AgradecimientoView, self).dispatch(*args, **kwargs)


class AdminView(ListView):
    template_name = 'admin/admin.html'
    model = Cuestionario
    paginate_by = 10
    context_object_name = 'objects'

    #def get_queryset(self):
    #    return Cuestionario.objects.filter()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AdminView, self).dispatch(*args, **kwargs)


class ReporteView(TemplateView):
    def get(self, request, *args, **kwargs):
        objects = Cuestionario.objects.all()
        return response_csv(objects, 'reporte')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_admin:
            return HttpResponseRedirect('/agradecimiento/')
        return super(ReporteView, self).dispatch(*args, **kwargs)