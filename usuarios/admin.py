from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioAsociado
from asociado.models import Asociado

class UsuarioAsociadoAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_associate')
    fieldsets = UserAdmin.fieldsets + (
        ('Información de Asociado', {'fields': ('is_associate', 'asociado')}),
    )

admin.site.register(UsuarioAsociado, UsuarioAsociadoAdmin)