from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from .models import Tarifas, TipoAuxilio, TipoAsociado
from .forms import PaisRepatriacionForm
from departamento.models import PaisRepatriacion
from beneficiario.models import Parentesco 

# Create your views here.

class Parametro(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'parametro/parametros.html'
        return render(request, template_name)

class ListarTipoAuxilio(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'parametro/listarTipoAuxilio.html'
        query = TipoAuxilio.objects.all()
        return render(request, template_name,{'query':query, 'vista':1})

class ListarTarifa(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'parametro/listarTarifas.html'
        query = Tarifas.objects.all()
        return render(request, template_name,{'query':query, 'vista':2})

class ListarPaises(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'parametro/listarPaises.html'
        query = PaisRepatriacion.objects.all()
        return render(request, template_name,{'query':query, 'vista':3})

class ListarParentesco(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'parametro/listarParentesco.html'
        query = Parentesco.objects.all()
        return render(request, template_name,{'query':query, 'vista':4})
    
class ListarTipoAsociado(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'parametro/listarTipoAsociado.html'
        query = TipoAsociado.objects.all()
        return render(request, template_name,{'query':query, 'vista':5})

class CrearPaisRepatriacion(CreateView, SuccessMessageMixin):
    model = PaisRepatriacion
    form_class = PaisRepatriacionForm
    template_name = 'parametro/crear.html'
    success_url = reverse_lazy('parametro:pais')
    success_message = "Creado exitosamente"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)  # Asegurar que se envía el mensaje
        return response

class EditarPaisRepatriacion(UpdateView):
    model = PaisRepatriacion
    form_class = PaisRepatriacionForm
    template_name = 'parametro/crear.html'
    success_url = reverse_lazy('parametro:pais')
    success_message = "Editado exitosamente"