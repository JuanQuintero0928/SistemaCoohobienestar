from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    # path('listarProductos/', login_required(ListarProductos.as_view()), name='listarProductos'),

]