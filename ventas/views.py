from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory

from .models import Producto, HistoricoVenta, DetalleVenta
from .form import ProductoForm, HistoricoVentaForm, DetalleVentaForm
from asociado.models import Asociado

# Create your views here.

class ListarProductos(ListView):
    model = Producto
    template_name = 'ventas/listarProductos.html'
    context_object_name = 'query'
    
    def get_queryset(self):
        return Producto.objects.select_related('categoria')

class CrearProducto(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'ventas/crearProducto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # se agrega parametros al contexto para identificar la operación
        context['operation'] = 'crear'
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            producto = form.save(commit=False)
            # Asignar valores manualmente
            producto.nombre = producto.nombre.upper()
            producto.inventario = True
            producto.estadoRegistro = True
            producto.save()
            messages.info(request, f"Producto creado correctamente.")
            return HttpResponseRedirect(reverse_lazy('asociado:listarProductos'))
        # Renderizar el formulario con errores si es inválido
        return render(
            request,
            self.template_name,
            {'form': form, 'errors': form.errors},
            status=400
        )

class EditarProducto(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'ventas/crearProducto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # se agrega parametros al contexto para identificar la operación
        context['operation'] = 'editar'
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            producto = form.save(commit=False)
            # Asignar valores manualmente antes de guardar
            producto.inventario = True
            producto.estadoRegistro = True
            producto.save()
            messages.info(request, f"Producto modificado correctamente.")
            return HttpResponseRedirect(reverse_lazy('asociado:listarProductos'))
        # Renderizar el formulario con errores si es inválido
        return render(
            request,
            self.template_name,
            {'form': form, 'errors': form.errors},
            status=400
        )
    
class ListarVentasAsociado(ListView):
    model = HistoricoVenta
    template_name = 'base/ventas/listarVentasAsociado.html'
    context_object_name = 'ventas'

    def get_queryset(self):
        return HistoricoVenta.objects.filter(asociado = self.kwargs['pkAsociado'],estadoRegistro=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'pkAsociado': self.kwargs['pkAsociado'],
            'vista': 11
        })
    
        if self.request.POST:
            context['detalle_venta_formset'] = inlineformset_factory(
                HistoricoVenta,
                DetalleVenta,
                form=DetalleVentaForm,
                extra=1,
                can_delete=True
            )(self.request.POST)
        else:
            context['detalle_venta_formset'] = inlineformset_factory(
                HistoricoVenta,
                DetalleVenta,
                form=DetalleVentaForm,
                extra=1,
                can_delete=True
            )()
        return context

class CrearVentaAsociado(CreateView):
    model = HistoricoVenta
    form_class = HistoricoVentaForm
    template_name = 'base/ventas/crearVentaAsociado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'asociado': Asociado.objects.get(pk = self.kwargs['pkAsociado']),
            'pkAsociado': self.kwargs['pkAsociado']
        })
        return context