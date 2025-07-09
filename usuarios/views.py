from django.urls import reverse_lazy
from django.utils.timezone import now
from django.utils.crypto import get_random_string
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
from usuarios.utils import generar_y_enviar_codigo_otp


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
