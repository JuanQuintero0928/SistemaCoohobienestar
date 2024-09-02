from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Beneficiario, Mascota

# Create your views here.

class ListarBeneficiarios(ListView):

    def get(self, request, *args, **kwargs):
        template_name = 'base/beneficiario/listarBeneficiariosTodos.html'
        query = Beneficiario.objects.all()
        return render(request, template_name, {'query':query})
    
class ListarMascotas(ListView):

    def get(self, request, *args, **kwargs):
        template_name = 'base/beneficiario/listarMascotasTodos.html'
        query = Mascota.objects.all()
        return render(request, template_name, {'query':query})

