from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('informacion/', login_required(InformacionHistorico.as_view()), name='informacion'),
    path('historicoPagos/', login_required(VerHistoricoPagos.as_view()), name='historicoPagos'),
    path('asociadoPago/', login_required(VerAsociadoPagos.as_view()), name='asociadoPago'),
    path('crearPagoAsociado/<int:pkAsociado>/<int:vista>', login_required(CrearPagoAsociado.as_view()), name='crearPagoAsociado'),
    path('editarPagoAsociado/<int:pk>/<int:pkAsociado>/<int:vista>', login_required(EditarPago.as_view()), name='editarPagoAsociado'),
    path('modalPago/<int:pkAsociado>/<int:vista>', login_required(ModalPago.as_view()), name='modalPago'),
    path('cargarCVS/', login_required(cargarCSV.as_view()), name='cargarCSV'),
    path('procesarPagos/', login_required(ProcesarPagos.as_view()), name='procesarPagos'),
]