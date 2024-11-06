from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
from django.core.paginator import Paginator

from .models import HistoricoAuxilio, HistorialPagos
from parametro.models import MesTarifa, FormaPago
from asociado.models import Asociado, ParametroAsociado, TarifaAsociado

from .form import HistorialPagoForm

# Create your views here.

class VerHistoricoAuxilio(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/asociado/listarAsociado.html'
        query = HistoricoAuxilio.objects.all()
        return render(request, template_name, {'query':query})

class VerHistoricoPagos(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'proceso/pago/listarPagos.html'
        
        # Capturar el valor de búsqueda del formulario
        num_documento = request.GET.get('numDocumento')

        # Consulta para obtener los registros
        query = HistorialPagos.objects.select_related(
            'asociado', 'mesPago', 'formaPago', 'asociado__tAsociado'
        ).all()
        
        # Filtrar por numDocumento si se ingresó algo en el campo de búsqueda
        if num_documento:
            query = query.filter(asociado__numDocumento__icontains=num_documento)

        # Configurar el paginador
        paginator = Paginator(query, 10)  # Muestra 10 registros por página
        page_number = request.GET.get('page')  # Obtén el número de página de la URL
        page_obj = paginator.get_page(page_number)  # Obtén la página actual
        
        return render(request, template_name, {'page_obj': page_obj})

class VerAsociadoPagos(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'proceso/pago/realizarPago.html'
        query = TarifaAsociado.objects.values('id','asociado__nombre','asociado__id','asociado__apellido','asociado__numDocumento','total','asociado__tAsociado__concepto')
        return render(request, template_name, {'query':query})
    
class CrearPagoAsociado(CreateView):

    def get(self, request, *args, **kwargs):
        template_name = 'proceso/pago/crearPagoAsociado.html'
        queryValor = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
        queryParamAsoc = ParametroAsociado.objects.get(asociado = kwargs['pkAsociado'])
        queryHistorial = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).exists()
        if queryHistorial:
            queryUltPago = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).last()
            queryMes = MesTarifa.objects.filter(pk__gt = queryUltPago.mesPago.pk)
        else:
            queryMes = MesTarifa.objects.filter(pk__gte = queryParamAsoc.primerMes.pk)
        queryPago = FormaPago.objects.all()
        queryHistorial = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).aggregate(total=Sum('diferencia'))
        for valor in queryHistorial.values():
            diferencia = valor
        return render(request, template_name, {'pkAsociado':kwargs['pkAsociado'], 'query':queryValor, 'queryMes':queryMes, 'queryPago':queryPago, 'diferencia':diferencia})

    def post(self, request, *args, **kwargs):
        mesPago = int(request.POST['mesPago'])
        formaPago = int(request.POST['formaPago'])
        if mesPago == 0 or formaPago == 0:
            messages.warning(request, "Digite completamente el formulario, fecha y forma de pago.")
            return redirect('proceso:asociadoPago')
        else:
            fechaPago = request.POST['fechaPago']
            valorPago = int(request.POST['valorPago'])
            aportePago = int(request.POST['aportePago'])
            bSocialPago = int(request.POST['bSocialPago'])
            mascotaPago = int(request.POST['mascotaPago'])
            repatriacionPago = int(request.POST['repatriacionPago'])
            seguroVidaPago = int(request.POST['seguroVidaPago'])
            adicionalesPago = int(request.POST['adicionalesPago'])
            coohopAporte = int(request.POST['coohopAporte'])
            coohopBsocial = int(request.POST['coohopBsocial'])
            
            # se realiza validacion en caso que el usuario pague menos del valor establecido
            valorPagoVerificacion = int(request.POST['valorPagoVerificacion'])
            valorPago = int(request.POST['valorPago'])
            obj = HistorialPagos()
            diferencia = 0
            # se valida si el valor pago es igual al valor real que debe pagar
            if valorPago != valorPagoVerificacion:
                diferencia = valorPago - valorPagoVerificacion
            obj.asociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
            obj.mesPago = MesTarifa.objects.get(pk = mesPago)
            obj.fechaPago = fechaPago
            obj.valorPago = valorPago
            obj.aportePago = aportePago
            obj.bSocialPago = bSocialPago
            obj.mascotaPago = mascotaPago
            obj.repatriacionPago = repatriacionPago
            obj.seguroVidaPago = seguroVidaPago
            obj.adicionalesPago = adicionalesPago
            obj.coohopAporte = coohopAporte
            obj.coohopBsocial = coohopBsocial
            obj.diferencia = diferencia
            obj.formaPago = FormaPago.objects.get(pk = formaPago)
            obj.estadoRegistro = True
            obj.userCreacion = User.objects.get(pk = request.user.pk)
            obj.save()
            messages.info(request, 'Pago Registrado Correctamente')
            return redirect('proceso:asociadoPago')                

