from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import Producto, HistoricoVenta
from .form import ProductoForm

# Create your views here.

class ListarProductos(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'ventas/listarProductos.html'
        query = Producto.objects.select_related('categoria')
        return render(request, template_name, {'query':query})
    
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
        return context

class CrearVentaAsociado(CreateView):
    model = HistoricoVenta
    template_name = 'base/ventas/crearVentaAsociado.html'
    context_object_name = 'ventas'
    
        