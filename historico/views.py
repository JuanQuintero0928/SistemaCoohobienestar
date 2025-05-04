import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DeleteView, TemplateView, DetailView
from usuarios.models import UsuarioAsociado
from django.contrib import messages
from django.db.models import Sum, F, Q, Subquery, Case, When, Value, IntegerField
from django.db import transaction
from django.core.paginator import Paginator
from django.utils.timezone import timedelta
from reportes.utils.medicion import medir_rendimiento

from .models import HistoricoAuxilio, HistorialPagos, HistoricoCredito
from parametro.models import MesTarifa, FormaPago, Tarifas, TipoAsociado
from asociado.models import Asociado, ParametroAsociado, TarifaAsociado
from .form import CargarArchivoForm
from ventas.models import HistoricoVenta
from funciones.function import procesar_csv

# Create your views here.

class InformacionHistorico(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'proceso/informacion.html'
        return render(request, template_name)

class VerHistoricoAuxilio(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/asociado/listarAsociado.html'
        query = HistoricoAuxilio.objects.all()
        return render(request, template_name, {'query':query})

class VerHistoricoPagos(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'proceso/pago/listarPagos.html'
        
        # Capturar el valor de búsqueda del formulario
        busqueda = request.GET.get('numDocumento')
        mensaje = None  # Variable para el mensaje

        if busqueda:
            try:
                # se valida si es un numero
                valorBuscado = int(busqueda.replace('.', ''))
                query = HistorialPagos.objects.select_related(
                            'asociado', 'mesPago', 'formaPago', 'asociado__tAsociado'
                        ).filter(asociado__numDocumento__icontains=valorBuscado)
            except ValueError:
                # si salta error, se busca por nombre o apellido
                query = HistorialPagos.objects.select_related(
                    'asociado', 'mesPago', 'formaPago', 'asociado__tAsociado'
                    ).filter(
                    Q(asociado__apellido__icontains=busqueda) |
                    Q(asociado__nombre__icontains=busqueda)
                    )
        else: 
            # Consulta para obtener los registros
            query = HistorialPagos.objects.select_related(
                'asociado', 'mesPago', 'formaPago', 'asociado__tAsociado'
            ).all()
        
        # Verificar si no hay resultados
        if not query.exists():
            mensaje = "No se encontraron resultados para la búsqueda."
        
        # Configurar el paginador
        paginator = Paginator(query, 10)  # Muestra 10 registros por página
        page_number = request.GET.get('page')  # Obtén el número de página de la URL
        page_obj = paginator.get_page(page_number)  # Obtén la página actual
        
        return render(request, template_name, {'page_obj': page_obj, 'mensaje':mensaje})

class VerAsociadoPagos(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'proceso/pago/realizarPago.html'
        query = TarifaAsociado.objects.values('id','asociado__nombre','asociado__id','asociado__apellido','asociado__numDocumento','total','asociado__tAsociado__concepto')
        return render(request, template_name, {'query':query})

class ModalPago(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'proceso/pago/modalPago.html'
        queryValor = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
        queryParamAsoc = ParametroAsociado.objects.get(asociado = kwargs['pkAsociado'])
        queryHistorial = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).exists()

        # Obtener la suma de los adicionales del asociado, se suma todo menos el aporte y el bSocial
        queryTarifa = TarifaAsociado.objects.filter(asociado = kwargs['pkAsociado']).aggregate(
            total_tarifa_asociado=Sum(
                F('cuotaMascota') + 
                F('cuotaRepatriacion') + 
                F('cuotaSeguroVida') + 
                F('cuotaAdicionales') + 
                F('cuotaCoohopAporte') + 
                F('cuotaCoohopBsocial') +
                F('cuotaConvenio')
            )
        )
        
        total_tarifa_asociado = queryTarifa['total_tarifa_asociado'] or 0  # Se obtiene el valor de la suma a 0 si no hay datos        

        if queryHistorial:
            mesesPagados = (HistorialPagos.objects
                            .filter(asociado = kwargs['pkAsociado'], mesPago_id__lt = 9990)
                            .values('mesPago'))
            queryMes = (MesTarifa.objects
                            .exclude(pk__in=Subquery(mesesPagados))
                            .exclude(pk=9993)
                            .filter(pk__gte = queryParamAsoc.primerMes.pk)
                            .annotate(
                                total = Case(
                                    When(pk__gte=9990, then=Value(0)),           # Se envia valor en 0 para mostrar en el template
                                    default=F('aporte') + F('bSocial') + total_tarifa_asociado, # se suma al resto de pk el valor de aporte, bsocial y total tarifa
                                    output_field=IntegerField()
                                )
                            )
                        )
        else:
            queryMes = MesTarifa.objects.filter(pk__gte = queryParamAsoc.primerMes.pk).annotate(total=F('aporte') + F('bSocial') + total_tarifa_asociado).exclude(pk=9993)
        
        queryPago = FormaPago.objects.all()

        queryHistorial = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).aggregate(total=Sum('diferencia'))
        total_diferencia = queryHistorial['total'] or 0  # Se obtiene el valor de la suma a 0 si no hay datos

        # Se valida si el asociado cuenta con credito de productos home elements
        queryValidacion = HistoricoVenta.objects.filter(asociado = kwargs['pkAsociado'], estadoRegistro = True, formaPago__in = ['CREDITO', 'DESCUENTO NOMINA']).exists()
        queryCreditoProd = None
        if queryValidacion:
            queryCreditoProd = HistoricoVenta.objects.filter(
                    asociado = kwargs['pkAsociado'],
                    formaPago__in = ['CREDITO', 'DESCUENTO NOMINA'],
                    estadoRegistro = True,
                    pendientePago__gt = 0
                )
            for homeElements in queryCreditoProd:
                if homeElements.valorNeto % homeElements.pendientePago != 0:
                    if homeElements.cuotas - homeElements.cuotasPagas == 1:
                        homeElements.valorCuotas = homeElements.pendientePago
        
        # Se valida si el asociado cuenta con credito
        queryValidacionCredito = HistoricoCredito.objects.filter(asociado = kwargs['pkAsociado'], estadoRegistro = True, pendientePago__gt = 0).exists()
        queryCredito = None
        if queryValidacionCredito:
            queryCredito = HistoricoCredito.objects.filter(
                    asociado = kwargs['pkAsociado'],
                    estadoRegistro = True,
                    pendientePago__gt = 0
                )
            for credito in queryCredito:
                if credito.totalCredito % credito.pendientePago != 0:
                    if credito.cuotas - credito.cuotasPagas == 1:
                        credito.valorCuota = credito.pendientePago
        
        # Se valida si el asociado debe cuotas de la vinculación
        cuotaVinculacion = None
        cuotaVinculacionMenorEdad = Tarifas.objects.values('valor').get(pk=8)
        if queryParamAsoc.vinculacionFormaPago and queryParamAsoc.vinculacionFormaPago.pk == 2 and queryParamAsoc.vinculacionPendientePago > 0:
            queryPagosVinculacion = HistorialPagos.objects.filter(
                asociado = kwargs['pkAsociado'],
                mesPago = 9995, # Id de la vinculación Adulto
                estadoRegistro = True,
            ).count()

            if queryPagosVinculacion == (queryParamAsoc.vinculacionCuotas - 1):
                cuotaVinculacion = queryParamAsoc.vinculacionPendientePago
            else:
                cuotaVinculacion = queryParamAsoc.vinculacionValor

        context = {
            'pkAsociado':kwargs['pkAsociado'],
            'vista':kwargs['vista'],
            'query':queryValor,
            'queryMes':queryMes,
            'queryPago':queryPago,
            'diferencia':total_diferencia,
            'queryCreditoProd':queryCreditoProd,
            'queryCredito':queryCredito,
            'cuotaVinculacion':cuotaVinculacion,
            'cuotaVinculacionMenorEdad':cuotaVinculacionMenorEdad
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        fechaPago = request.POST['fechaPago']
        formaPago = request.POST['formaPago']
        valorPago = int(request.POST['valorPago'])
        tarifaAsociado = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
        diferencia = request.POST['diferencia']
        valorDiferencia = int(diferencia.replace('.', ''))

        # creamos un array para guardar los pagos que se marcaron como activos
        datos_pagos = []

        # obtenemos los switchs que se marcaron como activos en el modal
        switches_activos = request.POST.getlist('switches') or []
     
         # saber el tamaño de los botones marcados
        cantidadSwitches = len(switches_activos)

        usuario = request.user
    
        # Se recorre los switch activos, con el pk del mes activo
        for contador, pk in enumerate(switches_activos, start=1):
            
            split = pk.split('-')

            if len(split) == 1:
                # Aplica para abonos, se crea un registro de pago con el valor de abono
                if pk == '9999':
                    pago = {
                        'asociado': Asociado.objects.get(pk = kwargs['pkAsociado']),
                        'mesPago': MesTarifa.objects.get(pk = pk),
                        'fechaPago': fechaPago,
                        'formaPago': FormaPago.objects.get(pk = formaPago),
                        'aportePago': MesTarifa.objects.get(pk = pk).aporte,
                        'bSocialPago': MesTarifa.objects.get(pk = pk).bSocial,
                        'mascotaPago': 0,
                        'repatriacionPago': 0,
                        'seguroVidaPago': 0,
                        'adicionalesPago': 0,
                        'coohopAporte': 0,
                        'coohopBsocial': 0,
                        'convenioPago': 0,
                        'creditoHomeElements': 0,
                        'diferencia': valorDiferencia if cantidadSwitches == contador else 0,
                        'valorPago':  valorDiferencia if cantidadSwitches == contador else 0,
                        'estadoRegistro': True,
                        'userCreacion': usuario,
                    }
                    datos_pagos.append(pago)

                # Aplica para pagos de boletas de cine y certificado, pk 9997 y 9996
                elif pk in ['9997', '9996']:
                    if pk == '9997':
                        valorPago = request.POST['valorCine'] if contador < cantidadSwitches else int(request.POST['valorCine']) + valorDiferencia
                    elif pk == '9996':
                        valorPago = request.POST['valorCertificado'] if contador < cantidadSwitches else int(request.POST['valorCertificado']) + valorDiferencia

                    pago = {
                            'asociado': Asociado.objects.get(pk = kwargs['pkAsociado']),
                            'mesPago': MesTarifa.objects.get(pk = pk),
                            'fechaPago': fechaPago,
                            'formaPago': FormaPago.objects.get(pk = formaPago),
                            'aportePago': 0,
                            'bSocialPago': 0,
                            'mascotaPago': 0,
                            'repatriacionPago': 0,
                            'seguroVidaPago': 0,
                            'adicionalesPago': 0,
                            'coohopAporte': 0,
                            'coohopBsocial': 0,
                            'convenioPago': 0,
                            'creditoHomeElements': 0,
                            'diferencia': valorDiferencia if cantidadSwitches == contador else 0,
                            'valorPago':  valorPago,
                            'estadoRegistro': True,
                            'userCreacion': usuario,
                        }
                    datos_pagos.append(pago)

                # Aplica para pagos de mes normal, se crea un registro de pago con el valor del mes
                else:
                    valorMes = MesTarifa.objects.get(pk = pk).aporte + MesTarifa.objects.get(pk = pk).bSocial + tarifaAsociado.cuotaMascota + tarifaAsociado.cuotaRepatriacion + tarifaAsociado.cuotaSeguroVida + tarifaAsociado.cuotaAdicionales + tarifaAsociado.cuotaCoohopAporte + tarifaAsociado.cuotaCoohopBsocial + tarifaAsociado.cuotaConvenio
                    valorPago = valorMes if contador < cantidadSwitches else valorMes + valorDiferencia

                    pago = {
                            'asociado': Asociado.objects.get(pk = kwargs['pkAsociado']),
                            'mesPago': MesTarifa.objects.get(pk = pk),
                            'fechaPago': fechaPago,
                            'formaPago': FormaPago.objects.get(pk = formaPago),
                            'aportePago': MesTarifa.objects.get(pk = pk).aporte,
                            'bSocialPago': MesTarifa.objects.get(pk = pk).bSocial,
                            'mascotaPago': tarifaAsociado.cuotaMascota,
                            'repatriacionPago': tarifaAsociado.cuotaRepatriacion,
                            'seguroVidaPago': tarifaAsociado.cuotaSeguroVida,
                            'adicionalesPago': tarifaAsociado.cuotaAdicionales,
                            'coohopAporte': tarifaAsociado.cuotaCoohopAporte,
                            'coohopBsocial': tarifaAsociado.cuotaCoohopBsocial,
                            'convenioPago': tarifaAsociado.cuotaConvenio,
                            'creditoHomeElements': 0,
                            'diferencia': valorDiferencia if cantidadSwitches == contador else 0,
                            'valorPago':  valorPago,
                            'estadoRegistro': True,
                            'userCreacion': usuario,
                        }
                    datos_pagos.append(pago)

            # Aplica para Pagos de vinculacion de adulto y menores edad, pk 9994, 9995
            elif len(split) == 2:
                pk = split[0]   # pk del mes (9994-9995)
                cuotaVinculacion = int(split[1]) # valor pagado
         
                valorPago = cuotaVinculacion + valorDiferencia if cantidadSwitches == contador else cuotaVinculacion
         
                pago = {
                        'asociado': Asociado.objects.get(pk = kwargs['pkAsociado']),
                        'mesPago': MesTarifa.objects.get(pk = pk),
                        'fechaPago': fechaPago,
                        'formaPago': FormaPago.objects.get(pk = formaPago),
                        'aportePago': 0,
                        'bSocialPago': 0,
                        'mascotaPago': 0,
                        'repatriacionPago': 0,
                        'seguroVidaPago': 0,
                        'adicionalesPago': 0,
                        'coohopAporte': 0,
                        'coohopBsocial': 0,
                        'convenioPago': 0,
                        'creditoHomeElements': 0,
                        'diferencia': valorDiferencia if cantidadSwitches == contador else 0,
                        'valorPago':  valorPago,
                        'estadoRegistro': True,
                        'userCreacion': usuario,
                    }
                datos_pagos.append(pago)

                if pk == '9995':
                    # Si es vinculacion de adulto, actualizamos el pendiente de pago
                    ParametroAsociado.objects.filter(asociado = kwargs['pkAsociado']).update(
                        vinculacionPendientePago=F('vinculacionPendientePago')- valorPago
                    )

            # Aplica para Creditos Home Elements
            # desde el modalPago se envia, pkVenta, 9998, valorCuota
            else:
                extra_param = split[0]  # pk de la venta
                pk = split[1] # identificador del tipo de pago, credito home elements
                valorCuota = int(split[2].replace('.', ''))  # valor de la cuota

                # Creditos Home Elements
                if pk == '9998':
                    queryCreditoProd = HistoricoVenta.objects.get(pk = extra_param)
                    pago = {
                        'asociado': Asociado.objects.get(pk = kwargs['pkAsociado']),
                        'mesPago': MesTarifa.objects.get(pk = pk),
                        'fechaPago': fechaPago,
                        'formaPago': FormaPago.objects.get(pk = formaPago),
                        'aportePago': 0,
                        'bSocialPago': 0,
                        'mascotaPago': 0,
                        'repatriacionPago': 0,
                        'seguroVidaPago': 0,
                        'adicionalesPago': 0,
                        'coohopAporte': 0,
                        'coohopBsocial': 0,
                        'convenioPago': 0,
                        'creditoHomeElements': queryCreditoProd.valorCuotas,
                        'diferencia': valorCuota - queryCreditoProd.valorCuotas + valorDiferencia if cantidadSwitches == contador else 0,
                        'valorPago':  queryCreditoProd.valorCuotas if contador < cantidadSwitches else valorCuota + valorDiferencia,
                        'ventaHE': queryCreditoProd,
                        'estadoRegistro': True,
                        'userCreacion': usuario,
                    }
                    datos_pagos.append(pago)
                    if contador < cantidadSwitches:
                        queryCreditoProd.valorCuotas
                    elif queryCreditoProd.valorCuotas :
                        queryCreditoProd.valorCuotas + valorDiferencia
                    queryCreditoProd.pendientePago = queryCreditoProd.pendientePago - pago['valorPago']
                    queryCreditoProd.cuotasPagas = queryCreditoProd.cuotasPagas + 1
                    
                    queryCreditoProd.save()

                # Pk 9993 credito
                else:
                    queryCredito = HistoricoCredito.objects.get(pk = extra_param)
                    valorPago = queryCredito.valorCuota if contador < cantidadSwitches else valorCuota + valorDiferencia
                    pago = {
                        'asociado': Asociado.objects.get(pk = kwargs['pkAsociado']),
                        'mesPago': MesTarifa.objects.get(pk = pk),
                        'fechaPago': fechaPago,
                        'formaPago': FormaPago.objects.get(pk = formaPago),
                        'aportePago': 0,
                        'bSocialPago': 0,
                        'mascotaPago': 0,
                        'repatriacionPago': 0,
                        'seguroVidaPago': 0,
                        'adicionalesPago': 0,
                        'coohopAporte': 0,
                        'coohopBsocial': 0,
                        'convenioPago': 0,
                        'creditoHomeElements': 0,
                        'credito': queryCredito.valorCuota,
                        'diferencia': valorCuota - queryCredito.valorCuota + valorDiferencia if cantidadSwitches == contador else 0,
                        'creditoId': queryCredito,
                        'valorPago':  valorPago,
                        'estadoRegistro': True,
                        'userCreacion': usuario,
                    }
                    datos_pagos.append(pago)
                    queryCredito.pendientePago = queryCredito.pendientePago - valorPago
                    queryCredito.cuotasPagas = queryCredito.cuotasPagas + 1
                    queryCredito.save()

        # Crear cada registro en un bucle
        for data in datos_pagos:
            HistorialPagos.objects.create(**data)
        
        messages.info(request, 'Pago Registrado Correctamente')
        url = reverse('proceso:asociadoPago')

        # Ajusta la URL según el valor de vista
        if kwargs['vista'] == 1:
            url = reverse('asociado:historialPagos', args=[kwargs['pkAsociado']])

        return HttpResponseRedirect(url)

class EditarPago(ListView):
    
    def get(self, request, *args, **kwargs):
        template_name = 'proceso/pago/editarPagoAsociado.html'
        queryPago = HistorialPagos.objects.select_related('mesPago', 'formaPago').get(pk=kwargs['pk'])
        mesesPagados = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).values('mesPago')
        queryMes = MesTarifa.objects.exclude(pk__in=Subquery(mesesPagados))
        queryFormaPago = FormaPago.objects.all()
        return render(request, template_name, {'queryPago':queryPago, 'queryFormaPago':queryFormaPago, 'queryMes':queryMes, 'pk':kwargs['pk'], 'pkAsociado':kwargs['pkAsociado'], 'vista':kwargs['vista']})
    
    def post(self, request, *args, **kwargs):

        mesPago = request.POST['mesPago']

        objHistorico = HistorialPagos.objects.get(pk = kwargs['pk'])
        
        objHistorico.mesPago = MesTarifa.objects.get(pk = mesPago)
        objHistorico.formaPago = FormaPago.objects.get(pk = request.POST['formaPago'])
        objHistorico.fechaPago = request.POST['fechaPago']
        objHistorico.valorPago = request.POST['valorPago']
        objHistorico.aportePago = request.POST['aportePago']
        objHistorico.bSocialPago = request.POST['bSocialPago']
        objHistorico.diferencia = request.POST['diferencia']
        if objHistorico.mascotaPago != 0:
            objHistorico.mascotaPago = request.POST['mascotaPago']
        if objHistorico.repatriacionPago != 0:
            objHistorico.repatriacionPago = request.POST['repatriacionPago']
        if objHistorico.seguroVidaPago != 0:
            objHistorico.seguroVidaPago = request.POST['seguroVidaPago']
        if objHistorico.adicionalesPago != 0:
            objHistorico.adicionalesPago = request.POST['adicionalesPago']
        if objHistorico.coohopAporte != 0:
            objHistorico.coohopAporte = request.POST['coohopAporte']
        if objHistorico.coohopBsocial != 0:
            objHistorico.coohopBsocial = request.POST['coohopBsocial']
        if objHistorico.convenioPago != 0:
            objHistorico.convenioPago = request.POST['convenioPago']
        objHistorico.userModificacion = UsuarioAsociado.objects.get(pk = request.user.pk)
        objHistorico.save()
        messages.info(request, 'Pago Modificado Correctamente')

        # Recupera el valor de num_documento del POST
        num_documento = request.POST.get('num_documento', '')
        # Inicializar la URL por defecto
        url = reverse('proceso:historicoPagos')

        # Ajusta la URL según el valor de vista
        if kwargs['vista'] == 1:
            url = reverse('asociado:historialPagos', args=[kwargs['pkAsociado']])
        
        # Añadir el filtro de num_documento como parámetro en la URL
        if num_documento:
            url += f'?numDocumento={num_documento}'

        return HttpResponseRedirect(url)

class EliminarPago(DeleteView):
    def get(self, request, *args, **kwargs):
        template_name = 'proceso/pago/eliminar.html'
        query = HistorialPagos.objects.get(pk = kwargs['pk'])
        context = {'query': query,
                   'pk': kwargs['pk'],
                   'pkAsociado': kwargs['pkAsociado'],
                   'vista': kwargs['vista'],
                   }
        return render(request, template_name, context) 

    def post(self, request, *args, **kwargs):

        obj = HistorialPagos.objects.get(pk=kwargs['pk'])
    
        # si es credito home elements, se elimina el registro y se actualiza el valor de credito
        if obj.mesPago.pk == 9998:
            credito = (HistoricoVenta.objects
                            .get(asociado = kwargs['pkAsociado'], valorCuotas = obj.creditoHomeElements, estadoRegistro = True)
                        )
            credito.pendientePago = credito.pendientePago + obj.valorPago
            credito.cuotasPagas = credito.cuotasPagas - 1
            credito.save()
        
        obj.delete()
        messages.info(request, 'Pago Eliminado Correctamente')

        # Recupera el valor de num_documento del POST
        num_documento = request.POST.get('num_documento', '')
        # Inicializar la URL por defecto
        url = reverse('proceso:historicoPagos')

        # Ajusta la URL según el valor de vista
        if kwargs['vista'] == 1:
            url = reverse('asociado:historialPagos', args=[kwargs['pkAsociado']])
        
        # Añadir el filtro de num_documento como parámetro en la URL
        if num_documento:
            url += f'?numDocumento={num_documento}'

        return HttpResponseRedirect(url)

class cargarCSV(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'proceso/cargarCSV.html'
        form = CargarArchivoForm()
        return render(request, template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        archivo_csv = request.FILES.get('archivo_csv')
        if archivo_csv:
            try:
                user_creacion_id = request.user.pk
                registros = procesar_csv(archivo_csv, user_creacion_id)
                HistorialPagos.objects.bulk_create(registros)
                messages.info(request, "Datos insertados correctamente:  Se ha registrado " + str(len(registros)) + " registros.")
            except ValueError as e:
                messages.error(request, f"Error: {str(e)}")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
                
        return redirect('proceso:cargarCSV')    
            
class ActualizarEstadoAsoc(TemplateView):
    template_name = 'proceso/actualizarEstadoAsoc.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['TipoAsociado'] = TipoAsociado.objects.all()
        context['mes'] = MesTarifa.objects.filter(pk__lte=9990)
        return context

    def post(self, request, *args, **kwargs):
        tipoAsociado = request.POST['tipoAsociado']
        mes = int(request.POST['mes'])

        resultado = []

        if tipoAsociado == '0':
            asociados = Asociado.objects.filter(~Q(estadoAsociado = 'RETIRO')).values('id','nombre','apellido','numDocumento','estadoAsociado')
        else:
            asociados = Asociado.objects.filter(~Q(estadoAsociado = 'RETIRO'), tAsociado = tipoAsociado).values('id','nombre','apellido','numDocumento', 'estadoAsociado')
        
        for asociado in asociados:
            # query de primer mes del asociado
            primerMes = ParametroAsociado.objects.filter(asociado=asociado['id']).values_list('primerMes', flat=True).first()
            # Si el asociado se vinculo antes del mes seleccionado
            if primerMes <= mes:
                # numero de pagos del asociado del mes seleccionado hacia atras
                pagosRealizados = HistorialPagos.objects.filter(asociado = asociado['id'], mesPago__lte = mes).count()
                pagosEsperados = mes - (primerMes -1)
                # tiene el mismo numero de pagos que el mes seleccionado
                if pagosEsperados == pagosRealizados:
                    diferencia = HistorialPagos.objects.filter(asociado = asociado['id'], mesPago__lte = mes).aggregate(totalDiferencia=Sum('diferencia'))['totalDiferencia'] or 0
                    # Activo
                    if diferencia >= 0:
                        resultado.append({
                            'id':asociado['id'],
                            'numero_documento':asociado['numDocumento'],
                            'nombre_completo':asociado['nombre'] + ' ' + asociado['apellido'],
                            'estado_actual':asociado['estadoAsociado'],
                            'estado_calculado':"ACTIVO",
                            'observaciones':'',
                        })
                    # Inactivo, diferencia negativa
                    else:
                        resultado.append({
                            'id':asociado['id'],
                            'numero_documento':asociado['numDocumento'],
                            'nombre_completo':asociado['nombre'] + ' ' + asociado['apellido'],
                            'estado_actual':asociado['estadoAsociado'],
                            'estado_calculado':"INACTIVO",
                            'observaciones': f'Inactivo, diferencia negativa {diferencia}',
                        })
                else:
                    # listado de meses los cuales el asociado debe tener pagado
                    listaMeses = MesTarifa.objects.filter(id__gte=primerMes, id__lte=mes).values_list('id', 'concepto')
                    mesesPagados = HistorialPagos.objects.filter(
                                    asociado_id=asociado['id'],
                                    mesPago__id__gte=primerMes,
                                    mesPago__id__lte=mes
                                    ).values_list('mesPago__id', flat=True)
                    mesesFaltantes = [mes for mes in listaMeses if mes[0] not in mesesPagados]
                    soloMeses = [mes[1] for mes in mesesFaltantes]
                    resultado.append({
                        'id':asociado['id'],
                        'numero_documento':asociado['numDocumento'],
                        'nombre_completo':asociado['nombre'] + ' ' + asociado['apellido'],
                        'estado_actual':asociado['estadoAsociado'],
                        'estado_calculado':"INACTIVO",
                        'observaciones': f'Meses faltantes: {soloMeses}',
                    })
            # El asociado se vinculo despues del mes seleccionado, activo
            else:
                resultado.append({
                    'id':asociado['id'],
                    'numero_documento':asociado['numDocumento'],
                    'nombre_completo':asociado['nombre'] + ' ' + asociado['apellido'],
                    'estado_actual':asociado['estadoAsociado'],
                    'estado_calculado':"ACTIVO",
                    'observaciones':'',
                })
        return JsonResponse({'resultados':resultado})

def actualizarEstadoMasivo(request):
    if request.method == "POST":
        data = json.loads(request.body) # Convertir la peticion Json a un diccionario
        asociados = data.get("asociados", [])  # Obtenemos los datos enviados

        if not asociados:
            return JsonResponse({"success": False, "error": "No se enviaron datos"}, status=400)

        with transaction.atomic():  #  se usa una transacción para mayor eficiencia
            registroActualizar =[]
            for asociado_data in asociados:
                asociado = Asociado.objects.filter(id=asociado_data["id"]).first()
                if asociado:
                    asociado.estadoAsociado = asociado_data["estado"]
                    registroActualizar.append(asociado)
            
            Asociado.objects.bulk_update(registroActualizar, ["estadoAsociado"])
            
        return JsonResponse({"success": True, "actualizados": len(asociados)})
    
    # Manejo de error si no es un POST
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=400)

class ComprobantePago(DetailView):
    model = HistorialPagos
    template_name = "proceso/pago/comprobante.html"
    context_object_name = "pago"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pago_principal = self.get_object()
        asociado = pago_principal.asociado
        fecha_objetivo = pago_principal.fechaCreacion

        # Rango de 2 segundos antes y después
        rango_inicio = fecha_objetivo - timedelta(seconds=2)
        rango_fin = fecha_objetivo + timedelta(seconds=2)

        pagos_relacionados = HistorialPagos.objects.filter(
            asociado=asociado,
            fechaCreacion__range=(rango_inicio, rango_fin),
            fechaPago = pago_principal.fechaPago
        ).order_by('fechaCreacion').annotate(
            total_aporte_bsocial=Sum(F('aportePago') + F('bSocialPago')),
            total_coohop = Sum(F('coohopAporte') + F('coohopBsocial')),
        )

        pago_total = pagos_relacionados.aggregate(total=Sum('valorPago'))['total'] or 0

        context['pagos_relacionados'] = pagos_relacionados
        context['pago_total'] = pago_total

        return context