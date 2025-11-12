from django.shortcuts import render
from django.conf.urls import handler404
from django.conf import settings
from django.views.generic import ListView
from asociado.models import Asociado

# Create your views here.


class Dashboard(ListView):
    def get(self, request, *args, **kwargs):
        template_name = "index.html"
        query = Asociado.objects.all().count()
        queryActivos = Asociado.objects.filter(estadoAsociado="ACTIVO").count()
        queryInactivos = Asociado.objects.filter(estadoAsociado="INACTIVO").count()
        queryRetirados = Asociado.objects.filter(estadoAsociado="RETIRO").count()

        return render(
            request,
            template_name,
            {
                "total": query,
                "activos": queryActivos,
                "inactivos": queryInactivos,
                "retirado": queryRetirados,
            },
        )


class Informacion(ListView):
    def get(self, request, *args, **kwargs):
        template_name = "base/informacion.html"
        return render(request, template_name)


# Definir el handler para el error 404
def custom_page_not_found_view(request, exception):
    return render(request, "404.html", {}, status=404)


# Asigna el handler404 a la vista personalizada
handler404 = custom_page_not_found_view


def csrf_failure(request, reason=""):
    return render(request, '403_csrf.html', status=403)