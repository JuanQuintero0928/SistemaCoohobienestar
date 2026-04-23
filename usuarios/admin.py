from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from .models import UsuarioAsociado, LoginBlockLog
from asociado.models import Asociado

class UsuarioAsociadoAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_associate')
    fieldsets = UserAdmin.fieldsets + (
        ('Información de Asociado', {'fields': ('is_associate', 'asociado')}),
    )

@admin.register(LoginBlockLog)
class LoginBlockLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'username', 'blocked_at', 'blocked_until', 'attempts_count', 'status_badge', 'unlock_button')
    list_filter = ('blocked_at', 'reason')
    search_fields = ('ip_address', 'username')
    readonly_fields = ('blocked_at', 'ip_address', 'username', 'unlock_token', 'attempts_count')
    ordering = ['-blocked_at']
    actions = ['unblock_selected']
    
    def status_badge(self, obj):
        if obj.unlocked_at:
            return format_html('<span style="color: green;">✓ Desbloqueado</span>')
        elif obj.is_expired:
            return format_html('<span style="color: orange;">Expirado</span>')
        else:
            return format_html('<span style="color: red;">Bloqueado ({} min)</span>', obj.remaining_minutes)
    status_badge.short_description = 'Estado'
    
    def unlock_button(self, obj):
        if not obj.unlocked_at and not obj.is_expired:
            url = reverse('usuarios:unlock_login', args=[obj.unlock_token])
            return format_html('<a class="button" href="{}" style="background: #dc3545; color: white; padding: 5px 10px; border-radius: 3px; text-decoration: none;">Desbloquear</a>', url)
        return '-'
    unlock_button.short_description = 'Acción'
    
    def unblock_selected(self, request, queryset):
        from django.utils import timezone
        count = 0
        for obj in queryset.filter(unlocked_at__isnull=True):
            obj.unlocked_at = timezone.now()
            obj.unlocked_by = request.user
            obj.is_active = False
            obj.save()
            count += 1
        self.message_user(request, f'{count} bloqueos han sido desbloqueados.')
    unblock_selected.short_description = 'Desbloquear seleccionados'