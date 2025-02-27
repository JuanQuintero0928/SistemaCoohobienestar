from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from .models import Tarifas, TipoAuxilio, TipoAsociado, MesTarifa, Convenio, TasasInteresCredito
from .forms import *
from departamento.models import PaisRepatriacion, Pais
from beneficiario.models import Parentesco 
# Create your views here.

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
    
class Parametro(StaffRequiredMixin, TemplateView):
    template_name = 'parametro/parametros.html'
    
class ListarTipoAuxilio(StaffRequiredMixin, ListView):
    template_name = 'parametro/listarTipoAuxilio.html'
    model = TipoAuxilio
    context_object_name = 'query'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'vista': 1,
        })
        return context

class ListarTarifa(StaffRequiredMixin, ListView):
    template_name = 'parametro/listarTarifas.html'
    model = Tarifas
    context_object_name = 'query'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'vista': 2,
        })
        return context
    
class ListarPaises(StaffRequiredMixin, ListView):
    template_name = 'parametro/listarPaises.html'
    model = PaisRepatriacion
    context_object_name = 'query'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'vista': 3,
        })
        return context

class ListarParentesco(StaffRequiredMixin,ListView):
    template_name = 'parametro/listarParentesco.html'
    model = Parentesco
    context_object_name = 'query'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'vista': 4,
        })
        return context
    
class ListarTipoAsociado(StaffRequiredMixin,ListView):
    template_name = 'parametro/listarTipoAsociado.html'
    model = TipoAsociado
    context_object_name = 'query'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'vista': 5,
        })
        return context

class ListarIndicativoCelular(StaffRequiredMixin, ListView):
    template_name = 'parametro/listarPaisIndicativo.html'
    model = Pais
    context_object_name = 'query'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'vista': 6,
        })
        return context

class ListarMesTarifa(StaffRequiredMixin, ListView):
    template_name = 'parametro/listarMesTarifa.html'
    model = MesTarifa
    context_object_name = 'query'

    def get_queryset(self):
        return MesTarifa.objects.filter(pk__lt = 9000)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'vista': 7,
        })
        return context

class ListarConvenio(StaffRequiredMixin, ListView):
    template_name = 'parametro/listarConvenio.html'
    model = Convenio
    context_object_name = 'query'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vista'] = 8
        return context

class ListarTasasInteresCredito(StaffRequiredMixin, ListView):
    template_name = 'parametro/listarTasaInteresCredito.html'
    model = TasasInteresCredito
    context_object_name = 'query'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vista'] = 9
        return context

class CrearPaisRepatriacion(StaffRequiredMixin, CreateView, SuccessMessageMixin):
    model = PaisRepatriacion
    form_class = PaisRepatriacionForm
    template_name = 'parametro/formulario.html'
    success_url = reverse_lazy('parametro:pais')
    success_message = "Creado exitosamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'operation': 'paisR',
        })
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

class EditarPaisRepatriacion(StaffRequiredMixin, UpdateView):
    model = PaisRepatriacion
    form_class = PaisRepatriacionForm
    template_name = 'parametro/formulario.html'
    success_url = reverse_lazy('parametro:pais')
    success_message = "Editado exitosamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'operation': 'paisR',
        })
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
class CrearParentesco(StaffRequiredMixin,CreateView, SuccessMessageMixin):
    model = Parentesco
    form_class = ParentescoForm
    template_name = 'parametro/formulario.html'
    success_url = reverse_lazy('parametro:parentesco')
    success_message = "Creado exitosamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'operation': 'parentesco',
        })
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

class EditarParentesco(StaffRequiredMixin, UpdateView):
    model = Parentesco
    form_class = ParentescoForm
    template_name = 'parametro/formulario.html'
    success_url = reverse_lazy('parametro:parentesco')
    success_message = "Editado exitosamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'operation': 'parentesco',
        })
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

class EditarTarifa(StaffRequiredMixin, UpdateView):
    model = Tarifas
    form_class = TarifasForm
    template_name = 'parametro/formulario.html'
    success_url = reverse_lazy('parametro:tarifa')
    success_message = "Editado exitosamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'operation': 'tarifa',
        })
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

