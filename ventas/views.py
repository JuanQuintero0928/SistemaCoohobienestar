from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DetailView
from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from reportes.utils.medicion import medir_rendimiento
from django.db.models import Sum

from .models import Producto, HistoricoVenta, DetalleVenta, PorcentajeDescuento
from .form import ProductoForm, HistoricoVentaForm, DetalleVentaForm
from asociado.models import Asociado, ParametroAsociado
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

class ListarVentasAsociado(DetailView):
    model = Asociado
    template_name = 'base/ventas/listarVentasAsociado.html'
    context_object_name = 'queryAsociado'
    pk_url_kwarg = 'pkAsociado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asociado = self.object

        ventas = HistoricoVenta.objects.filter(
            asociado=asociado,
            estadoRegistro=True
        ).order_by('fechaVenta')
        
        context.update({
            'ventas': ventas,
            'pkAsociado': asociado.pk,
            'queryAsociado': asociado,  # por compatibilidad si usas esto en el template
            'vista': 11
        })
        return context


@require_http_methods(["GET"])
def verPagosVentas(request, pk):
    if request.method == "GET":
        pagos = HistorialPagos.objects.filter(ventaHE_id = pk)
        forma_pago = FormaPago.objects.all()
        total_pagado = pagos.aggregate(total=Sum("valorPago"))["total"] or 0
        return render(request, "base/ventas/verPagosHistoricoVenta.html", {"data":pagos, "total_pagado":total_pagado, "forma_pago":forma_pago})

class CrearVentaAsociado(CreateView):
    model = HistoricoVenta
    form_class = HistoricoVentaForm
    template_name = 'base/ventas/crearVentaAsociado.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj_asociado = get_object_or_404(Asociado, pk=self.kwargs.get('pkAsociado'))
        obj_parametro_asociado = get_object_or_404(ParametroAsociado, asociado = obj_asociado)
        context.update({
            'asociado': obj_asociado,
            'pkAsociado': self.kwargs['pkAsociado'],
            'queryProducto': Producto.objects.all(),
            'descuento': PorcentajeDescuento.objects.filter(estado = True),
            'metodoPago': FormaPago.objects.all().exclude(id = 2),
            'meses': MesTarifa.objects.filter(id__lte= 9000, id__gte= obj_parametro_asociado.primerMes_id),
        })
        return context

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            asociado = get_object_or_404(Asociado, pk=self.kwargs['pkAsociado'])
            user = request.user

            # === Datos comunes ===
            valor_bruto = int(request.POST['valorBruto'].replace('.', ''))
            valor_neto = int(request.POST['valorNeto'].replace('.', ''))
            forma_pago = request.POST['formaPago']
            fecha_venta = request.POST['fechaVenta']

            # === Crear histórico de venta ===
            objHistoricoVenta = HistoricoVenta.objects.create(
                asociado=asociado,
                fechaVenta=fecha_venta,
                formaPago=forma_pago,
                valorBruto=valor_bruto,
                valorNeto=valor_neto,
                userCreacion=user,
                estadoRegistro=True,
            )

            # === Casos según forma de pago ===
            if forma_pago in ['CREDITO', 'DESCUENTO NOMINA']:
                objHistoricoVenta.primerMes = get_object_or_404(MesTarifa, pk=request.POST['primerMes'])
                objHistoricoVenta.cuotas = request.POST['cuotas']
                objHistoricoVenta.valorCuotas = int(request.POST['valorCuotas'].replace('.', ''))
                objHistoricoVenta.pendientePago = valor_neto
                objHistoricoVenta.cuotasPagas = 0

                tasa_valor, concepto = request.POST['tasaInteres'].split('|')
                objHistoricoVenta.tasaInteres = get_object_or_404(TasasInteresCredito, concepto=concepto)
                objHistoricoVenta.save()

            else:  # CONTADO u otras formas
                objHistoricoVenta.descuento = get_object_or_404(PorcentajeDescuento, pk=1)
                objHistoricoVenta.valorDescuento = 0
                objHistoricoVenta.save()

            # === Función auxiliar para crear HistoricoPago ===
            def crear_historico_pago(valor_pago, mes_pk, metodo_pago_pk):
                return HistorialPagos.objects.create(
                    asociado=asociado,
                    mesPago=get_object_or_404(MesTarifa, pk=mes_pk),
                    fechaPago=fecha_venta,
                    formaPago=get_object_or_404(FormaPago, pk=metodo_pago_pk),
                    aportePago=0,
                    bSocialPago=0,
                    mascotaPago=0,
                    repatriacionPago=0,
                    seguroVidaPago=0,
                    adicionalesPago=0,
                    coohopAporte=0,
                    coohopBsocial=0,
                    convenioPago=0,
                    creditoHomeElements=0,
                    diferencia=0,
                    valorPago=valor_pago,
                    estadoRegistro=True,
                    userCreacion=user,
                    ventaHE=objHistoricoVenta,
                )

            # === Crear pago inmediato ===
            metodo_pago_pk = request.POST.get('metodoPago')
            metodo_pago_anticipo_pk= request.POST.get('formaPagoAnticipo')

            if forma_pago == 'CONTADO':
                crear_historico_pago(valor_neto, mes_pk=9992, metodo_pago_pk=metodo_pago_pk)

            elif forma_pago in ['CREDITO', 'DESCUENTO NOMINA'] and concepto.strip() == 'CREDITO PRODUCTO - 1.0 %':
                anticipo = int(request.POST['anticipo'].replace('.', ''))
                objHistoricoVenta.pendientePago -= anticipo
                objHistoricoVenta.save()
                crear_historico_pago(anticipo, mes_pk=9988, metodo_pago_pk=metodo_pago_anticipo_pk)

            # === Procesar productos ===
            productos = []
            for key, value in request.POST.items():
                if not key.startswith('producto_'):
                    continue

                index = key.split('_')[1]
                producto = get_object_or_404(Producto, pk=int(value))
                productos.append(DetalleVenta(
                    historicoVenta=objHistoricoVenta,
                    producto=producto,
                    precio=int(request.POST.get(f"precio_{index}", "0").replace('.', '')),
                    cantidad=int(request.POST.get(f"cantidad_{index}", "0")),
                    totalBruto=int(request.POST.get(f"totalBruto_{index}", "0").replace('.', '')),
                    totalNeto=int(request.POST.get(f"totalConInteres_{index}", "0").replace('.', '')),
                ))

            # Inserción en bloque para eficiencia
            DetalleVenta.objects.bulk_create(productos)

        messages.info(request, "Venta creada correctamente.")
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
        if venta.formaPago in ['CREDITO', 'DESCUENTO NOMINA']:
            if venta.valorNeto == venta.pendientePago:
                return True
        else:
            print(venta.pk)
            # Se comprueba si hay un pago relacionado a la venta   
            if not HistorialPagos.objects.filter(asociado = self.kwargs['pkAsociado'], ventaHE = venta.pk).exists():
                return True

        # Si no se cumplen las condiciones, se devuelve False, no se puede eliminar la venta
        return False

class UtilidadesProductos(TemplateView):
    template_name = 'base/ventas/utilidades.html'