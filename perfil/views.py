from django.shortcuts import render
from django.views.generic import TemplateView, ListView
import asociado
from asociado.models import Asociado
from departamento.models import PaisRepatriacion
from historico.models import HistorialPagos
from beneficiario.models import Beneficiario, Mascota

# Create your views here.

class Inicio(TemplateView):
    template_name = 'perfil/inicio.html'

class InformacionPersonal(ListView):
    template_name = 'perfil/informacionPersonal.html'
    model = Asociado
    context_object_name = 'query'

    def get_queryset(self):
        return Asociado.objects.get(pk=self.request.user.asociado.pk)
    
class ListarPagos(ListView):
    template_name = 'perfil/listarPagos.html'
    model = HistorialPagos
    context_object_name = 'query'

    def get_queryset(self):
        return HistorialPagos.objects.filter(asociado=self.request.user.asociado.pk)
    
class ListarBeneficiarios(ListView):
    template_name = 'perfil/listarBeneficiarios.html'
    model = Beneficiario
    context_object_name = 'query'

    def get_queryset(self):
        return Beneficiario.objects.filter(asociado=self.request.user.asociado.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['queryMascota'] = Mascota.objects.filter(asociado=self.request.user.asociado.pk, estadoRegistro=True)
        context['repatriacion'] = Beneficiario.objects.filter(asociado=self.request.user.asociado.pk, paisRepatriacion__isnull = False, estadoRegistro=True).exists()
        return context