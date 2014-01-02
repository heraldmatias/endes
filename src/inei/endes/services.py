__author__ = 'holivares'

import csv
from django.http import HttpResponse
from django.template import loader, Context

def response_csv(objects, filename):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % filename

    writer = csv.writer(response)
    writer.writerow(['Usuario', 'Estado1', 'Estado2', 'Estado3'])
    for object in objects:
        writer.writerow([object.usuario, object.get_estado1(), object.get_estado2().replace('<br>', ''), object.get_estado3()])

    # t = loader.get_template('reporte.txt')
    # c = Context({
    #     'data': objects,
    # })
    # response.write(t.render(c))
    return response