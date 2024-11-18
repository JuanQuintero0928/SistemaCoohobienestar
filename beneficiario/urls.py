from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('beneficiario/', login_required(ListarBeneficiarios.as_view()), name='beneficiario'),
    path('mascota/', login_required(ListarMascotas.as_view()), name='mascota'),
    path('utilidades/', login_required(Utilidades.as_view()), name='utilidades'),
]