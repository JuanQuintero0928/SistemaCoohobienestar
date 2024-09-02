from django.contrib import admin
from .models import Departamento, Municipio, PaisRepatriacion

# Register your models here.

admin.site.register(Departamento)
admin.site.register(Municipio)
admin.site.register(PaisRepatriacion)

