from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('informacionReporte/', login_required(InformacionReporte.as_view()), name='informacionReporte'),
    path('verModificacionesPorFecha/', login_required(VerModificacionesFecha.as_view()), name='verModificacionesPorFecha'),
    path('generarModXFechaExcel/', login_required(ReporteExcelFecha.as_view()), name='generarModXFechaExcel'),
    path('verPagosPorFecha/', login_required(VerPagosFecha.as_view()), name='verPagosPorFecha'),
    path('generarPagoExcel/', login_required(ReporteExcelPago.as_view()), name='generarPagoExcel'),
    path('formatoExtracto/', login_required(FormatoExtracto.as_view()), name='formatoExtracto'),
    path('descuentosNomina/', login_required(VerDescuentosNomina.as_view()), name='descuentosNomina'),
    path('excelDescuentosNomina/', login_required(ExcelDescuentosNomina.as_view()), name='excelDescuentosNomina'),
    path('verConciliacionBancaria/', login_required(VerConciliacionBancaria.as_view()), name='verConciliacionBancaria'),
    path('excelConciliacionBancaria/', login_required(ExcelConciliacionBancaria.as_view()), name='excelConciliacionBancaria'),
]