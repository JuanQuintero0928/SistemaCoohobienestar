from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('verModificacionesPorFecha/', login_required(VerModificacionesFecha.as_view()), name='verModificacionesPorFecha'),
    path('generarModXFechaExcel/', login_required(ReporteExcelFecha.as_view()), name='generarModXFechaExcel'),
    path('verPagosPorFecha/', login_required(VerPagosFecha.as_view()), name='verPagosPorFecha'),
    path('generarPagoExcel/', login_required(ReporteExcelPago.as_view()), name='generarPagoExcel'),

]