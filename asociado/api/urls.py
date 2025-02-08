from django.urls import path
from .views import obtener_total_tarifa

urlpatterns = [
    path('obtener_total_tarifa/<int:pkAsociado>/', obtener_total_tarifa, name='obtener_total_tarifa'),
]