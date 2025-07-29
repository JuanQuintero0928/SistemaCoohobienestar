from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('informacion/', login_required(InformacionHistorico.as_view()), name='informacion'),
    path('historicoPagos/', login_required(VerHistoricoPagos.as_view()), name='historicoPagos'),
    path('asociadoPago/', login_required(VerAsociadoPagos.as_view()), name='asociadoPago'),
    path('editarPagoAsociado/<int:pk>/<int:pkAsociado>/<int:vista>', login_required(EditarPago.as_view()), name='editarPagoAsociado'),
    path('modalPago/<int:pkAsociado>/<int:vista>', login_required(ModalPago.as_view()), name='modalPago'),
    path('modalPagoVentas/<int:pkVenta>/<int:pkAsociado>/<str:tipo>/', login_required(modal_pago_ventas), name='modalPagoVenta'),
    path('cargarCVS/', login_required(cargarCSV.as_view()), name='cargarCSV'),
    path('eliminarPago/<int:pk>/<int:pkAsociado>/<int:vista>', login_required(EliminarPago.as_view()), name='eliminarPago'),
    path('actualizarEstadoAsoc/', login_required(ActualizarEstadoAsoc.as_view()), name='actualizarEstadoAsoc'),
    path("actualizarEstadoMasivo/", actualizarEstadoMasivo, name="actualizarEstadoMasivo"),
    path("comprobantePago/<int:pk>", login_required(ComprobantePago.as_view()), name="comprobantePago"),
    path('actualizar_pago/<int:pk>/<int:tipo>/', actualizar_pago, name='actualizar_pago'),
    path('eliminar_pago/<int:pk>/<int:tipo>/', eliminar_pago, name='eliminar_pago'),
]