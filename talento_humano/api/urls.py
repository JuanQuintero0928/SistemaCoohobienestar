from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import obtener_datos_certificado_laboral

urlpatterns = [
    path(
        "obtener_datos_certificado_laboral/<int:empleado_id>/<str:tipo_formato>/",
        login_required(obtener_datos_certificado_laboral),
        name="obtener_datos_certificado_laboral",
    ),
]
