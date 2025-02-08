from django.contrib import admin
from .models import Departamento, Municipio, PaisRepatriacion, Pais

# Register your models here.

admin.site.register(Departamento)
admin.site.register(Municipio)
admin.site.register(PaisRepatriacion)
admin.site.register(Pais)

