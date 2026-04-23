from django.urls import reverse_lazy
from django.utils.timezone import now
from django.utils.crypto import get_random_string
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from usuarios.utils import generar_y_enviar_codigo_otp
from usuarios.models import LoginBlockLog
from usuarios.backends import RateLimitExceeded


class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()

        if user.is_associate:
            messages.error(
                self.request, "No tiene permisos para acceder a esta plataforma."
            )
            return redirect("login")

        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrectos.")
        return super().form_invalid(form)
    
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except RateLimitExceeded as e:
            from django.contrib.auth.forms import AuthenticationForm
            messages.error(request, str(e))
            form = AuthenticationForm(request)
            return render(request, self.template_name, {'form': form})


class FormRegistro(TemplateView):
    template_name = "registration/registro.html"


class VerificacionCuenta(TemplateView):
    template_name = "registration/verificacionCodigo.html"


class CustomLoginViewAsociado(LoginView):
    def form_valid(self, form):
        user = form.get_user()

        if user.is_staff:
            messages.error(
                self.request,
                "No tiene permisos para acceder a esta plataforma.",
            )
            return redirect("usuarios:login")
        
        if user.verification_code:
            messages.info(
                self.request,
                "Por favor, verifica tu cuenta antes de iniciar sesión.",
            )
            return redirect(f'/accounts/verificacionCuenta/?email={user.username}')

        # Si todo es correcto, iniciar sesión
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrectos.")
        return super().form_invalid(form)

    def get_success_url(self):
        if self.request.user.is_associate:
            return reverse_lazy("perfil:inicio")


@login_required
def unlock_login_view(request, token):
    """Vista para desbloquear un usuario/IP bloqueado por rate limiting"""
    block_log = get_object_or_404(LoginBlockLog, unlock_token=token, is_active=True)
    
    if request.method == 'POST':
        from django.utils import timezone
        
        # Desbloquear en cache
        cache.delete(f'ratelimit-admin-{block_log.ip_address}-ip')
        if block_log.username:
            cache.delete(f'ratelimit-admin-{block_log.ip_address}-user:{block_log.username}')
        
        # Actualizar registro
        block_log.unlocked_by = request.user
        block_log.unlocked_at = timezone.now()
        block_log.is_active = False
        block_log.save()
        
        messages.success(request, f'Bloqueo desbloqueado exitosamente para {block_log.username or block_log.ip_address}')
        return redirect('admin:usuarios_loginblocklog_changelist')
    
    return render(request, 'registration/unlock_confirmation.html', {'block_log': block_log})
