from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('historicoPagos/', login_required(VerHistoricoPagos.as_view()), name='historicoPagos'),
    path('asociadoPago/', login_required(VerAsociadoPagos.as_view()), name='asociadoPago'),
    path('crearPagoAsociado/<int:pkAsociado>', login_required(CrearPagoAsociado.as_view()), name='crearPagoAsociado'),
    path('editarPagoAsociado/<int:pk>/<int:pkAsociado>', login_required(EditarPago.as_view()), name='editarPagoAsociado'),
    
]