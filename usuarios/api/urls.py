from django.urls import path
from usuarios.api.views import RegistroAsociadoView, VerificarCodigoView

urlpatterns = [
    path('registro-asociado/', RegistroAsociadoView.as_view(), name='registro-asociado'),
    path('verificar-codigo/', VerificarCodigoView.as_view(), name='verificar-codigo'),
]