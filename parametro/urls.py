from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('parametro/', login_required(Parametro.as_view()), name='parametro'),
    path('tipoAuxilio/', login_required(ListarTipoAuxilio.as_view()), name='tipoAuxilio'),
    path('tarifa/', login_required(ListarTarifa.as_view()), name='tarifa'),
    path('pais/', login_required(ListarPaises.as_view()), name='pais'),
    path('paisIndicativo/', login_required(ListarIndicativoCelular.as_view()), name='paisIndicativo'),
    path('parentesco/', login_required(ListarParentesco.as_view()), name='parentesco'),
    path('tipoAsociado/', login_required(ListarTipoAsociado.as_view()), name='tipoAsociado'),
    path('crearPaisR/', login_required(CrearPaisRepatriacion.as_view()), name='crearPaisR'),
    path('editarPaisR/<int:pk>', login_required(EditarPaisRepatriacion.as_view()), name='editarPaisR'),
    path('crearParentesco/', login_required(CrearParentesco.as_view()), name='crearParentesco'),
    path('editarParentesco/<int:pk>', login_required(EditarParentesco.as_view()), name='editarParentesco'),
    path('editarTarifa/<int:pk>', login_required(EditarTarifa.as_view()), name='editarTarifa'),
    path('crearTipoAsociado/', login_required(CrearTipoAsociado.as_view()), name='crearTipoAsociado'),
    path('editarTipoAsociado/<int:pk>', login_required(EditarTipoAsociado.as_view()), name='editarTipoAsociado'),
    path('editarTipoAuxilio/<int:pk>', login_required(EditarTipoAuxilio.as_view()), name='editarTipoAuxilio'),
    path('crearPaisIndicativo/', login_required(CrearIndicativoCelular.as_view()), name='crearPaisIndicativo'),

]