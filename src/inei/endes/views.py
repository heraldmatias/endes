from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from inei.auth.forms import UserForm
from inei.auth.models import User, Profesion, Proyectos
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
        if self.request.session.has_key('parte0'):
            if not 'parte1' in self.request.session:
                return HttpResponseRedirect('/cuestionario/2/')
            elif not 'parte2' in self.request.session:
                return HttpResponseRedirect('/cuestionario/3/')
            elif not 'parte3' in self.request.session:
                return HttpResponseRedirect('/cuestionario/4/')
            else:
                return HttpResponseRedirect('/agradecimiento/2/')
        return super(Cuestionario1View, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(Cuestionario1View, self).get_context_data(**kwargs)
        ctx['form'] = UserForm()
        ctx['profesiones'] = Profesion.objects.values('codigo', 'detalle')
        ctx['proyectos'] = Proyectos.objects.values('codigo', 'detalle')
        return ctx

    def post(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps(self.save()), content_type="application/json")
        return response

    def save(self):
        data = dict()
        data.update(self.request.POST)
        for field, v in data.items():
            if isinstance(v, list):
                data[field] = v[0]
        data['username'] = self.request.user.username
        data['password'] = self.request.user.password
        data['last_login'] = self.request.user.last_login

        form = UserForm(data, instance=self.request.user)
        if form.is_valid():
            form.save()
            self.request.session['parte0'] = True
            response = {
                'success': True,
                'error': None,
                'data': 'Todo bien'
            }
        else:
            response = {
                'success': False,
                'error': True,
                'data': form.errors
            }
        return response


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
            return HttpResponseRedirect('/agradecimiento2/')
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

    def get_context_data(self, **kwargs):
        ctx = super(AdminView, self).get_context_data(**kwargs)
        ctx['odeis'] = self.get_odeis()
        return ctx

    def get_queryset(self):
        filtro = {}
        if 'odei' in self.request.GET and self.request.GET.get('odei') != '':
            filtro['usuario__odei'] = self.request.GET['odei']
        return super(AdminView, self).get_queryset().filter(**filtro)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AdminView, self).dispatch(*args, **kwargs)

    def get_odeis(self):
        return [v[0] for v in User.objects.exclude(odei=None).distinct('odei').values_list('odei')]


class ReporteView(TemplateView):
    def get(self, request, *args, **kwargs):
        objects = Cuestionario.objects.all()
        return response_csv(objects, 'reporte')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_admin:
            return HttpResponseRedirect('/agradecimiento/')
        return super(ReporteView, self).dispatch(*args, **kwargs)


class Agradecimiento2View(TemplateView):
    template_name = 'cuestionario/agradecimiento2.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(Agradecimiento2View, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Agradecimiento2View, self).dispatch(*args, **kwargs)