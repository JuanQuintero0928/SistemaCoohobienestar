from multiprocessing import context
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, F, Q, Subquery
from django.core.paginator import Paginator

from .models import HistoricoAuxilio, HistorialPagos, HistoricoSeguroVida
from parametro.models import MesTarifa, FormaPago, Tarifas
from asociado.models import Asociado, ParametroAsociado, TarifaAsociado
from beneficiario.models import Mascota, Beneficiario, Coohoperativitos
from .form import HistorialPagoForm, CargarArchivoForm
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
            mesesPagados = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).values('mesPago')
            queryMes = (MesTarifa.objects
                        .exclude(pk__in=Subquery(mesesPagados))
                        .filter(pk__gte = queryParamAsoc.primerMes.pk)
                        .annotate(total=F('aporte') + F('bSocial') + total_tarifa_asociado))
        else:
            queryMes = MesTarifa.objects.filter(pk__gte = queryParamAsoc.primerMes.pk).annotate(total=F('aporte') + F('bSocial') + total_tarifa_asociado)
        
        queryPago = FormaPago.objects.all()

        queryHistorial = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).aggregate(total=Sum('diferencia'))
        total_diferencia = queryHistorial['total'] or 0  # Se obtiene el valor de la suma a 0 si no hay datos

        # Se valida si el asociado cuenta con credito de productos home elements
        queryValidacion = HistoricoVenta.objects.filter(asociado = kwargs['pkAsociado'], estadoRegistro = True, formaPago = 'CREDITO').exists()
        queryCreditoProd = None
        if queryValidacion:
            queryCreditoProd = HistoricoVenta.objects.filter(
                    asociado = kwargs['pkAsociado'],
                    formaPago = 'CREDITO',
                    estadoRegistro = True,
                    pendientePago__gt = 0
                )
            for homeElements in queryCreditoProd:
                if homeElements.valorNeto % homeElements.pendientePago != 0:
                    if homeElements.cuotas - homeElements.cuotasPagas == 1:
                        homeElements.valorCuotas = homeElements.pendientePago


        context = {
            'pkAsociado':kwargs['pkAsociado'],
            'vista':kwargs['vista'],
            'query':queryValor,
            'queryMes':queryMes,
            'queryPago':queryPago,
            'diferencia':total_diferencia,
            'queryCreditoProd':queryCreditoProd
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
        switches_activos = request.POST.getlist('switches')
        # saber el tamaño de los botones marcados
        cantidadSwitches = len(switches_activos)
        
        # Se recorre los switch activos, con el pk del mes activo
        for contador, pk in enumerate(switches_activos, start=1):
            # si es un abono, se crea un registro de pago con el valor de abono
            split = pk.split('-')

            if len(split) == 1:
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
                        'userCreacion': User.objects.get(pk = request.user.pk),
                    }
                    datos_pagos.append(pago)
                # si es un mes normal, se crea un registro de pago con el valor del mes
                else:
                    valorMes = MesTarifa.objects.get(pk = pk).aporte + MesTarifa.objects.get(pk = pk).bSocial + tarifaAsociado.cuotaMascota + tarifaAsociado.cuotaRepatriacion + tarifaAsociado.cuotaSeguroVida + tarifaAsociado.cuotaAdicionales + tarifaAsociado.cuotaCoohopAporte + tarifaAsociado.cuotaCoohopBsocial + tarifaAsociado.cuotaConvenio
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
                            'valorPago':  valorMes if contador < cantidadSwitches else valorMes + valorDiferencia,
                            'estadoRegistro': True,
                            'userCreacion': User.objects.get(pk = request.user.pk),
                        }
                    datos_pagos.append(pago)
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
                        'estadoRegistro': True,
                        'userCreacion': User.objects.get(pk = request.user.pk),
                    }
                    if contador < cantidadSwitches:
                        queryCreditoProd.valorCuotas
                    elif queryCreditoProd.valorCuotas :
                        queryCreditoProd.valorCuotas + valorDiferencia
                    datos_pagos.append(pago)
                    queryCreditoProd.pendientePago = queryCreditoProd.pendientePago - pago['valorPago']
                    queryCreditoProd.cuotasPagas = queryCreditoProd.cuotasPagas + 1
                    
                    queryCreditoProd.save()

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
        queryPago = HistorialPagos.objects.get(pk = kwargs['pk'])
        mesesPagados = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).values('mesPago')
        queryMes = MesTarifa.objects.exclude(pk__in=Subquery(mesesPagados))
        queryFormaPago = FormaPago.objects.all()
        return render(request, template_name, {'queryPago':queryPago, 'queryFormaPago':queryFormaPago, 'queryMes':queryMes, 'pk':kwargs['pk'], 'pkAsociado':kwargs['pkAsociado'], 'vista':kwargs['vista']})
    
    def post(self, request, *args, **kwargs):

        mesPago = request.POST['mesPago']

        objHistorico = HistorialPagos.objects.get(pk = kwargs['pk'])
        infoMes = MesTarifa.objects.get(pk=mesPago)
        
        objHistorico.mesPago = MesTarifa.objects.get(pk = mesPago)
        objHistorico.formaPago = FormaPago.objects.get(pk = request.POST['formaPago'])
        objHistorico.fechaPago = request.POST['fechaPago']
        objHistorico.valorPago = request.POST['valorPago']
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
        objHistorico.userModificacion = User.objects.get(pk = request.user.pk)
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


# PRUEBA
class ProcesarPagos(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'proceso/procesarPagos.html'
        return render(request, template_name)
    
    def post(self, request, *args, **kwargs):
        query = Asociado.objects.get(pk = 436)
        valorActual = TarifaAsociado.objects.get(asociado = 436)
        
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
                F('cuotaCoohopBsocial')
            )
        )
   
        total_tarifa_asociado = queryTarifa['total_tarifa_asociado'] or 0  # Se obtiene el valor de la suma a 0 si no hay datos
        if queryHistorial:
            mesesPagados = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).values('mesPago')
            queryMes = (MesTarifa.objects
                        .exclude(pk__in=Subquery(mesesPagados))
                        .filter(pk__gte = queryParamAsoc.primerMes.pk)
                        .annotate(total=F('aporte') + F('bSocial') + total_tarifa_asociado))