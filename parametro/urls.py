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
    path('mesTarifa/', login_required(ListarMesTarifa.as_view()), name='mesTarifa'),
    path('convenio/', login_required(ListarConvenio.as_view()), name='convenio'),
    path('tasasInteresCredito/', login_required(ListarTasasInteresCredito.as_view()), name='tasasInteresCredito'),
    path('crearPaisR/', login_required(CrearPaisRepatriacion.as_view()), name='crearPaisR'),
    path('editarPaisR/<int:pk>', login_required(EditarPaisRepatriacion.as_view()), name='editarPaisR'),
    path('crearParentesco/', login_required(CrearParentesco.as_view()), name='crearParentesco'),
    path('editarParentesco/<int:pk>', login_required(EditarParentesco.as_view()), name='editarParentesco'),
    path('editarTarifa/<int:pk>', login_required(EditarTarifa.as_view()), name='editarTarifa'),
    path('crearTipoAsociado/', login_required(CrearTipoAsociado.as_view()), name='crearTipoAsociado'),
    path('editarTipoAsociado/<int:pk>', login_required(EditarTipoAsociado.as_view()), name='editarTipoAsociado'),
    path('editarTipoAuxilio/<int:pk>', login_required(EditarTipoAuxilio.as_view()), name='editarTipoAuxilio'),
    path('crearPaisIndicativo/', login_required(CrearIndicativoCelular.as_view()), name='crearPaisIndicativo'),
    path('editarPaisIndicativo/<int:pk>', login_required(EditarIndicativoCelular.as_view()), name='editarPaisIndicativo'),
    path('crearMesTarifa/', login_required(CrearMesTarifa.as_view()), name='crearMesTarifa'),
    path('editarMesTarifa/<int:pk>', login_required(EditarMesTarifa.as_view()), name='editarMesTarifa'),
    path('crearConvenio/', login_required(CrearConvenio.as_view()), name='crearConvenio'),
    path('editarConvenio/<int:pk>', login_required(EditarConvenio.as_view()), name='editarConvenio'),
    path('crearTasaInteresCredito/', login_required(CrearTasasInteresCredito.as_view()), name='crearTasaInteresCredito'),
    path('editarTasaInteresCredito/<int:pk>', login_required(EditarTasasInteresCredito.as_view()), name='editarTasaInteresCredito'),

]