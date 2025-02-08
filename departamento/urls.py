from django.urls import path
from .views import get_municipios, buscar_municipios, obtener_paises

urlpatterns = [
    # Esta ruta es la que maneja la solicitud AJAX
    path('getMunicipios/<int:departamento_id>/', get_municipios, name='getMunicipios'),
    path('buscar-municipios/', buscar_municipios, name='buscar_municipios'),
    path('obtener_paises/', obtener_paises, name='obtener_paises'),
]