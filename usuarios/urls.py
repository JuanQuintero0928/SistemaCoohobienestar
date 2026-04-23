from django.urls import path
from .views import CustomLoginViewAsociado, FormRegistro, VerificacionCuenta, unlock_login_view

urlpatterns = [
    path('crearCuenta/', FormRegistro.as_view(), name='crearCuenta'),
    path('verificacionCuenta/', VerificacionCuenta.as_view(), name='verificacionCuenta'),
    path('loginAsociado/', CustomLoginViewAsociado.as_view(template_name='registration/loginAsociado.html'), name='login'),
    path('unlock/<str:token>/', unlock_login_view, name='unlock_login'),
]