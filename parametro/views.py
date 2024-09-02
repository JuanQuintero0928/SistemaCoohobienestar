from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Tarifas, TipoAuxilio, TipoAsociado
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
        return render(request, template_name,{'query':query, 'tipoAuxilio':'yes'})

class ListarTarifa(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'parametro/listarTarifas.html'
        query = Tarifas.objects.all()
        return render(request, template_name,{'query':query})

class ListarPaises(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'parametro/listarPaises.html'
        query = PaisRepatriacion.objects.all()
        return render(request, template_name,{'query':query})

class ListarParentesco(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'parametro/listarParentesco.html'
        query = Parentesco.objects.all()
        return render(request, template_name,{'query':query})
    
class ListarTipoAsociado(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'parametro/listarTipoAsociado.html'
        query = TipoAsociado.objects.all()
        return render(request, template_name,{'query':query})
