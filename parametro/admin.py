from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(TipoAuxilio)
admin.site.register(Tarifas)
admin.site.register(MesTarifa)
admin.site.register(FormaPago)
admin.site.register(TipoAsociado)