class EditarPago(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'proceso/pago/editarPagoAsociado.html'
        queryPago = HistorialPagos.objects.get(pk = kwargs['pk'])
        queryMes = MesTarifa.objects.all()
        queryFormaPago = FormaPago.objects.all()
        return render(request, template_name, {'queryPago':queryPago, 'queryFormaPago':queryFormaPago, 'queryMes':queryMes, 'pk':kwargs['pk'], 'pkAsociado':kwargs['pkAsociado']})
    
    def post(self, request, *args, **kwargs):
        objHistorico = HistorialPagos.objects.get(pk = kwargs['pk'])
        objTarifa = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
        valorPago = int(request.POST['valorPago'])
        # se valida si el valor pago es igual al valor real que debe pagar
        if valorPago != objTarifa.total:
            diferencia = valorPago - objTarifa.total
            objHistorico.diferencia = diferencia
        else:
            objHistorico.diferencia = 0
        objHistorico.mesPago = MesTarifa.objects.get(pk = request.POST['mesPago'])
        objHistorico.formaPago = FormaPago.objects.get(pk = request.POST['formaPago'])
        objHistorico.fechaPago = request.POST['fechaPago']
        objHistorico.valorPago = request.POST['valorPago']
        objHistorico.userModificacion = User.objects.get(pk = request.user.pk)
        objHistorico.save()
        messages.info(request, 'Pago Modificado Correctamente')
        return redirect('proceso:historicoPagos')

# backup clase
class CrearPagoAsociadoBackup(CreateView):

    def get(self, request, *args, **kwargs):
        template_name = 'proceso/pago/crearPagoAsociado.html'
        queryValor = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
        form_class = HistorialPagoForm(initial={'aportePago':queryValor.cuotaAporte,
                                                'bSocialPago':queryValor.cuotaBSocial,
                                                'mascotaPago':queryValor.cuotaMascota,
                                                'repatriacionPago':queryValor.cuotaRepatriacion,
                                                'seguroVidaPago':queryValor.cuotaSeguroVida,
                                                'adicionalesPago':queryValor.cuotaAdicionales,
                                                'coohopAporte':queryValor.cuotaCoohopAporte,
                                                'coohopBsocial':queryValor.cuotaCoohopBsocial,
                                                'valorPago':queryValor.total
                                                })
        return render(request, template_name, {'form':form_class, 'pkAsociado':kwargs['pkAsociado']})
   
    def post(self, request, *args, **kwargs):
        formulario = HistorialPagoForm(request.POST)
        if formulario.is_valid():
            obj = HistorialPagos()
            mesPagado = formulario.cleaned_data['mesPago']
            obj.asociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
            # se realiza la validacion si el asociado ya habia pagado el mes seleccionado
            validacion = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).only('mesPago')
            for mes in validacion:
                if mes.mesPago == mesPagado:
                    messages.warning(request, f"{mesPagado}" + ' ya se encuentra registrado para el asociado ' + obj.asociado.nombre + ' ' + obj.asociado.apellido + ', por favor validar la información.')
                    return redirect('proceso:asociadoPago') 
            obj.mesPago = MesTarifa.objects.get(concepto = formulario.cleaned_data['mesPago'])
            obj.valorPago = formulario.cleaned_data['valorPago']
            obj.aportePago = formulario.cleaned_data['aportePago']
            obj.bSocialPago = formulario.cleaned_data['bSocialPago']
            obj.mascotaPago = formulario.cleaned_data['mascotaPago']
            obj.repatriacionPago = formulario.cleaned_data['repatriacionPago']
            obj.seguroVidaPago = formulario.cleaned_data['seguroVidaPago']
            obj.adicionalesPago = formulario.cleaned_data['adicionalesPago']
            obj.coohopAporte = formulario.cleaned_data['coohopAporte']
            obj.coohopBsocial = formulario.cleaned_data['coohopBsocial']
            obj.formaPago = FormaPago.objects.get(formaPago = formulario.cleaned_data['formaPago'])
            obj.estadoRegistro = True
            obj.save()
            messages.info(request, 'Pago Registrado Correctamente')
            return redirect('proceso:asociadoPago')
        else:
            # formulario.cleaned_data['mesPago']
            messages.error(request, 'Pago No se pudo registrar')
            return redirect('proceso:asociadoPago')

