from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Municipio, Pais

def get_municipios(request, departamento_id):
    municipios = Municipio.objects.filter(departamento_id=departamento_id).values('id', 'nombre')
    return JsonResponse(list(municipios), safe=False)

@csrf_exempt
def buscar_municipios(request):
    search = request.GET.get('q', '').strip()  # Captura el término de búsqueda
    municipios = Municipio.objects.filter(
        Q(nombre__icontains=search) | Q(departamento__nombre__icontains=search)
    ).values('id', 'nombre', 'departamento__nombre')[:20]  # Máximo 20 resultados

    return JsonResponse(list(municipios), safe=False)

def obtener_paises(request):
    paises = Pais.objects.values('id','nombre', 'indicativo', 'bandera')
    return JsonResponse(list(paises), safe=False)