class CrearTipoAsociado(StaffRequiredMixin, CreateView, SuccessMessageMixin):
    model = TipoAsociado
    form_class = TipoAsociadoForm
    template_name = 'parametro/formulario.html'
    success_url = reverse_lazy('parametro:tipoAsociado')
    success_message = "Creado exitosamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'operation': 'tipoAsociado',
        })
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

class EditarTipoAsociado(StaffRequiredMixin, UpdateView):
    model = TipoAsociado
    form_class = TipoAsociadoForm
    template_name = 'parametro/formulario.html'
    success_url = reverse_lazy('parametro:tipoAsociado')
    success_message = "Editado exitosamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'operation': 'tipoAsociado',
        })
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

class EditarTipoAuxilio(StaffRequiredMixin, UpdateView):
    model = TipoAuxilio
    form_class = TipoAuxilioForm
    template_name = 'parametro/formulario.html'
    success_url = reverse_lazy('parametro:tipoAuxilio')
    success_message = "Editado exitosamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'operation': 'tipoAuxilio',
        })
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

class CrearIndicativoCelular(StaffRequiredMixin, CreateView, SuccessMessageMixin):
    model = Pais
    form_class = PaisForm
    template_name = 'parametro/formulario.html'
    success_url = reverse_lazy('parametro:paisIndicativo')
    success_message = "Editado exitosamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'operation': 'paisIndicativo',
        })
        return context

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            messages.success(self.request, self.success_message)
            return JsonResponse({'success': True})
        return response
    
class EditarIndicativoCelular(StaffRequiredMixin, UpdateView, SuccessMessageMixin):
    model = Pais
    form_class = PaisForm
    template_name = 'parametro/formulario.html'
    success_url = reverse_lazy('parametro:paisIndicativo')
    success_message = "Editado exitosamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = 'paisIndicativo'
        return context
    
    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            messages.success(self.request, self.success_message)
            return JsonResponse({'success': True})
        return response

class CrearMesTarifa(StaffRequiredMixin, CreateView, SuccessMessageMixin):
    model = MesTarifa
    form_class = MesTarifaForm
    template_name = 'parametro/formulario.html'
    success_url = reverse_lazy('parametro:mesTarifa')
    success_message = "Creado exitosamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = 'mesTarifa'
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    
class EditarMesTarifa(StaffRequiredMixin, UpdateView):
    model = MesTarifa
    form_class = MesTarifaForm
    template_name = 'parametro/formulario.html'
    success_url = reverse_lazy('parametro:mesTarifa')
    success_message = "Editado exitosamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'operation': 'mesTarifa',
        })
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

class CrearConvenio(StaffRequiredMixin, CreateView, SuccessMessageMixin):
    model = Convenio
    form_class = ConvenioForm
    template_name = 'parametro/formulario.html'
    success_url = reverse_lazy('parametro:convenio')
    success_message = "Creado exitosamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = 'convenio'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    
class EditarConvenio(StaffRequiredMixin, UpdateView):
    model = Convenio
    form_class = ConvenioForm
    template_name = 'parametro/formulario.html'
    success_url = reverse_lazy('parametro:convenio')
    success_message = "Editado exitosamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = 'convenio'
        return context
    
    def form_valid(self, form):
        if form.instance.fechaTerminacion:
            form.instance.estado = False
        else:
            form.instance.estado = True
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    
class CrearTasasInteresCredito(StaffRequiredMixin, CreateView, SuccessMessageMixin):
    model = TasasInteresCredito
    form_class = TasasInteresCreditoForm
    template_name = 'parametro/formulario.html'
    success_url = reverse_lazy('parametro:tasasInteresCredito')
    success_message = "Creado exitosamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = 'tasasInteresCredito'
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

class EditarTasasInteresCredito(StaffRequiredMixin, UpdateView):
    model = TasasInteresCredito
    form_class = TasasInteresCreditoForm
    template_name = 'parametro/formulario.html'
    success_url = reverse_lazy('parametro:tasasInteresCredito')
    success_message = "Editado exitosamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = 'tasasInteresCredito'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    