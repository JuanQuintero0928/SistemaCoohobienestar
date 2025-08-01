from django.urls import path
from usuarios.api.views import RegistroAsociadoView, VerificarCodigoView, ReenviarCodigoView

urlpatterns = [
    path('registro-asociado/', RegistroAsociadoView.as_view(), name='registro-asociado'),
    path('verificar-codigo/', VerificarCodigoView.as_view(), name='verificar-codigo'),
    path('reenviar-codigo/', ReenviarCodigoView.as_view(), name='reenviar-codigo'),
]