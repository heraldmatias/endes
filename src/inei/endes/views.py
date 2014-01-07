import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from inei.auth.forms import UserForm
from inei.auth.models import Profesion, Proyectos, Odei, Region
from inei.endes.models import Cuestionario
from django.views.generic import FormView, TemplateView
from django.http.response import HttpResponseRedirect, HttpResponse
from inei.endes.forms import LoginForm
from django.contrib.auth import login, authenticate, logout
from inei.endes.forms import CuestionarioForm
import json
from inei.endes.services import response_csv
from django.views.decorators.csrf import csrf_exempt

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
                    return HttpResponseRedirect('/agradecimiento2/')
                return HttpResponseRedirect(self.get_success_url())
            else:
                #cuenta deshabilitada
                return self.render_to_response(self.get_context_data(form=form))
        else:
            #login invalido
            return self.render_to_response(self.get_context_data(form=form))


class InstructivoView(TemplateView):
    template_name = 'instructivo.html'

    #@method_decorator(login_required)
    #def dispatch(self, *args, **kwargs):
    #    if self.request.session.has_key('parte0'):
    #        if not 'parte1' in self.request.session:
    #            return HttpResponseRedirect('/cuestionario/2/')
    #        elif not 'parte2' in self.request.session:
    #            return HttpResponseRedirect('/cuestionario/3/')
    #        elif not 'parte3' in self.request.session:
    #            return HttpResponseRedirect('/cuestionario/4/')
    #        else:
    #            return HttpResponseRedirect('/agradecimiento/2/')
    #    return super(InstructivoView, self).dispatch(*args, **kwargs)

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
        ctx['profesiones'] = Profesion.objects.values('codigo', 'detalle').order_by('detalle')
        ctx['regiones'] = Region.objects.values('codigo', 'descripcion').order_by('descripcion')
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
                if field == 'eproyectos_inei':
                    data[field] = ','.join(v)
                else:
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

    def process_elapsed_time(self):
        if 'vparte1' in self.request.COOKIES:
            elapsed = datetime.datetime.now() - datetime.datetime.strptime(self.request.COOKIES['vparte1'], '%Y-%m-%d %H:%M:%S')
            self.request.session['parte1_tiempo'] = int(elapsed.total_seconds())
            return self.request.session['parte1_tiempo']
        else:
            return 0

    def get_context_data(self, **kwargs):
        ctx = super(Cuestionario2View, self).get_context_data(**kwargs)
        ctx['parte1_tiempo'] = self.process_elapsed_time()
        return ctx

    def get(self, request, *args, **kwargs):
        response = super(Cuestionario2View, self).get(request, *args, **kwargs)
        if 'vparte1' not in self.request.COOKIES:
            response.set_cookie('vparte1', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 600)
        return response

    def post(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps(self.save()), content_type="application/json")
        response.delete_cookie('vparte1')
        return response

    def save(self):
        self.request.session['cuestionario'] = self.request.POST
        self.request.session['parte1'] = True
        self.process_elapsed_time()
        del self.request.COOKIES['vparte1']
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
        response.delete_cookie('vparte2')
        return response

    def process_elapsed_time(self):
        if 'vparte2' in self.request.COOKIES:
            elapsed = datetime.datetime.now() - datetime.datetime.strptime(self.request.COOKIES['vparte2'], '%Y-%m-%d %H:%M:%S')
            self.request.session['parte2_tiempo'] = int(elapsed.total_seconds())
            return self.request.session['parte2_tiempo']
        else:
            return 0

    def get_context_data(self, **kwargs):
        ctx = super(Cuestionario3View, self).get_context_data(**kwargs)
        ctx['parte2_tiempo'] = self.process_elapsed_time()
        return ctx

    def get(self, request, *args, **kwargs):
        response = super(Cuestionario3View, self).get(request, *args, **kwargs)
        if 'vparte2' not in self.request.COOKIES:
            response.set_cookie('vparte2', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1200)
        return response

    def save(self):
        cuestionario = self.request.session.get('cuestionario', dict())
        cuestionario.update(self.request.POST)
        self.request.session['cuestionario'] = cuestionario
        self.request.session['parte2'] = True
        self.process_elapsed_time()
        del self.request.COOKIES['vparte2']
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

    def process_elapsed_time(self):
        if 'vparte3' in self.request.COOKIES:
            elapsed = datetime.datetime.now() - datetime.datetime.strptime(self.request.COOKIES['vparte3'], '%Y-%m-%d %H:%M:%S')
            self.request.session['parte3_tiempo'] = int(elapsed.total_seconds())
            return self.request.session['parte3_tiempo']
        else:
            return 0

    def get_context_data(self, **kwargs):
        ctx = super(Cuestionario4View, self).get_context_data(**kwargs)
        ctx['parte3_tiempo'] = self.process_elapsed_time()
        return ctx

    def get(self, request, *args, **kwargs):
        response = super(Cuestionario4View, self).get(request, *args, **kwargs)
        if 'vparte3' not in self.request.COOKIES:
            response.set_cookie('vparte3', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1200)
        return response

    def post(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps(self.save()), content_type="application/json")
        response.delete_cookie('vparte3')
        return response

    def save(self):
        response = {
            'success': True,
            'error': None,
            'data': 'Todo bien'
        }
        #try:
        id = self.request.user.id or 0
        if not Cuestionario.objects.filter(usuario=id).exists():
            cuestionario = self.request.session.get('cuestionario', dict())
            self.process_elapsed_time()
            del self.request.COOKIES['vparte3']
            cuestionario.update(self.request.POST)
            cuestionario['usuario'] = id
            cuestionario['proyecto'] = self.request.user.proyecto or 'NINGUNO'
            #aqui guardar
            for field, v in cuestionario.items():
                if field.startswith('parte2'):
                    if isinstance(v, list):
                        cuestionario[field] = v[0]
                elif field.startswith('parte3'):
                    if isinstance(v, list):
                        cuestionario[field] = int(v[0])
            cuestionario['parte1_tiempo'] = self.request.session.get('parte1_tiempo')
            cuestionario['parte2_tiempo'] = self.request.session.get('parte2_tiempo')
            cuestionario['parte3_tiempo'] = self.request.session.get('parte3_tiempo')
            form = CuestionarioForm(cuestionario)
            form.save()
            self.request.session['parte3'] = True
            if self.request.session.has_key('cuestionario'):
                del self.request.session['cuestionario']
        else:
            response['data'] = 'Usted ya ha completado el cuestionario'
        #except Exception as e:
        #    response['success'] = False
        #    response['error'] = True
        #    response['data'] = e.message
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
                cuestionario['parte1_tiempo'] = self.request.session.get('parte1_tiempo')
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
        response.delete_cookie('vparte1')
        response.delete_cookie('vparte2')
        response.delete_cookie('vparte3')
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
            filtro['usuario__odei__odei'] = self.request.GET['odei']
        return super(AdminView, self).get_queryset().filter(**filtro)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AdminView, self).dispatch(*args, **kwargs)

    def get_odeis(self):
        return [v[0] for v in Odei.objects.exclude(odei=None).distinct('odei').values_list('odei', 'odei')]


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


class OdeiView(TemplateView):
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(OdeiView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps(self.get_odeis()), content_type="application/json")
        return response

    def get_odeis(self):
        region = self.request.POST['region']
        objects = list(Odei.objects.filter(region_id=region).values('id', 'descripcion').order_by('descripcion'))
        response = {
            'success': True,
            'data': objects,
            'error': False
        }
        return response


class Odei2View(TemplateView):
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(Odei2View, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps(self.get_odeis()), content_type="application/json")
        return response

    def get_odeis(self):
        provincia = self.request.POST['provincia']
        objects = Odei.objects.get(pk=provincia).odei
        response = {
            'success': True,
            'data': objects,
            'error': False
        }
        return response