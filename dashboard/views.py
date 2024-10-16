from django.shortcuts import render
from django.views.generic import ListView
from asociado.models import Asociado
from django.http import HttpResponse

# Create your views here.

def health_check(request):
    return HttpResponse("OK", status=200)

class Dashboard(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'index.html'
        query = Asociado.objects.all().count()
        queryActivos = Asociado.objects.filter(estadoAsociado = 'ACTIVO').count()
        queryInactivos = Asociado.objects.filter(estadoAsociado = 'INACTIVO').count()
        queryRetirados = Asociado.objects.filter(estadoAsociado = 'RETIRO').count()
    
        return render(request, template_name, {'total':query, 'activos':queryActivos, 'inactivos':queryInactivos, 'retirado':queryRetirados})
       
class Informacion(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/informacion.html'
        return render(request, template_name)