from django.urls import path
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import path
from .views import *

# Función para manejar el chequeo de salud
def health_check(request):
    return JsonResponse({'status': 'healthy'})

urlpatterns = [
    path('', login_required(Informacion.as_view()), name='informacion'),
    path('health/', health_check, name='health_check'),
]