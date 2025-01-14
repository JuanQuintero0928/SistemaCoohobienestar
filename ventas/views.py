from re import escape
import re
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory

from .models import Producto, HistoricoVenta, DetalleVenta, PorcentajeDescuento
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
        return context

class CrearVentaAsociado(CreateView):
    model = HistoricoVenta
    form_class = HistoricoVentaForm
    template_name = 'base/ventas/crearVentaAsociado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'asociado': Asociado.objects.get(pk = self.kwargs['pkAsociado']),
            'pkAsociado': self.kwargs['pkAsociado'],
            'queryProducto': Producto.objects.all(),
            'descuento': PorcentajeDescuento.objects.filter(estado = True)
        })
        return context

    def post(self, request, *args, **kwargs):
        objHistoricoVenta = HistoricoVenta()
        objHistoricoVenta.asociado = Asociado.objects.get(pk = self.kwargs['pkAsociado'])
        objHistoricoVenta.fechaVenta = request.POST['fechaVenta']
        objHistoricoVenta.formaPago = request.POST['formaPago']
        if objHistoricoVenta.formaPago == 'CREDITO':
            objHistoricoVenta.cuotas = request.POST['cuotas']
            objHistoricoVenta.valorCuotas = int(request.POST['valorCuotas'].replace('.', ''))
            objHistoricoVenta.pendientePago = int(request.POST['valorNeto'].replace('.', ''))
            objHistoricoVenta.cuotasPagas = 0
        else:
            objHistoricoVenta.descuento = PorcentajeDescuento.objects.get(pk = request.POST['descuento'])
            objHistoricoVenta.valorDescuento = int(request.POST['valorDescuento'].replace('.', ''))
        objHistoricoVenta.valorBruto = int(request.POST['valorBruto'].replace('.', ''))
        objHistoricoVenta.valorNeto = int(request.POST['valorNeto'].replace('.', ''))
        objHistoricoVenta.userCreacion = request.user
        objHistoricoVenta.estadoRegistro = True
        objHistoricoVenta.save()
        messages.info(request, f"Venta creada correctamente.")
        return HttpResponseRedirect(reverse_lazy('asociado:listarVentasAsociado', kwargs={'pkAsociado': self.kwargs['pkAsociado']}))