from django.urls import path
from .views import CustomLoginViewAsociado, FormRegistro, VerificacionCuenta

urlpatterns = [
    path('crearCuenta/', FormRegistro.as_view(), name='crearCuenta'),
    path('verificacionCuenta/', VerificacionCuenta.as_view(), name='verificacionCuenta'),
    path('loginAsociado/', CustomLoginViewAsociado.as_view(template_name='registration/loginAsociado.html'), name='login'),
]