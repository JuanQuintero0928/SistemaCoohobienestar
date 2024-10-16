from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('', login_required(Informacion.as_view()), name='informacion'),
    path('health/', health_check, name='health_check'),
]