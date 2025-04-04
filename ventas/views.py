from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import Producto, HistoricoVenta, DetalleVenta, PorcentajeDescuento
from .form import ProductoForm, HistoricoVentaForm, DetalleVentaForm
from asociado.models import Asociado
from historico.models import HistorialPagos
from parametro.models import FormaPago, TasasInteresCredito, MesTarifa

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
            {'form': form, 'errors': form.errors, 'operation':'crear'},
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
        # Recuperamos el objecto existente
        self.object = self.get_object()

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
            {'form': form, 'errors': form.errors, 'operation':'editar'},
            status=400
        )
    
class ListarVentasAsociado(ListView):
    model = HistoricoVenta
    template_name = 'base/ventas/listarVentasAsociado.html'
    context_object_name = 'ventas'

    def get_queryset(self):
        return HistoricoVenta.objects.filter(asociado = self.kwargs['pkAsociado'],estadoRegistro=True).order_by('fechaVenta')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'pkAsociado': self.kwargs['pkAsociado'],
            'queryAsociado': Asociado.objects.get(id = self.kwargs['pkAsociado']),
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
            'descuento': PorcentajeDescuento.objects.filter(estado = True),
            'metodoPago': FormaPago.objects.all().exclude(id = 2)
        })
        return context

    def post(self, request, *args, **kwargs):
        objHistoricoVenta = HistoricoVenta()
        objHistoricoVenta.asociado = Asociado.objects.get(pk = self.kwargs['pkAsociado'])
        objHistoricoVenta.fechaVenta = request.POST['fechaVenta']
        objHistoricoVenta.formaPago = request.POST['formaPago']
        if objHistoricoVenta.formaPago == 'CREDITO' or objHistoricoVenta.formaPago == 'DESCUENTO NOMINA':
            objHistoricoVenta.cuotas = request.POST['cuotas']
            objHistoricoVenta.valorCuotas = int(request.POST['valorCuotas'].replace('.', ''))
            objHistoricoVenta.pendientePago = int(request.POST['valorNeto'].replace('.', ''))
            objHistoricoVenta.tasaInteres = TasasInteresCredito.objects.get(porcentaje = request.POST['tasaInteres'])
            objHistoricoVenta.cuotasPagas = 0
        else:
            objHistoricoVenta.descuento = PorcentajeDescuento.objects.get(pk = 1)
            objHistoricoVenta.valorDescuento = 0
            # Se crea el HistoricoPago
            objHistoricoPago = HistorialPagos()
            objHistoricoPago.asociado = objHistoricoVenta.asociado
            objHistoricoPago.mesPago = MesTarifa.objects.get(pk = 9993)
            objHistoricoPago.fechaPago = objHistoricoVenta.fechaVenta
            objHistoricoPago.formaPago = FormaPago.objects.get(pk = 1)
            objHistoricoPago.aportePago = 0
            objHistoricoPago.bSocialPago = 0
            objHistoricoPago.mascotaPago = 0
            objHistoricoPago.repatriacionPago = 0
            objHistoricoPago.seguroVidaPago = 0
            objHistoricoPago.adicionalesPago = 0
            objHistoricoPago.coohopAporte = 0
            objHistoricoPago.coohopBsocial = 0
            objHistoricoPago.convenioPago = 0
            objHistoricoPago.creditoHomeElements = 0
            objHistoricoPago.diferencia = 0
            objHistoricoPago.valorPago = 111
            objHistoricoPago.estadoRegistro = True
            objHistoricoPago.userCreacion = request.user
            objHistoricoPago.save()

        objHistoricoVenta.valorBruto = int(request.POST['valorBruto'].replace('.', ''))
        objHistoricoVenta.valorNeto = int(request.POST['valorNeto'].replace('.', ''))
        objHistoricoVenta.userCreacion = request.user
        objHistoricoVenta.estadoRegistro = True
    
        objHistoricoVenta.save()
        # objDetalleVenta.historicoVenta = objHistoricoVenta.pk

        products = []
        for key, value in request.POST.items():
            if key.startswith('producto_'):
                print(key)
                print(value)
                # Se obtiene el indice del producto
                index = key.split('_')[1]

                # Extrar los datos relacionados
                producto_id = value
                precio = int(request.POST.get(f"precio_{index}", "0").replace('.', ''))
                cantidad = int(request.POST.get(f"cantidad_{index}", "0"))
                total_bruto = int(request.POST.get(f"totalNeto_{index}", "0").replace('.', '')) #en el template se puso valorNeto al valorBruto
                products.append({
                    "historicoVenta": objHistoricoVenta,
                    "producto": Producto.objects.get(pk = int(producto_id)),
                    "precio": precio,
                    "cantidad": cantidad,
                    "totalBruto": total_bruto,
                    "totalNeto": precio * cantidad if objHistoricoVenta.formaPago == "CREDITO" or objHistoricoVenta.formaPago == "DESCUENTO NOMINA" else (precio * cantidad * (1 - objHistoricoVenta.descuento.porcentaje)),
                })

        # Crear cada registro en un bucle
        for data in products:
            DetalleVenta.objects.create(**data)

        messages.info(request, f"Venta creada correctamente.")
        return HttpResponseRedirect(reverse_lazy('asociado:listarVentasAsociado', kwargs={'pkAsociado': self.kwargs['pkAsociado']}))
    
class ListarDetalleVenta(ListView):
    model = DetalleVenta
    template_name = 'base/ventas/listarDetalleVenta.html'
    context_object_name = 'detalleVenta'

    def get_queryset(self):
        return DetalleVenta.objects.filter(historicoVenta = self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'pkAsociado': self.kwargs['pkAsociado'],
            'vista': 11,
            'asociado': Asociado.objects.get(id = self.kwargs['pkAsociado']),
            'historicoVenta': HistoricoVenta.objects.get(id = self.kwargs['pk']),
        })
        return context
    
class EliminarDetalleVenta(UpdateView):
    model = HistoricoVenta
    template_name = 'base/ventas/eliminarDetalleVenta.html'
    fields = ['estadoRegistro']
    context_object_name = 'historicoVenta'

    def form_valid(self, form):
        # Validación personalizada
        if not self.validar_eliminacion():
            messages.error(self.request, "La venta no se ha podido eliminar ya que hay un pago asociado a la venta.")
            return HttpResponseRedirect(reverse_lazy('asociado:listarVentasAsociado', args=[self.kwargs['pkAsociado']])) # No guarda y regresa al formulario

        # Si la validación pasa, procede a cambiar el estado del registro
        form.instance.estadoRegistro = False
        messages.info(self.request, "Venta eliminada exitosamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('asociado:listarVentasAsociado', kwargs={'pkAsociado': self.kwargs['pkAsociado']})

    def get_queryset(self):
        return HistoricoVenta.objects.filter(pk = self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'pk': self.kwargs['pk'],
            'pkAsociado': self.kwargs['pkAsociado'],
            'vista': 11,
        })
        return context
    
    def validar_eliminacion(self):
        # Obtener el objeto de la venta actual
        venta = self.get_object()
        # Comprobar si las cuotas de la venta son iguales a las cuotas pagadas
        if venta.formaPago == 'CREDITO':
            if venta.valorNeto == venta.pendientePago:
                return True
        else:
            return True
        return False
