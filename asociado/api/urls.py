from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import obtener_total_tarifa, obtener_datos_formato_registro, obtener_datos_servicios_exequiales, obtener_datos_auxilio_economico

urlpatterns = [
    path('obtener_total_tarifa/<int:pkAsociado>/', login_required(obtener_total_tarifa), name='obtener_total_tarifa'),
    path('obtener_datos_formato_registro/<int:asociado_id>/<str:tipo_formato>/', login_required(obtener_datos_formato_registro), name='obtener_datos_formato_registro'),
    path('obtener_datos_servicios_exequiales/<int:asociado_id>/<str:tipo_formato>/', login_required(obtener_datos_servicios_exequiales), name='obtener_datos_servicios_exequiales'),
    path('obtener_datos_auxilio_economico/<int:asociado_id>/<str:tipo_formato>/<int:auxilio_id>/', login_required(obtener_datos_auxilio_economico), name='obtener_datos_auxilio_economico'),

]