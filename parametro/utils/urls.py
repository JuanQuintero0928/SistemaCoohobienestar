from django.urls import path
from django.contrib.auth.decorators import login_required
from .utils import mes_tarifa_info

urlpatterns = [
    path('mes-tarifa-info/<int:pk>/', login_required(mes_tarifa_info), name='mes_tarifa_info'),
]