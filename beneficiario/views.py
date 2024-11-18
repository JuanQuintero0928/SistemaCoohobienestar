from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Beneficiario, Mascota

# Create your views here.

class ListarBeneficiarios(ListView):

    def get(self, request, *args, **kwargs):
        template_name = 'base/beneficiario/listarBeneficiariosTodos.html'
        # query = Beneficiario.objects.all()
        # return render(request, template_name, {'query':query})

        # Capturar el valor de búsqueda del formulario
        num_documento = request.GET.get('numDocumento')

        # Consulta para obtener los registros
        query = Beneficiario.objects.select_related(
            'asociado', 'parentesco', 'paisRepatriacion'
        ).all()
        
        # Filtrar por numDocumento si se ingresó algo en el campo de búsqueda
        if num_documento:
            query = query.filter(
                Q(asociado__numDocumento__icontains=num_documento) |
                Q(asociado__apellido__icontains=num_documento) |
                Q(asociado__nombre__icontains=num_documento) |
                Q(nombre__icontains=num_documento) |
                Q(apellido__icontains=num_documento)
                )

        # Configurar el paginador
        paginator = Paginator(query, 10)  # Muestra 10 registros por página
        page_number = request.GET.get('page')  # Obtén el número de página de la URL
        page_obj = paginator.get_page(page_number)  # Obtén la página actual
        
        return render(request, template_name, {'page_obj': page_obj})
    
class ListarMascotas(ListView):

    def get(self, request, *args, **kwargs):
        template_name = 'base/beneficiario/listarMascotasTodos.html'
        # query = Mascota.objects.all()
        # return render(request, template_name, {'query':query})
    
        # Capturar el valor de búsqueda del formulario
        num_documento = request.GET.get('numDocumento')

        # Consulta para obtener los registros
        query = Mascota.objects.select_related(
            'asociado'
        ).all()
        
        # Filtrar por numDocumento si se ingresó algo en el campo de búsqueda
        if num_documento:
            query = query.filter(
                Q(asociado__numDocumento__icontains=num_documento) |
                Q(asociado__nombre__icontains=num_documento) |
                Q(asociado__apellido__icontains=num_documento) |
                Q(nombre__icontains=num_documento)
            )

        # Configurar el paginador
        paginator = Paginator(query, 10)  # Muestra 10 registros por página
        page_number = request.GET.get('page')  # Obtén el número de página de la URL
        page_obj = paginator.get_page(page_number)  # Obtén la página actual
        
        return render(request, template_name, {'page_obj': page_obj})

class Utilidades(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/beneficiario/utilidades.html'
        return render(request, template_name)