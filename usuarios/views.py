
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages

class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()

        if user.is_associate:
            messages.error(self.request, 'No tiene permisos para acceder a esta plataforma.')
            return redirect('login')

        login(self.request, user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña incorrectos.')
        return super().form_invalid(form)

class FormRegistro(TemplateView):
    template_name = 'registration/registro.html'

class VerificacionCuenta(TemplateView):
    template_name = 'registration/verificacionCodigo.html'

class CustomLoginViewAsociado(LoginView):
    def form_valid(self, form):
        user = form.get_user()

        if user.is_associate == False or user.is_active == False:
            messages.error(self.request, 'No tiene permisos para acceder a esta plataforma.')
            return redirect('loginAsociado')
        
        login(self.request, user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña incorrectos.')
        return super().form_invalid(form)
    
    def get_success_url(self):
        if self.request.user.is_associate:
            return reverse_lazy('perfil:inicio')