from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(HistoricoAuxilio)
admin.site.register(HistoricoCredito)
admin.site.register(HistorialPagos)
admin.site.register(HistoricoSeguroVida)

