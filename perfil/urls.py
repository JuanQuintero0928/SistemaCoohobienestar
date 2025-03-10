from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('', login_required(Inicio.as_view()), name='inicio'),
    path('informacionPersonal/', login_required(InformacionPersonal.as_view()), name='informacionPersonal'),
    path('pagos/', login_required(ListarPagos.as_view()), name='pagos'),
    path('beneficiarios/', login_required(ListarBeneficiarios.as_view()), name='beneficiarios'),
]