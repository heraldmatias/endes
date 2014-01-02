from django.http import HttpResponseRedirect

__author__ = 'holivares'
from inei.endes.models import Cuestionario


class CuestionarioMiddleware(object):
    def process_request(self, request):
        id = self.request.user.id or 0
        if Cuestionario.objects.filter(usuario=id).exists():
            return HttpResponseRedirect('/agradecimiento/')
        if self.request.session.has_key('parte1'):
            if not self.request.session.has_key('parte2'):
                return HttpResponseRedirect('/cuestionario/3/')

    def process_response(self, request, response):
        """
        If request.session was modified, or if the configuration is to save the
        session every time, save the changes and set a session cookie.
        """

        return response