# no se usa
class CrearPagoAsociado2(CreateView):

    def get(self, request, *args, **kwargs):
        template_name = 'proceso/pago/crearPagoAsociado.html'
        queryValor = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
        # se realiza la consulta del ultimo pago realizado por el asociado, 
        queryUltimoPago = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).last()
        if queryUltimoPago:
            print(queryUltimoPago.mesPago.pk)
            # se realiza la consulta del mes siguiente que debe pagar el asociado, solo muestra un registro
            mesSiguientePago = MesTarifa.objects.filter(pk__gt = queryUltimoPago.mesPago.pk).first()
            print(mesSiguientePago)
        else:
            mesSiguientePago = MesTarifa.objects.get(pk = 1)
        form_class = HistorialPagoForm(initial={'mesPago':mesSiguientePago,
                                                'aportePago':queryValor.cuotaAporte,
                                                'bSocialPago':queryValor.cuotaBSocial,
                                                'mascotaPago':queryValor.cuotaMascota,
                                                'repatriacionPago':queryValor.cuotaRepatriacion,
                                                'seguroVidaPago':queryValor.cuotaSeguroVida,
                                                'adicionalesPago':queryValor.cuotaAdicionales,
                                                'valorPago':queryValor.total
                                                })
        return render(request, template_name, {'form':form_class, 'pkAsociado':kwargs['pkAsociado']})
   
    def post(self, request, *args, **kwargs):
        formulario = HistorialPagoForm(request.POST)
        print(formulario)
        if formulario.is_valid():
            obj = HistorialPagos()
            obj.asociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
            obj.mesPago = MesTarifa.objects.get(concepto = formulario.cleaned_data['mesPago'])
            obj.valorPago = formulario.cleaned_data['valorPago']
            obj.aportePago = formulario.cleaned_data['aportePago']
            obj.bSocialPago = formulario.cleaned_data['bSocialPago']
            obj.mascotaPago = formulario.cleaned_data['mascotaPago']
            obj.repatriacionPago = formulario.cleaned_data['repatriacionPago']
            obj.seguroVidaPago = formulario.cleaned_data['seguroVidaPago']
            obj.adicionalesPago = formulario.cleaned_data['adicionalesPago']
            obj.formaPago = FormaPago.objects.get(formaPago = formulario.cleaned_data['formaPago'])
            obj.estadoRegistro = True
            obj.save()
            messages.info(request, 'Pago Registrado Correctamente')
            return redirect('proceso:asociadoPago')
        else:
            # formulario.cleaned_data['mesPago']
            messages.error(request, 'Pago No se pudo registrar')
            return redirect('proceso:asociadoPago')


