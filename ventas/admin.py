from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(PorcentajeDescuento)
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(HistoricoVenta)
admin.site.register(DetalleVenta)
