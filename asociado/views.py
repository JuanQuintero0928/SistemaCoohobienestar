from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Sum, Prefetch, Q
from datetime import date
from funciones.function import StaffRequiredMixin
import json

from .models import Asociado, ConveniosAsociado, Laboral, Financiera, ParametroAsociado, TarifaAsociado, RepatriacionTitular, ConvenioHistoricoGasolina
from beneficiario.models import Beneficiario, Mascota, Coohoperativitos, Parentesco
from credito.models import Codeudor
from departamento.models import Departamento, Municipio, PaisRepatriacion, Pais
from historico.models import HistoricoAuxilio, HistoricoCredito, HistoricoSeguroVida, HistorialPagos
from parametro.models import Tarifas, TipoAsociado, TipoAuxilio, ServicioFuneraria, MesTarifa, Convenio, TasasInteresCredito, FormaPago
from ventas.models import HistoricoVenta

from .form import ConvenioAsociadoForm, RepatriacionTitularForm
from beneficiario.form import BeneficiarioForm, MascotaForm, CoohoperativitoForm
from credito.form import CodeudorForm
from historico.form import HistoricoSeguroVidaForm, HistoricoAuxilioForm, HistoricoCreditoForm
from reportes.utils.medicion import medir_rendimiento
from reportes.utils.extracto import obtenerValorExtracto

# Create your views here.

class Asociados(LoginRequiredMixin, StaffRequiredMixin, ListView):
    template_name = 'base/asociado/listarAsociado.html'
    def get(self, request, *args, **kwargs):
        # Si es una petición AJAX, devolver JSON con paginación
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            start = int(request.GET.get('start', 0))
            length = int(request.GET.get('length', 10))
            search_value = request.GET.get('search_value', '').strip()  
            
            # Obtener columna y dirección de ordenación
            order_column_index = int(request.GET.get('order[0][column]', 0))
            order_direction = request.GET.get('order[0][dir]', 'asc')

            # Mapeo de columnas para ordenación
            column_map = [
                'id', 'nombre', 'apellido', 'numDocumento',
                'tAsociado__concepto', 'numCelular', 'estadoAsociado'
            ]
            
            # Obtener columna de ordenación (por defecto 'id')
            order_column = column_map[order_column_index] if order_column_index < len(column_map) else 'id'
            
            # Aplicar orden ascendente o descendente
            if order_direction == 'desc':
                order_column = f'-{order_column}'

            # Obtener datos ordenados
            query = Asociado.objects.values(
                'id', 'nombre', 'apellido', 'numDocumento',
                'tAsociado__concepto', 'numCelular', 'estadoAsociado'
            ).order_by(order_column)

            # Aplicar filtro de búsqueda
            if search_value:
                query = query.filter(
                    Q(nombre__icontains=search_value) |
                    Q(apellido__icontains=search_value) |
                    Q(numDocumento__icontains=search_value) |
                    Q(tAsociado__concepto__icontains=search_value) |
                    Q(numCelular__icontains=search_value) |
                    Q(estadoAsociado__icontains=search_value)
                )

            total_records = query.count()

            # Aplicar paginación
            paginator = Paginator(query, length)
            page_number = (start // length) + 1
            page = paginator.get_page(page_number)

            return JsonResponse({
                'data': list(page),
                'recordsTotal': total_records,
                'recordsFiltered': total_records,
            })

        else:
            # Renderizar la plantilla en la primera carga
            return render(request, self.template_name)


class CrearAsociado(CreateView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/asociado/crearAsociado.html'
        query_dpto = Departamento.objects.values('id','nombre')
        query_tAsociado = TipoAsociado.objects.all()
        query_parentesco = Parentesco.objects.all().order_by('nombre')
        # seleccionamos el valor de la vinculacion del adulto
        query_tarifa = Tarifas.objects.get(pk = 7)
        query_formaPago = FormaPago.objects.values('id','formaPago')

        context = {
            'query_dpto': query_dpto,
            'query_tAsociado': query_tAsociado,
            'query_parentesco': query_parentesco,
            'query_tarifa': query_tarifa.valor,
            'query_formaPago': query_formaPago,
        }
        return render(request, template_name, context)
    
    def post(self, request, *args, **kwargs):
        numDoc = request.POST['numDocumento']

        if Asociado.objects.filter(numDocumento = numDoc).exists():
            messages.error(request, f"El asociado con el número de documento {numDoc} ya existe.")
            return HttpResponseRedirect(reverse_lazy('asociado:crearAsociado'))
        try:
            with transaction.atomic():
                
                # Variables modelo ASOCIADO
                envio_correo = request.POST.getlist('envioInfoCorreo')
                envio_mensaje = request.POST.getlist('envioInfoMensaje')
                envio_whatsapp = request.POST.getlist('envioInfoWhatsapp')

                # se guarda informacion en el modelo ASOCIADO
                obj = Asociado.objects.create(
                    tPersona = request.POST['tPersona'],
                    tAsociado = TipoAsociado.objects.get(pk = request.POST['tAsociado']),
                    estadoAsociado = request.POST['estadoAsociado'],
                    nombre = request.POST['nombre'].upper(),
                    apellido = request.POST['apellido'].upper(),
                    tipoDocumento = request.POST['tipoDocumento'],
                    numDocumento = request.POST['numDocumento'],
                    fechaExpedicion = request.POST['fechaExpedicion'],
                    mpioDoc = Municipio.objects.get(pk = int(request.POST['mpioDoc'])),
                    nacionalidad = request.POST['nacionalidad'].upper(),
                    genero = request.POST['genero'],
                    estadoCivil = request.POST['estadoCivil'],
                    email = request.POST['email'].lower(),
                    numResidencia = request.POST['numResidencia'] if request.POST['numResidencia'] else "",
                    numCelular = request.POST['numCelular'],
                    indicativoCelular = Pais.objects.get(pk = request.POST['indicativo']),
                    envioInfoCorreo = True if len(envio_correo) == 1 else False,
                    envioInfoMensaje = True if len(envio_mensaje) == 1 else False,
                    envioInfoWhatsapp = True if len(envio_whatsapp) == 1 else False,
                    nivelEducativo = request.POST['nivelEducativo'],
                    tituloPregrado = request.POST['tituloPregrado'].upper() if request.POST['tituloPregrado'] != "" else None,
                    tituloPosgrado = request.POST['tituloPosgrado'].upper() if request.POST['tituloPosgrado'] != "" else None,
                    fechaIngreso = request.POST['fechaIngreso'],
                    estadoRegistro = True,
                    tipoVivienda = request.POST['tipoVivienda'].upper(),
                    estrato = request.POST['estrato'],
                    direccion = request.POST['direccion'].upper(),
                    barrio = request.POST['barrio'].upper(),
                    deptoResidencia = Departamento.objects.get(pk = request.POST['deptoResidencia']),
                    mpioResidencia = Municipio.objects.get(pk = request.POST['mpioResidencia']),
                    fechaNacimiento = request.POST['fechaNacimiento'],
                    dtoNacimiento = Departamento.objects.get(pk = request.POST['dtoNacimiento']),
                    mpioNacimiento = Municipio.objects.get(pk = request.POST['mpioNacimiento']),
                    nombreRF = request.POST['nombreRF'].upper(),
                    parentesco = request.POST['parentesco'],
                    numContacto = request.POST['numContacto'],
                )

                # se guarda informacion en el modelo LABORAL
                objLaboral = Laboral.objects.create(
                    asociado = obj,
                    estadoRegistro = True,
                )

                # se guarda informacion en el modelo FINANCIERA
                objFinanciera = Financiera.objects.create(
                    asociado = obj,
                    estadoRegistro = True,
                )
                
                # Consulta del valor de la tarifa de aporte, bSocial y vinculacion
                tarifas = Tarifas.objects.filter(pk__in=[1,2,7])

                # Convierte la lista de objetos en un diccionario
                tarifas_dict = {t.pk: t for t in tarifas}

                objTarifaAporte = tarifas_dict.get(1)
                objTarifaBSocial = tarifas_dict.get(2)

                # se guarda informacion en el modelo TARIFA ASOCIADO
                objTarifaAsoc = TarifaAsociado.objects.create(
                    asociado = obj,
                    cuotaAporte = objTarifaAporte.valor,
                    cuotaBSocial = objTarifaBSocial.valor,
                    total = objTarifaAporte.valor + objTarifaBSocial.valor,
                    cuotaMascota = 0,
                    cuotaRepatriacion = 0,
                    cuotaSeguroVida = 0,
                    cuotaAdicionales = 0,
                    cuotaCoohopAporte = 0,
                    cuotaCoohopBsocial = 0,
                    cuotaConvenio = 0,
                    estadoAdicional = False,
                    estadoRegistro = True,
                )

                # Se selecciona la forma de pago de la vinculacion
                formaPago = request.POST['formaPago']
                
                # Variables modelo PARAMETROASOCIADO
                try:
                    primerMesPago = MesTarifa.objects.get(fechaInicio__lte = obj.fechaIngreso, fechaFinal__gte = obj.fechaIngreso)
                except MesTarifa.DoesNotExist:
                    primerMesPago = MesTarifa.objects.get(pk = 1)
                
                vinculacionForma = FormaPago.objects.get(pk = formaPago)
                servicioFuneraria = ServicioFuneraria.objects.get(pk = 1)

                # se guarda informacion en el modelo PARAMETROASOCIADO
                objParametro = ParametroAsociado.objects.create(
                    asociado = obj,
                    autorizaciondcto = False if obj.tAsociado.pk == 1 else True,
                    funeraria = servicioFuneraria,
                    primerMes = primerMesPago,
                    tarifaAsociado = objTarifaAsoc,
                    vinculacionFormaPago = vinculacionForma,
                    vinculacionCuotas = request.POST['cuotasPago'] if vinculacionForma.pk == 2 else None,
                    vinculacionValor = request.POST['valorCuota'] if vinculacionForma.pk == 2 else None,
                    vinculacionPendientePago = int(request.POST['valorCuota']) * int(request.POST['cuotasPago']) if vinculacionForma.pk == 2 else None,
                    estadoRegistro = True,
                )

                if vinculacionForma.pk != 2:
                    # Pk de la vinculacion adulto
                    mes_Pago = MesTarifa.objects.get(pk = 9995)

                    HistorialPagos.objects.create(
                        asociado = obj,
                        mesPago = mes_Pago,
                        fechaPago = obj.fechaIngreso,
                        valorPago = tarifas_dict.get(7).valor,
                        aportePago = 0,
                        bSocialPago = 0,
                        mascotaPago = 0,
                        repatriacionPago = 0,
                        seguroVidaPago = 0,
                        adicionalesPago = 0,
                        coohopAporte = 0,
                        coohopBsocial = 0,
                        convenioPago = 0,
                        creditoHomeElements = 0,
                        diferencia = 0,
                        formaPago = vinculacionForma,
                        userCreacion = request.user,
                        estadoRegistro = True
                    )
                
                messages.info(request, 'Asociado Creado Correctamente')
                return HttpResponseRedirect(reverse_lazy('asociado:verAsociado', args=[obj.pk]))
        
        except Exception as e:
            messages.error(request, f"Error al crear el asociado: {str(e)}")
            return HttpResponseRedirect(reverse_lazy('asociado:crearAsociado'))

class VerAsociado(DetailView):
    model = Asociado
    template_name = 'base/asociado/verAsociado.html'
    context_object_name = 'objAsociado'
    pk_url_kwarg = 'pkAsociado'

    def get_queryset(self):
        return Asociado.objects.select_related(
            'tAsociado',
            'mpioNacimiento',
            'mpioResidencia',
            'mpioDoc',
            'deptoResidencia',
            'dtoNacimiento',
            'indicativoCelular'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asociado = self.object

        context.update({
            'pkAsociado': asociado.pk,
            'query_dpto': Departamento.objects.values('id', 'nombre'),
            'objParentesco': Parentesco.objects.all().order_by('nombre'),
            'objEmpresa': TipoAsociado.objects.all(),
            'objServFuneraria': ServicioFuneraria.objects.all(),
            'objParametroAsociado': ParametroAsociado.objects.values(
                'id', 'funeraria', 'autorizaciondcto', 'primerMes'
            ).get(asociado=asociado.pk),
            'objMes': MesTarifa.objects.all(),
            'objLaboral': Laboral.objects.select_related('mpioTrabajo', 'dptoTrabajo').get(asociado=asociado.pk),
            'objFinanciero': Financiera.objects.get(asociado=asociado.pk),
            'pais_seleccionado': asociado.indicativoCelular.id if asociado.indicativoCelular else None,
            'vista': 1
        })
        return context

    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

class EditarAsociado(UpdateView):

    def post(self, request, *args, **kwargs):
        obj = Asociado.objects.get(pk = kwargs['pkAsociado'])
        obj.tPersona = request.POST['tPersona']
        obj.tAsociado = TipoAsociado.objects.get(pk = request.POST['tAsociado'])
        # se valida si cambia el estado del asociado
        if obj.estadoAsociado != request.POST['estadoAsociado']:
            # se valida si en el form se paso de activo a retiro
            if request.POST['estadoAsociado'] == 'RETIRO':
                obj.fechaRetiro = request.POST['fechaRetiro']
                obj.estadoAsociado = request.POST['estadoAsociado']
            # si pasa de retiro o inactivo a activo
            elif request.POST['estadoAsociado'] == 'ACTIVO':
                obj.fechaRetiro = None
                obj.estadoAsociado = request.POST['estadoAsociado']
            # INACTIVO
            else:
                obj.estadoAsociado = request.POST['estadoAsociado']
        elif obj.estadoAsociado == 'RETIRO':
            obj.fechaRetiro = request.POST['fechaRetiro']
        obj.nombre = request.POST['nombre'].upper()
        obj.apellido = request.POST['apellido'].upper()
        obj.tipoDocumento = request.POST['tipoDocumento']
        obj.numDocumento = request.POST['numDocumento']
        obj.fechaExpedicion = request.POST['fechaExpedicion']
        obj.mpioDoc = Municipio.objects.get(pk = int(request.POST['mpioDoc']))
        obj.nacionalidad = request.POST['nacionalidad'].upper()
        obj.genero = request.POST['genero']
        obj.estadoCivil = request.POST['estadoCivil']
        obj.email = request.POST['email']
        if request.POST['numResidencia'] != None:
            obj.numResidencia = request.POST['numResidencia']
        else:
            obj.numResidencia = None
        obj.indicativoCelular = Pais.objects.get(pk = request.POST['indicativo'])    
        obj.numCelular = request.POST['numCelular']
        envioCorreo = request.POST.getlist('envioInfoCorreo')
        envioMensaje = request.POST.getlist('envioInfoMensaje')
        envioWhatsapp = request.POST.getlist('envioInfoWhatsapp')

        if len(envioCorreo) == 1:
            obj.envioInfoCorreo = True
        else:
            obj.envioInfoCorreo = False
        if len(envioMensaje) == 1:
            obj.envioInfoMensaje = True
        else:
            obj.envioInfoMensaje = False
        if len(envioWhatsapp) == 1:
            obj.envioInfoWhatsapp = True
        else:
            obj.envioInfoWhatsapp = False
        obj.nivelEducativo = request.POST['nivelEducativo']
        if request.POST['tituloPregrado'] != "":
            obj.tituloPregrado = request.POST['tituloPregrado']
        if request.POST['tituloPosgrado'] != "":
            obj.tituloPosgrado = request.POST['tituloPosgrado']
        obj.fechaIngreso = request.POST['fechaIngreso']
        obj.estadoRegistro = True
        obj.tipoVivienda = request.POST['tipoVivienda'].upper()
        obj.estrato = request.POST['estrato']
        obj.direccion = request.POST['direccion'].upper()
        obj.barrio = request.POST['barrio'].upper()
        obj.deptoResidencia = Departamento.objects.get(pk = request.POST['deptoResidencia'])
        obj.mpioResidencia = Municipio.objects.get(pk = request.POST['mpioResidencia'])
        obj.fechaNacimiento = request.POST['fechaNacimiento']
        obj.dtoNacimiento = Departamento.objects.get(pk = request.POST['dtoNacimiento'])
        obj.mpioNacimiento = Municipio.objects.get(pk = request.POST['mpioNacimiento'])
        obj.nombreRF = request.POST['nombreRF']
        obj.parentesco = request.POST['parentesco']
        obj.numContacto = request.POST['numContacto']
        obj.save()
        messages.info(request, 'Información Modificada Correctamente')
        return HttpResponseRedirect(reverse_lazy('asociado:verAsociado', args=[kwargs['pkAsociado']]))

class EditarLaboral(CreateView):
    def post(self, request, *args, **kwargs):
        obj = Laboral.objects.get(asociado = kwargs['pkAsociado'])
        obj.asociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
        obj.ocupacion = request.POST['ocupacion'].upper()
        if request.POST['nombreEmpresa'] != "":
            obj.nombreEmpresa = request.POST['nombreEmpresa'].upper()
        else:
            obj.nombreEmpresa = None
        if request.POST['cargo'] != "":
            obj.cargo = request.POST['cargo'].upper()
        else:
            obj.cargo = None
        if request.POST['nomRepresenLegal'] != "":
            obj.nomRepresenLegal = request.POST['nomRepresenLegal'].upper()
        else:
            obj.nomRepresenLegal = None
        if request.POST['numDocRL'] != "":
            obj.numDocRL = request.POST['numDocRL']
        else:
            obj.numDocRL = None
        if request.POST['fechaInicio'] != "":
            obj.fechaInicio = request.POST['fechaInicio']
        else:
            obj.fechaInicio = None
        if request.POST['fechaTerminacion'] != "":
            obj.fechaTerminacion = request.POST['fechaTerminacion']
        else:
            obj.fechaTerminacion = None
        if request.POST['direccion'] != "":
            obj.direccion = request.POST['direccion'].upper()
        else:
            obj.direccion = None
        if int(request.POST['dptoTrabajo']) != 0:
            obj.dptoTrabajo = Departamento.objects.get(pk = request.POST['dptoTrabajo'])
            obj.mpioTrabajo = Municipio.objects.get(pk = request.POST['mpioTrabajo'])
        else:
            obj.dptoTrabajo = None
            obj.mpioTrabajo = None
        if request.POST['telefono'] != "" and request.POST['telefono'] != "0":
            obj.telefono = request.POST['telefono']
        else:
            obj.telefono = None
        obj.admRP = request.POST['admRP']
        obj.pep = request.POST['pep']
        if request.POST['activEcono'] != "":
            obj.activEcono = request.POST['activEcono'].upper()
        else:
            obj.activEcono = None
        if request.POST['ciiu'] != "":
            obj.ciiu = request.POST['ciiu']
        else:
            obj.ciiu = None
        if request.POST['banco'] != "":
            obj.banco = request.POST['banco'].upper()
        else:
            obj.banco = None
        if request.POST['numCuenta'] != "":
            obj.numCuenta = request.POST['numCuenta']
        else:
            obj.numCuenta = None
        obj.tipoCuenta = request.POST['tipoCuenta']
        obj.estadoRegistro = True
        obj.save()
        objFinanciera = Financiera.objects.get(asociado = kwargs['pkAsociado'])
        objFinanciera.asociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
        if request.POST['ingresosActPrin'] != "":
            objFinanciera.ingresosActPrin = int(request.POST['ingresosActPrin'].replace('.', ''))
        else:
            objFinanciera.ingresosActPrin = None
        if request.POST['otroIngreso1'] != "":
            objFinanciera.otroIngreso1 = int(request.POST['otroIngreso1'].replace('.', ''))
        else:
            objFinanciera.otroIngreso1 = None
        if request.POST['otroIngreso2'] != "":
            objFinanciera.otroIngreso2 = int(request.POST['otroIngreso2'].replace('.', ''))
        else:
            objFinanciera.otroIngreso2 = None
        if request.POST['egresos'] != "":
            objFinanciera.egresos = int(request.POST['egresos'].replace('.', ''))
        else:
            objFinanciera.egresos = None
        if request.POST['activos'] != "":
            objFinanciera.activos = int(request.POST['activos'].replace('.', ''))
        else:
            objFinanciera.activos = None
        if request.POST['pasivos'] != "":
            objFinanciera.pasivos = int(request.POST['pasivos'].replace('.', ''))
        else:
            objFinanciera.pasivos = None
        if request.POST['patrimonio'] != "":
            objFinanciera.patrimonio = int(request.POST['patrimonio'].replace('.', ''))
        else:
            objFinanciera.patrimonio = None
        objFinanciera.estadoRegistro = True
        objFinanciera.save()
        messages.info(request, 'Información Modificada Correctamente')
        return HttpResponseRedirect(reverse_lazy('asociado:verAsociado', args=[kwargs['pkAsociado']]))

class EditarParametroAsociado(CreateView):

    def post(self, request, *args, **kwargs):
        obj = ParametroAsociado.objects.get(asociado = kwargs['pkAsociado'])
        autorizacion = request.POST.getlist('autorizaciondcto')
        objAsociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
        if len(autorizacion) >= 1:
            obj.autorizaciondcto = True
            objAsociado.tAsociado = TipoAsociado.objects.get(pk = request.POST['empresaDcto'])
        else:
            obj.autorizaciondcto = False
            # Si se desactiva el check el asociado pasa a indenpendeinte
            objAsociado.tAsociado = TipoAsociado.objects.get(pk = 1)
        obj.funeraria = ServicioFuneraria.objects.get(pk = request.POST['servFuneraria'])
        obj.primerMes = MesTarifa.objects.get(pk = request.POST['primesMes'])
        obj.save()
        objAsociado.save()
        messages.info(request, 'Información Modificada Correctamente')
        return HttpResponseRedirect(reverse_lazy('asociado:verAsociado', args=[kwargs['pkAsociado']]))

class Beneficiarios(DetailView):
    model = Asociado
    template_name = 'base/asociado/listarBeneficiarios.html'
    context_object_name = 'queryAsociado'
    pk_url_kwarg = 'pkAsociado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        beneficiarios = Beneficiario.objects.filter(asociado = self.object.pk, estadoRegistro = True).select_related('parentesco','paisRepatriacion')
        context.update({
            'query': beneficiarios,
            'cuenta': beneficiarios.count(),
            'updateAsociado': 'yes',
            'pkAsociado': self.object.pk,
            'vista': 2
        })
        return context

class CrearBeneficiario(CreateView):
    form_class = BeneficiarioForm
    template_name = 'base/beneficiario/crearBeneficiario.html'

    def get(self, request, *args, **kwargs):
        query = Asociado.objects.get(pk = kwargs['pkAsociado'])
        return render(request, self.template_name, {'form':self.form_class, 'create':'yes', 'pkAsociado':kwargs['pkAsociado'], 'query':query})
    
    def post(self, request, *args, **kwargs):
        formulario = BeneficiarioForm(request.POST)
        if formulario.is_valid():
            obj = Beneficiario()
            obj.asociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
            obj.nombre = formulario.cleaned_data['nombre'].upper()
            obj.apellido = formulario.cleaned_data['apellido'].upper()
            obj.tipoDocumento = formulario.cleaned_data['tipoDocumento']
            obj.numDocumento = formulario.cleaned_data['numDocumento']
            obj.fechaNacimiento = formulario.cleaned_data['fechaNacimiento']
            obj.parentesco = formulario.cleaned_data['parentesco']
            paisRepatriacion = formulario.cleaned_data['paisRepatriacion']
            if paisRepatriacion is None:
                obj.repatriacion = False
                obj.estadoRegistro = True
                obj.fechaIngreso = formulario.cleaned_data['fechaIngreso']
                obj.save()
                messages.info(request, 'Beneficiario Creado Correctamente')
                return HttpResponseRedirect(reverse_lazy('asociado:beneficiario', args=[kwargs['pkAsociado']]))
            else:
                obj.paisRepatriacion = PaisRepatriacion.objects.get(nombre = formulario.cleaned_data['paisRepatriacion'])
                obj.repatriacion = True
                obj.estadoRegistro = True
                obj.fechaRepatriacion = formulario.cleaned_data['fechaRepatriacion']
                obj.ciudadRepatriacion = formulario.cleaned_data['ciudadRepatriacion'].upper()
                obj.fechaIngreso = formulario.cleaned_data['fechaIngreso']
                obj.save()
                # se busca el valor de la repatriacion, el pk es 4
                objTarifa = Tarifas.objects.get(pk = 4)
                # se busca la tarifa del asociado
                objTarifaAsociado = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
                objTarifaAsociado.cuotaRepatriacion = objTarifaAsociado.cuotaRepatriacion + objTarifa.valor
                objTarifaAsociado.total = objTarifaAsociado.total + objTarifa.valor
                objTarifaAsociado.save()
                messages.info(request, 'Beneficiario Creado Correctamente')
                return HttpResponseRedirect(reverse_lazy('asociado:beneficiario', args=[kwargs['pkAsociado']]))

class EditarBeneficiario(UpdateView):
    template_name = 'base/beneficiario/editarBeneficiario.html'

    def get(self, request, *args, **kwargs):
        form_update = get_object_or_404(Beneficiario, pk = kwargs['pk'])
        form = BeneficiarioForm(initial={'nombre':form_update.nombre,
                                     'apellido':form_update.apellido,
                                     'tipoDocumeno':form_update.tipoDocumento,
                                     'numDocumento':form_update.numDocumento,
                                     'fechaNacimiento':form_update.fechaNacimiento,
                                     'parentesco':form_update.parentesco,
                                     'paisRepatriacion':form_update.paisRepatriacion,
                                     'fechaRepatriacion':form_update.fechaRepatriacion,
                                     'ciudadRepatriacion':form_update.ciudadRepatriacion,
                                     'estadoRegistro':form_update.estadoRegistro,
                                     'fechaIngreso':form_update.fechaIngreso                                    
                                     })
        
        context = {
            'form': form,
            'pkAsociado': kwargs['pkAsociado'],
            'pk': kwargs['pk'],
            'paisRepatriacion': form_update.paisRepatriacion.id if form_update.paisRepatriacion else None,  # Valor de paisRepatriacion para el JS
        }

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        formulario = BeneficiarioForm(request.POST)
        if formulario.is_valid():
            obj = Beneficiario.objects.get(pk = kwargs['pk'])
            obj.nombre = formulario.cleaned_data['nombre'].upper()
            obj.apellido = formulario.cleaned_data['apellido'].upper()
            obj.tipoDocumento = formulario.cleaned_data['tipoDocumento']
            obj.numDocumento = formulario.cleaned_data['numDocumento']
            obj.fechaNacimiento = formulario.cleaned_data['fechaNacimiento']
            obj.parentesco = formulario.cleaned_data['parentesco']
            # Numero repatriaciones actuales
            numRepatriacion = Beneficiario.objects.filter(asociado = kwargs['pkAsociado'], repatriacion = True).count()
            paisRepatriacion = formulario.cleaned_data['paisRepatriacion']
            # se valida si pais repatriacion ya existe de antes
            if obj.paisRepatriacion:
                # se busca el valor de la repatriacion, pk = 4
                objTarifa = Tarifas.objects.get(pk = 4)
                objTarifaAsociado = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
                obj.estadoRegistro = True
                obj.fechaIngreso = formulario.cleaned_data['fechaIngreso']
                # validacion si quitan la repatriacion
                if paisRepatriacion is None:
                    obj.repatriacion = False
                    obj.paisRepatriacion = None
                    obj.fechaRepatriacion = None
                    obj.ciudadRepatriacion = ''
                    obj.save()
                    objTarifaAsociado.cuotaRepatriacion = objTarifaAsociado.cuotaRepatriacion - objTarifa.valor
                    objTarifaAsociado.total = objTarifaAsociado.total - objTarifa.valor
                    objTarifaAsociado.save()
                    messages.info(request, 'Registro Modificado Correctamente')
                    return HttpResponseRedirect(reverse_lazy('asociado:beneficiario', args=[kwargs['pkAsociado']]))
                # entra si cambia de repatriacion, de un pais a otro
                else:
                    obj.paisRepatriacion = PaisRepatriacion.objects.get(nombre = formulario.cleaned_data['paisRepatriacion'])
                    obj.repatriacion = True
                    obj.fechaRepatriacion = formulario.cleaned_data['fechaRepatriacion']
                    obj.ciudadRepatriacion = formulario.cleaned_data['ciudadRepatriacion'].upper()
                    obj.save()
                    objTarifaAsociado.save()
                    messages.info(request, 'Registro Modificado Correctamente')
                    return HttpResponseRedirect(reverse_lazy('asociado:beneficiario', args=[kwargs['pkAsociado']]))
            # valida si se agrega una repatriacion
            elif paisRepatriacion != None:
                obj.paisRepatriacion = PaisRepatriacion.objects.get(nombre = formulario.cleaned_data['paisRepatriacion'])
                obj.repatriacion = True
                obj.fechaRepatriacion = formulario.cleaned_data['fechaRepatriacion']
                obj.ciudadRepatriacion = formulario.cleaned_data['ciudadRepatriacion'].upper()
                obj.estadoRegistro = True
                obj.fechaIngreso = formulario.cleaned_data['fechaIngreso']
                obj.save()
                # Se busca el pk correspondiente a repatriacion
                objTarifa = Tarifas.objects.get(pk = 4)
                objTarifaAsociado = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
                if numRepatriacion > 0:
                    objTarifaAsociado.cuotaRepatriacion = objTarifaAsociado.cuotaRepatriacion + objTarifa.valor
                else:
                    objTarifaAsociado.cuotaRepatriacion = objTarifa.valor
                objTarifaAsociado.total = objTarifa.valor + objTarifaAsociado.total
                objTarifaAsociado.save()
                messages.info(request, 'Registro Modificado Correctamente')
                return HttpResponseRedirect(reverse_lazy('asociado:beneficiario', args=[kwargs['pkAsociado']]))
            # no se agrego repatriacion
            else:
                obj.repatriacion = False
                obj.fechaRepatriacion = None
                obj.estadoRegistro = True
                obj.fechaIngreso = formulario.cleaned_data['fechaIngreso']
                obj.save()
                messages.info(request, 'Registro Modificado Correctamente')
                return HttpResponseRedirect(reverse_lazy('asociado:beneficiario', args=[kwargs['pkAsociado']]))

class EliminarBeneficiario(UpdateView):
    model = Beneficiario
    template_name = 'base/beneficiario/eliminar.html'

    def get(self, request, *args, **kwargs):
        query = Beneficiario.objects.get(pk = kwargs['pk'])
        return render(request, self.template_name, {'pkAsociado':kwargs['pkAsociado'],'pk':kwargs['pk'], 'queryBeneficiario':query})

    def post(self, request, *args, **kwargs):
        obj = Beneficiario.objects.get(pk = kwargs['pk'])
        obj.estadoRegistro = False
        obj.fechaRetiro = date.today()
        if obj.repatriacion == True:
            obj.repatriacion = False
            objTarifa = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
            tarifaRepatriacion = Tarifas.objects.get(pk = 4)
            objTarifa.cuotaRepatriacion = objTarifa.cuotaRepatriacion - tarifaRepatriacion.valor
            objTarifa.total = objTarifa.total - tarifaRepatriacion.valor
            objTarifa.save()
        obj.save()
        messages.info(request, 'Registro Eliminado Correctamente')
        return HttpResponseRedirect(reverse_lazy('asociado:beneficiario', args=[kwargs['pkAsociado']]))

class Mascotas(DetailView):
    model = Asociado
    template_name = 'base/asociado/listarMascota.html'
    context_object_name = 'queryAsociado'
    pk_url_kwarg = 'pkAsociado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryMascotas = Mascota.objects.filter(asociado = self.object.pk, estadoRegistro = True)
        context.update({
            'query': queryMascotas,
            'pkAsociado': self.object.pk,
            'vista': 3
        })
        return context

class CrearMascota(CreateView):
    form_class = MascotaForm
    template_name = 'base/beneficiario/crearMascota.html'

    def get(self, request, *args, **kwargs):
        query = Asociado.objects.get(pk = kwargs['pkAsociado'])
        return render(request, self.template_name, {'form':self.form_class, 'create':'yes', 'pkAsociado':kwargs['pkAsociado'], 'query':query})
    
    def post(self, request, *args, **kwargs):
        formulario = MascotaForm(request.POST)
        if formulario.is_valid():
            obj = Mascota()
            obj.asociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
            obj.nombre = formulario.cleaned_data['nombre'].upper()
            obj.tipo = formulario.cleaned_data['tipo']
            obj.raza = formulario.cleaned_data['raza'].upper()
            obj.fechaNacimiento = formulario.cleaned_data['fechaNacimiento']
            obj.vacunasCompletas = formulario.cleaned_data['vacunasCompletas']
            obj.estadoRegistro = True
            obj.fechaIngreso = formulario.cleaned_data['fechaIngreso']
            obj.save()
            numMascotas = Mascota.objects.filter(asociado = kwargs['pkAsociado']).filter(estadoRegistro = True).count()
            objTarifaAsociado = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
            # Valor quemado de la mascota, pk = 3
            objTarifa = Tarifas.objects.get(pk = 3)
            objTarifaAsociado.cuotaMascota = numMascotas * objTarifa.valor
            objTarifaAsociado.total = objTarifaAsociado.total + objTarifa.valor
            objTarifaAsociado.save()
            messages.info(request, 'Mascota Creada Correctamente')
            return HttpResponseRedirect(reverse_lazy('asociado:mascota', args=[kwargs['pkAsociado']]))

class EditarMascota(UpdateView):
    template_name = 'base/beneficiario/editarMascota.html'

    def get(self, request, *args, **kwargs):
        form_update = get_object_or_404(Mascota, pk = kwargs['pk'])
        fechaNacFormateada = form_update.fechaNacimiento.strftime("%Y-%m-%d")
        fechaIngFormateada = form_update.fechaIngreso.strftime("%Y-%m-%d")
        form = MascotaForm(initial={'nombre':form_update.nombre,
                                     'tipo':form_update.tipo,
                                     'raza':form_update.raza,
                                     'tipoDocumeno':form_update.raza,
                                     'vacunasCompletas':form_update.vacunasCompletas,
                                     'fechaNacimiento':fechaNacFormateada,
                                     'fechaIngreso':fechaIngFormateada
                                     })
        return render(request, self.template_name, {'form':form,'pkAsociado':kwargs['pkAsociado'],'pk':kwargs['pk']})
    
    def post(self, request, *args, **kwargs):
        formulario = MascotaForm(request.POST)
        if formulario.is_valid():
            obj = Mascota.objects.get(pk = kwargs['pk'])
            obj.nombre = formulario.cleaned_data['nombre'].upper()
            obj.tipo = formulario.cleaned_data['tipo']
            obj.raza = formulario.cleaned_data['raza'].upper()
            obj.fechaNacimiento = formulario.cleaned_data['fechaNacimiento']
            obj.vacunasCompletas = formulario.cleaned_data['vacunasCompletas']
            obj.fechaIngreso = formulario.cleaned_data['fechaIngreso']
            obj.save()
            messages.info(request, 'Registro Editado Correctamente')
            return HttpResponseRedirect(reverse_lazy('asociado:mascota', args=[kwargs['pkAsociado']]))

class EliminarMascota(UpdateView):
    model = Mascota
    template_name = 'base/beneficiario/eliminar.html'

    def get(self, request, *args, **kwargs):
        queryMascota = Mascota.objects.get(pk = kwargs['pk'])
        return render(request, self.template_name, {'pkAsociado':kwargs['pkAsociado'],'pk':kwargs['pk'], 'queryMascota':queryMascota})

    def post(self, request, *args, **kwargs):
        obj = Mascota.objects.get(pk = kwargs['pk'])
        obj.estadoRegistro = False
        obj.fechaRetiro = date.today()
        obj.save()
        # Valor quemado de la mascota, pk = 3
        objTarifa = Tarifas.objects.get(pk = 3)
        objTarifaAsoc = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
        objTarifaAsoc.cuotaMascota = objTarifaAsoc.cuotaMascota - objTarifa.valor
        objTarifaAsoc.total = objTarifaAsoc.total - objTarifa.valor
        objTarifaAsoc.save()
        messages.info(request, 'Registro Eliminado Correctamente')
        return HttpResponseRedirect(reverse_lazy('asociado:mascota', args=[kwargs['pkAsociado']]))

class VerHistoricoAuxilio(DetailView):
    model = Asociado
    template_name = 'base/historico/listarHistoricoAuxilio.html'
    context_object_name = 'queryAsociado'
    pk_url_kwarg = 'pkAsociado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryHistorico = HistoricoAuxilio.objects.filter(asociado = self.object.pk, estadoRegistro = True).select_related('tipoAuxilio')
        context.update({
            'updateAsociado': 'yes',
            'pkAsociado': self.object.pk,
            'query': queryHistorico,
            'queryAsociado': self.object,
            'vista': 4
        })
        return context

class CrearAuxilio(CreateView):
    form_class = HistoricoAuxilioForm
    template_name = 'base/historico/crearAuxilio.html'

    def get(self, request, *args, **kwargs):
        query = Asociado.objects.get(pk = kwargs['pkAsociado'])
        return render(request, self.template_name, {'form':self.form_class, 'create':'yes', 'pkAsociado':kwargs['pkAsociado'], 'query':query})
    
    def post(self, request, *args, **kwargs):
        formulario = HistoricoAuxilioForm(request.POST)
        if formulario.is_valid():
            obj = HistoricoAuxilio()
            obj.fechaSolicitud = formulario.cleaned_data['fechaSolicitud']
            obj.asociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
            obj.tipoAuxilio = TipoAuxilio.objects.get(nombre = formulario.cleaned_data['tipoAuxilio'])
            obj.entidadBancaria = formulario.cleaned_data['entidadBancaria'].upper()
            obj.numCuenta = formulario.cleaned_data['numCuenta']
            obj.valor = obj.tipoAuxilio.valor
            obj.estado = formulario.cleaned_data['estado']
            obj.estadoRegistro = True
            obj.save()
            messages.info(request, 'Auxilio Creado Correctamente')
            return HttpResponseRedirect(reverse_lazy('asociado:historicoAuxilio', args=[kwargs['pkAsociado']]))

class DetalleAuxilio(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/historico/detalleAuxilio.html'
        obj = HistoricoAuxilio.objects.get(pk = kwargs['pk'])
        objParentesco = None
        if obj.tipoAuxilio.pk == 4 or obj.tipoAuxilio.pk == 5 or obj.tipoAuxilio.pk == 6 or obj.tipoAuxilio.pk == 9:
            objParentesco = Parentesco.objects.all().order_by('nombre')
        return render(request, template_name, {'obj':obj, 'objParentesco':objParentesco, 'pkAsociado':kwargs['pkAsociado'], 'pk': kwargs['pk']})

    def post(self, request, *args, **kwargs):
        obj = HistoricoAuxilio.objects.get(pk = kwargs['pk'])
        obj.estado = request.POST['estado']
        obj.fechaSolicitud = request.POST['fechaSolicitud']
        obj.entidadBancaria = request.POST['entidadBancaria'].upper()
        obj.numCuenta = request.POST['numCuenta']
        if obj.tipoAuxilio.pk == 4 or obj.tipoAuxilio.pk == 5 or obj.tipoAuxilio.pk == 6 or obj.tipoAuxilio.pk == 9:
            obj.nombre = request.POST['nombre'].upper()
            obj.numDoc = request.POST['numDoc']
            obj.parentesco = Parentesco.objects.get(pk = request.POST['parentesco'])
            obj.nivelEducativo = request.POST['nivelEducativo'].upper()
        if request.POST['anexoOne'] != '':
            obj.anexoOne = request.POST['anexoOne'].upper()
        else:
            obj.anexoOne = None
        if request.POST['anexoTwo'] != '':
            obj.anexoTwo = request.POST['anexoTwo'].upper()
        else:
            obj.anexoTwo = None
        if request.POST['anexoThree'] != '':
            obj.anexoThree = request.POST['anexoThree'].upper()
        else:
            obj.anexoThree = None
        if request.POST['anexoFour'] != '':
            obj.anexoFour = request.POST['anexoFour'].upper()
        else:
            obj.anexoFour = None
        if request.POST['anexoFive'] != '':
            obj.anexoFive = request.POST['anexoFive'].upper()
        else:
            obj.anexoFive = None
        if request.POST['anexoSix'] != '':
            obj.anexoSix = request.POST['anexoSix'].upper()
        else:
            obj.anexoSix = None
        if request.POST['anexoSeven'] != '':
            obj.anexoSeven = request.POST['anexoSeven'].upper()
        else:
            obj.anexoSeven = None
        if request.POST['anexoEight'] != '':
            obj.anexoEight = request.POST['anexoEight'].upper()
        else:
            obj.anexoEight = None
        if obj.estado == 'OTORGADO' and request.POST['fechaDesembolso'] != "":
            obj.fechaDesembolso = request.POST['fechaDesembolso']
            obj.observacion = None
        if obj.estado == 'DENEGADO':
            obj.fechaDesembolso = None
            obj.observacion = request.POST['observacion']
        if obj.estado == 'REVISION':
            obj.fechaDesembolso = None
            obj.observacion = None
        obj.save()

        messages.info(request, 'Información Actualizada Correctamente')
        return HttpResponseRedirect(reverse_lazy('asociado:historicoAuxilio', args=[kwargs['pkAsociado']]))

class EliminarAuxilio(UpdateView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/historico/eliminar.html'
        queryAuxilio = HistoricoAuxilio.objects.get(pk = kwargs['pk'])
        return render(request, template_name, {'pk':kwargs['pk'], 'pkAsociado':kwargs['pkAsociado'], 'queryAuxilio':queryAuxilio})

    def post(self, request, *args, **kwargs):
        queryAuxilio = HistoricoAuxilio.objects.get(pk = kwargs['pk'])
        queryAuxilio.estadoRegistro = False
        queryAuxilio.motivoEliminacion = request.POST['observacion']
        queryAuxilio.save()
        messages.info(request, 'Registro Eliminado Correctamente')
        return HttpResponseRedirect(reverse_lazy('asociado:historicoAuxilio', args=[kwargs['pkAsociado']]))
    
class VerHistoricoCredito(DetailView):
    model = Asociado
    template_name = 'base/historico/listarHistoricoCredito.html'
    context_object_name = 'queryAsociado'
    pk_url_kwarg = 'pkAsociado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryHistorico = HistoricoCredito.objects.prefetch_related(
                                Prefetch('codeudor_set', queryset=Codeudor.objects.all())
                            ).filter(asociado = self.object.pk).select_related('tasaInteres')
        context.update({
            'pkAsociado': self.object.pk,
            'query': queryHistorico,
            'queryAsociado': self.object,
            'vista': 5
        })
        return context
    
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)
    

@require_http_methods(["GET"])
def verPagosCredito(request, pk):
    if request.method == "GET":
        pagos = HistorialPagos.objects.filter(creditoId = pk)
        forma_pago = FormaPago.objects.all()
        total_pagado = pagos.aggregate(total=Sum("valorPago"))["total"] or 0
        return render(request, "base/historico/verPagosHistoricoCredito.html", {"data":pagos, "total_pagado":total_pagado, "forma_pago":forma_pago})

    
class CrearHistoricoCredito(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/historico/crearHistoricoCredito.html'
        form = HistoricoCreditoForm()
        queryAsociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
        queryFinanciera = queryAsociado.financiera.all().first()
        queryCodeudor = Codeudor.objects.filter()
        context = {
            'pkAsociado':kwargs['pkAsociado'],
            'form':form,
            'asociado':queryAsociado,
            'financiera':queryFinanciera,
            'tasasInteresCredito':TasasInteresCredito.objects.all()
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        formulario = HistoricoCreditoForm(request.POST)
        if formulario.is_valid():
            obj = HistoricoCredito()
            obj.fechaSolicitud = formulario.cleaned_data['fechaSolicitud']
            obj.asociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
            obj.lineaCredito = formulario.cleaned_data['lineaCredito']
            obj.amortizacion = formulario.cleaned_data['amortizacion']
            
            # cuando se utiliza en el form model ModelChoiceField, se obtiene es la instancia del objeto
            tasas = formulario.cleaned_data['tasaInteres'] 
            obj.tasaInteres = TasasInteresCredito.objects.get(pk = tasas.pk)

            obj.valor = formulario.cleaned_data['valor']
            obj.cuotas = formulario.cleaned_data['cuotas']
            obj.valorCuota = formulario.cleaned_data['valorCuota']
            obj.totalCredito = formulario.cleaned_data['totalCredito']
            obj.medioPago = formulario.cleaned_data['medioPago']
            obj.formaDesembolso = formulario.cleaned_data['formaDesembolso']
            obj.estado = formulario.cleaned_data['estado']
            obj.pendientePago = formulario.cleaned_data['totalCredito']
            obj.cuotasPagas = 0
            obj.estadoRegistro = True
            obj.save()
            messages.info(request, 'Registro Creado Correctamente')
            return HttpResponseRedirect(reverse_lazy('asociado:historicoCredito', args=[kwargs['pkAsociado']]))
        else:
            messages.error(request, 'Hubo un problema al guardar la información, comuniquese con el administrador del sitio.')
            return HttpResponseRedirect(reverse_lazy('asociado:historicoCredito', args=[kwargs['pkAsociado']]))

class EditarHistoricoCredito(ListView):
    def get(self, request, *args, **kwargs):
        form_update = get_object_or_404(HistoricoCredito, pk = kwargs['pk'])
        form = HistoricoCreditoForm(initial={'fechaSolicitud':form_update.fechaSolicitud,
                                            'valor':form_update.valor,
                                            'lineaCredito':form_update.lineaCredito,
                                            'amortizacion':form_update.amortizacion,
                                            'tasaInteres':form_update.tasaInteres,
                                            'cuotas':form_update.cuotas,
                                            'valorCuota':form_update.valorCuota,
                                            'totalCredito':form_update.totalCredito,
                                            'medioPago':form_update.medioPago,
                                            'formaDesembolso':form_update.formaDesembolso,
                                            'estado':form_update.estado,
                                            'banco':form_update.banco,
                                            'numCuenta':form_update.numCuenta,
                                            'tipoCuenta':form_update.tipoCuenta,
                                            })
        template_name = 'base/historico/editarHistoricoCredito.html'
        context = {
            'form':form,
            'pkAsociado':kwargs['pkAsociado'],
            'pk':kwargs['pk'],
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        formulario = HistoricoCreditoForm(request.POST)
        if formulario.is_valid():
            obj = HistoricoCredito.objects.get(pk = kwargs['pk'])
            obj.fechaSolicitud = formulario.cleaned_data['fechaSolicitud']
            obj.valor = formulario.cleaned_data['valor']
            obj.lineaCredito = formulario.cleaned_data['lineaCredito']
            obj.amortizacion = formulario.cleaned_data['amortizacion']
            obj.valorCuota = formulario.cleaned_data['valorCuota']
            obj.totalCredito = formulario.cleaned_data['totalCredito']
            tasa_interes = formulario.cleaned_data['tasaInteres']
            obj.tasaInteres = TasasInteresCredito.objects.get(pk = tasa_interes.pk)
            obj.medioPago = formulario.cleaned_data['medioPago']
            obj.cuotas = formulario.cleaned_data['cuotas']
            obj.formaDesembolso = formulario.cleaned_data['formaDesembolso']
            obj.estado = formulario.cleaned_data['estado']
            obj.banco = (formulario.cleaned_data['banco'] or '').upper()
            obj.tipoCuenta = formulario.cleaned_data['tipoCuenta']
            obj.numCuenta = formulario.cleaned_data['numCuenta']
            obj.save()
            messages.info(request, 'Registro Editado Correctamente')
            return HttpResponseRedirect(reverse_lazy('asociado:historicoCredito', args=[kwargs['pkAsociado']]))

class VerTarifaAsociado(ListView):
    template_name = 'base/historico/listarTarifaAsociado.html'

    def get_repatriacion_data(self, asociado):
        repatriacion_titular = RepatriacionTitular.objects.filter(asociado=asociado, estadoRegistro=True).first()
        repatriacion_valor = 0

        if repatriacion_titular:
            tarifa_repatriacion = Tarifas.objects.filter(pk=4).first()
            repatriacion_valor = tarifa_repatriacion.valor if tarifa_repatriacion else 0

        return repatriacion_titular, repatriacion_valor

    def get_credito_productos_data(self, asociado):
        queryset = HistoricoVenta.objects.filter(
            asociado=asociado,
            formaPago__in=['CREDITO', 'DESCUENTO NOMINA'],
            estadoRegistro=True,
            pendientePago__gt=0
        )
        total = 0
        for obj_venta in queryset:
            if (obj_venta.cuotas - obj_venta.cuotasPagas) == 1:
                obj_venta.valorCuotas = obj_venta.pendientePago
                total += obj_venta.valorCuotas
            else:
                if (obj_venta.cuotas - obj_venta.cuotasPagas) <= 0 and obj_venta.pendientePago > 0:
                    obj_venta.valorCuotas = obj_venta.pendientePago
                    total += obj_venta.valorCuotas
                elif obj_venta.pendientePago == 0:
                    obj_venta.valorCuotas = 0
                    total += obj_venta.valorCuotas
                elif obj_venta.pendientePago < obj_venta.valorCuotas and (obj_venta.cuotas - obj_venta.cuotasPagas) >= 1:
                    obj_venta.valorCuotas = obj_venta.pendientePago
                    total += obj_venta.valorCuotas
                else:
                    obj_venta.valorCuotas = obj_venta.valorCuotas
                    total += obj_venta.valorCuotas
        return queryset, total

    def get_credito_general_data(self, asociado):
        queryset = HistoricoCredito.objects.filter(
            asociado=asociado,
            estadoRegistro=True,
            pendientePago__gt=0,
            estado='OTORGADO'
        )
        total = 0
        for obj_credito in queryset:
            if (obj_credito.cuotas - obj_credito.cuotasPagas) == 1:
                obj_credito.valorCuota = obj_credito.pendientePago
                total += obj_credito.valorCuota
            else:
                if (obj_credito.cuotas - obj_credito.cuotasPagas) <= 0 and obj_credito.pendientePago > 0:
                    obj_credito.valorCuota = obj_credito.pendientePago
                    total += obj_credito.valorCuota
                elif obj_credito.pendientePago == 0:
                    obj_credito.valorCuota = 0
                    total += obj_credito.valorCuota
                elif obj_credito.pendientePago < obj_credito.valorCuota and (obj_credito.cuotas - obj_credito.cuotasPagas) >= 1:
                    obj_credito.valorCuota = obj_credito.pendientePago
                    total += obj_credito.valorCuota
                else:
                    obj_credito.valorCuota = obj_credito.valorCuota
                    total += obj_credito.valorCuota
        return queryset, total

    def get_vinculacion_data(self, asociado):
        param = ParametroAsociado.objects.filter(asociado=asociado, vinculacionPendientePago__gt=0).first()
        if param and param.vinculacionValor:
            cuotas_pendientes = round(param.vinculacionPendientePago / param.vinculacionValor) - param.vinculacionCuotas
        else:
            cuotas_pendientes = None
        return param, param.vinculacionValor if param else 0, cuotas_pendientes
    
    def get_valor_convenio_gasolina(self, asociado):
        convenio_gasolina = 0
        query_convenio = ConvenioHistoricoGasolina.objects.filter(asociado=asociado, estado_registro=True)
        if query_convenio:
            for obj in query_convenio:
                if obj.pendiente_pago > 0:
                    convenio_gasolina += obj.pendiente_pago
        return convenio_gasolina

    def get(self, request, *args, **kwargs):
        asociado = get_object_or_404(Asociado, pk=kwargs['pkAsociado'])
        tarifa_asociado = TarifaAsociado.objects.select_related('asociado').get(asociado=asociado)

        convenios = ConveniosAsociado.objects.filter(asociado=asociado, estadoRegistro=True)

        valor_convenio_gasolina = self.get_valor_convenio_gasolina(asociado)

        adicional = tarifa_asociado.cuotaAdicionales > 0

        repatriacion_titular, repatriacion_valor = self.get_repatriacion_data(asociado)
        
        if repatriacion_titular:
            tarifa_asociado.cuotaRepatriacion = (tarifa_asociado.cuotaRepatriacion or None) - repatriacion_valor

        credito_productos_qs, total_credito_productos = self.get_credito_productos_data(asociado)
        credito_general_qs, total_credito_general = self.get_credito_general_data(asociado)
        vinculacion_param, cuota_vinculacion, vinculacion_cuotas_pte = self.get_vinculacion_data(asociado)

        total_tarifa = tarifa_asociado.total + total_credito_productos + total_credito_general + cuota_vinculacion + valor_convenio_gasolina

        context = {
            'updateAsociado': 'yes',
            'pkAsociado': asociado.pk,
            'query': tarifa_asociado,
            'adicional': adicional,
            'queryRepatriacionTitular': repatriacion_titular,
            'repatriacion': repatriacion_valor,
            'pk': repatriacion_titular.pk if repatriacion_titular else 0,
            'queryConvenio': convenios,
            'vista': 8,
            'query_credito_prod': credito_productos_qs,
            'queryCredito': credito_general_qs,
            'queryVinculacion': vinculacion_param,
            'vinculacionCuotasPte': vinculacion_cuotas_pte,
            'cuotaGasolina': valor_convenio_gasolina,
            'totalTarifaAsociado': total_tarifa
        }
        return render(request, self.template_name, context)


@require_http_methods(["POST", "GET"])
def EditarConvenioGasolina(request, pkConvenio):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            registros = data.get("registros", [])
            convenio = ConveniosAsociado.objects.get(pk=pkConvenio)

            nuevos_ids = []

            for item in registros:
                mes_id = item.get("mes_id")
                valor = item.get("valor")
                if mes_id and valor:
                    nuevo = ConvenioHistoricoGasolina.objects.create(
                        convenio=convenio,
                        asociado=convenio.asociado,
                        mes_tarifa_id=mes_id,
                        valor_pagar=valor,
                        pendiente_pago=valor,
                        estado_registro=True
                    )
                    nuevos_ids.append({
                        "id": nuevo.id,
                        "mes_id": mes_id,
                        "valor": valor
                    })

            return JsonResponse({"success": True, "nuevos": nuevos_ids, "message": "Datos guardados correctamente."})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    else:
        convenio = ConveniosAsociado.objects.get(pk = pkConvenio)
        meses = MesTarifa.objects.filter(pk__gte = convenio.primerMes.pk, pk__lte = 9000).values("id", "concepto")
        meses_seleccionados = ConvenioHistoricoGasolina.objects.filter(convenio = pkConvenio).values_list('mes_tarifa_id', flat=True)
        meses = meses.exclude(id__in=meses_seleccionados)
        historico = ConvenioHistoricoGasolina.objects.filter(convenio = pkConvenio)
        return render(request, 'base/historico/convenio_gasolina.html', {"meses":list(meses), "pkConvenio":pkConvenio, "historico":historico})


@require_http_methods(["POST"])
def EliminarDetalleGasolina(request, pkConvenio):
    if request.method == "POST":
        detalle = get_object_or_404(ConvenioHistoricoGasolina, pk=pkConvenio)
        detalle.delete()
        return JsonResponse({
            'status': 'ok'
            })
    else:
        return JsonResponse({'error':"Metodo no permitido"})


class CrearAdicionalAsociado(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/historico/crearAdicional.html'
        return render(request, template_name, {'pkAsociado':kwargs['pkAsociado'],'create':'yes'})

    def post(self, request, *args, **kwargs):
        cuotaAdicional = request.POST['cuotaAdicionales']
        fechaInicioAdicional = request.POST['fechaInicioAdicional']
        objTarifa = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
        objTarifa.cuotaAdicionales = cuotaAdicional
        objTarifa.fechaInicioAdicional = fechaInicioAdicional
        objTarifa.conceptoAdicional = request.POST['concepto'].upper()
        objTarifa.total = objTarifa.total + int(cuotaAdicional)
        objTarifa.estadoAdicional = True
        objTarifa.save()
        messages.info(request, 'Información Registrada Correctamente')
        return HttpResponseRedirect(reverse_lazy('asociado:tarifaAsociado', args=[kwargs['pkAsociado']]))

class EditarAdicionalAsociado(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/historico/crearAdicional.html'
        query = TarifaAsociado.objects.get(pk = kwargs['pk'])
        return render(request, template_name, {'pkAsociado':kwargs['pkAsociado'],'pk':kwargs['pk'] ,'update':'yes', 'query':query})

    def post(self, request, *args, **kwargs):
        cuotaAdicional = request.POST['cuotaAdicionales']
        valorAnterior = request.POST['adicionalAnterior']
        fechaInicioAdicional = request.POST['fechaInicioAdicional']
        objTarifa = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
        objTarifa.cuotaAdicionales = cuotaAdicional
        objTarifa.conceptoAdicional = request.POST['concepto'].upper()
        objTarifa.total = objTarifa.total + int(cuotaAdicional) - int(valorAnterior)
        objTarifa.fechaInicioAdicional = fechaInicioAdicional
        objTarifa.save()
        messages.info(request, 'Registo Modificado Correctamente')
        return HttpResponseRedirect(reverse_lazy('asociado:tarifaAsociado', args=[kwargs['pkAsociado']]))

class EliminarAdicionalAsociado(UpdateView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/asociado/eliminarAdicional.html'
        query = TarifaAsociado.objects.only('cuotaAdicionales', 'id', 'fechaInicioAdicional').get(pk = kwargs['pk'])
        context = {'query': query,
                'pk': kwargs['pk'],
                'pkAsociado': kwargs['pkAsociado'],
                }
        return render(request, template_name, context)
    
    def post(self, request, *args, **kwargs):
        obj = TarifaAsociado.objects.get(pk = kwargs['pk'])
        obj.total = obj.total - obj.cuotaAdicionales
        obj.cuotaAdicionales = 0
        obj.fechaFinAdicional = date.today()
        obj.estadoAdicional = False
        obj.save()
        messages.info(request, 'Registro Eliminado Correctamente')
        return HttpResponseRedirect(reverse_lazy('asociado:tarifaAsociado', args=[kwargs['pkAsociado']]))

class VerSeguroVida(DetailView):
    model = Asociado
    template_name = 'base/asociado/listarSeguroVida.html'
    context_object_name = 'queryAsociado'
    pk_url_kwarg = 'pkAsociado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        querySeguroVida = HistoricoSeguroVida.objects.filter(asociado = self.object.pk)
        context.update({
            'pkAsociado': self.object.pk,
            'query': querySeguroVida,
            'queryAsociado': self.object,
            'vista': 6
        }) 
        return context

class CrearSeguroVida(CreateView):
    form_class = HistoricoSeguroVidaForm
    template_name = 'base/historico/crearSeguroVida.html'

    def get(self, request, *args, **kwargs):
        query = Asociado.objects.get(pk = kwargs['pkAsociado'])
        return render(request, self.template_name, {'form':self.form_class, 'create':'yes', 'pkAsociado':kwargs['pkAsociado'], 'query':query})
    
    def post(self, request, *args, **kwargs):
        formulario = HistoricoSeguroVidaForm(request.POST)
        if formulario.is_valid():
            obj = HistoricoSeguroVida()
            obj.asociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
            obj.valorPago = formulario.cleaned_data['valorPago']
            obj.fechaIngreso = formulario.cleaned_data['fechaIngreso']
            obj.estadoRegistro = True
            obj.save()
            objTarifaAsociado = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
            objTarifaAsociado.cuotaSeguroVida = obj.valorPago
            objTarifaAsociado.total = objTarifaAsociado.total + obj.valorPago
            objTarifaAsociado.save()
            messages.info(request, 'Registro Creado Correctamente')
            return HttpResponseRedirect(reverse_lazy('asociado:seguroVida', args=[kwargs['pkAsociado']]))

class EditarSeguroVida(UpdateView):
    template_name = 'base/historico/crearSeguroVida.html'

    def get(self, request, *args, **kwargs):
        form_update = get_object_or_404(HistoricoSeguroVida, pk = kwargs['pk'])
        fechaIngFormateada = form_update.fechaIngreso.strftime("%Y-%m-%d")
        if form_update.fechaRetiro != None:
            fechaRetFormateada = form_update.fechaRetiro.strftime("%Y-%m-%d")
            form = HistoricoSeguroVidaForm(initial={'valorPago':form_update.valorPago,
                                                'fechaIngreso':fechaIngFormateada,
                                                'fechaRetiro':fechaRetFormateada,
                                                })
        else:
            form = HistoricoSeguroVidaForm(initial={'valorPago':form_update.valorPago,
                                                'fechaIngreso':fechaIngFormateada,
                                                })
        return render(request, self.template_name, {'form':form,'pkAsociado':kwargs['pkAsociado'],'pk':kwargs['pk']})
    
    def post(self, request, *args, **kwargs):
        formulario = HistoricoSeguroVidaForm(request.POST)
        if formulario.is_valid():
            obj = HistoricoSeguroVida.objects.get(pk = kwargs['pk'])
            # se guarda esta variable, en caso que ponga fecha retiro y el usuario ponga valor en 0, le pueda restar el valor que estaba al total de la tarifa del asociado
            valorActual = obj.valorPago
            obj.valorPago = formulario.cleaned_data['valorPago']
            obj.fechaIngreso = formulario.cleaned_data['fechaIngreso']
            objTarifaAsociado = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
            # si se ingresa fecha de retiro, se inactiva y se resta al valor de la tarifa
            if formulario.cleaned_data['fechaRetiro'] != None:
                obj.fechaRetiro = formulario.cleaned_data['fechaRetiro']
                obj.estadoRegistro = False
                objTarifaAsociado.cuotaSeguroVida = 0
                objTarifaAsociado.total = objTarifaAsociado.total - valorActual
                objTarifaAsociado.save()
                obj.save()
                messages.info(request, 'Registro Editado Correctamente')
                return HttpResponseRedirect(reverse_lazy('asociado:seguroVida', args=[kwargs['pkAsociado']]))
            else:
                obj.save()
            # validaciones si aumenta o disminuye el valor del seguro de vida
            objTarifaAsociado.cuotaSeguroVida = obj.valorPago
            if valorActual > obj.valorPago:
                diferencia = valorActual - obj.valorPago
                objTarifaAsociado.total = objTarifaAsociado.total - diferencia 

            else:
                diferencia = obj.valorPago - valorActual   
                objTarifaAsociado.total = objTarifaAsociado.total + diferencia 
            objTarifaAsociado.save()
            messages.info(request, 'Registro Editado Correctamente')
            return HttpResponseRedirect(reverse_lazy('asociado:seguroVida', args=[kwargs['pkAsociado']]))

class VerCoohoperativitos(DetailView):
    model = Asociado
    template_name = 'base/beneficiario/listarCoohoperativitos.html'
    context_object_name = 'queryAsociado'
    pk_url_kwarg = 'pkAsociado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryCoohoperativitos = Coohoperativitos.objects.filter(asociado = self.object.pk, estadoRegistro=True)
        context.update({
            'updateAsociado': 'yes',
            'pkAsociado': self.object.pk,
            'query': queryCoohoperativitos,
            'queryAsociado': self.object,
            'vista': 7
        })
        return context

class CrearCoohoperativito(UpdateView):
    form_class = CoohoperativitoForm
    template_name = 'base/beneficiario/crearCoohoperativito.html'

    def get(self, request, *args, **kwargs):
        query = Asociado.objects.get(pk = kwargs['pkAsociado'])
        return render(request, self.template_name, {'form':self.form_class, 'create':'yes', 'pkAsociado':kwargs['pkAsociado'], 'query':query})
    
    def post(self, request, *args, **kwargs):
        formulario = CoohoperativitoForm(request.POST)
        if formulario.is_valid():
            obj = Coohoperativitos()
            obj.asociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
            obj.nombre = formulario.cleaned_data['nombre'].upper()
            obj.apellido = formulario.cleaned_data['apellido'].upper()
            obj.tipoDocumento = formulario.cleaned_data['tipoDocumento']
            obj.numDocumento = formulario.cleaned_data['numDocumento']
            obj.fechaNacimiento = formulario.cleaned_data['fechaNacimiento']
            obj.estadoRegistro = True
            obj.fechaIngreso = formulario.cleaned_data['fechaIngreso']
            obj.save()
            # se consulta cuantos coohoperativitos tiene actualmente
            numCoohoperativitos = Coohoperativitos.objects.filter(asociado = kwargs['pkAsociado'], estadoRegistro = True).count()
            objTarifaAsociado = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
            # valor de aportes coohoperativitos
            objTarifaCooho = Tarifas.objects.get(pk = 6)
            # valor de b social coohoperativitos
            objTarifaCoohoBSocial = Tarifas.objects.get(pk = 5)
            objTarifaAsociado.cuotaCoohopAporte = objTarifaCooho.valor * numCoohoperativitos
            objTarifaAsociado.cuotaCoohopBsocial = objTarifaCoohoBSocial.valor * numCoohoperativitos
            objTarifaAsociado.total = objTarifaAsociado.total + objTarifaCooho.valor + objTarifaCoohoBSocial.valor
            objTarifaAsociado.save()
            messages.info(request, 'Registro Creado Correctamente')
            return HttpResponseRedirect(reverse_lazy('asociado:coohoperativitos', args=[kwargs['pkAsociado']]))

class EditarCoohoperativito(UpdateView):
    template_name = 'base/beneficiario/crearCoohoperativito.html'

    def get(self, request, *args, **kwargs):
        form_update = get_object_or_404(Coohoperativitos, pk = kwargs['pk'])
        form = CoohoperativitoForm(initial={'nombre':form_update.nombre,
                                            'apellido':form_update.apellido,
                                            'tipoDocumento':form_update.tipoDocumento,
                                            'numDocumento':form_update.numDocumento,
                                            'fechaNacimiento':form_update.fechaNacimiento,
                                            'fechaIngreso':form_update.fechaIngreso,
                                            })
        return render(request, self.template_name, {'form':form,'pkAsociado':kwargs['pkAsociado'],'pk':kwargs['pk']})
    
    def post(self, request, *args, **kwargs):
        formulario = CoohoperativitoForm(request.POST)
        if formulario.is_valid():
            obj = Coohoperativitos.objects.get(pk = kwargs['pk'])
            obj.nombre = formulario.cleaned_data['nombre'].upper()
            obj.apellido = formulario.cleaned_data['apellido'].upper()
            obj.tipoDocumento = formulario.cleaned_data['tipoDocumento']
            obj.numDocumento = formulario.cleaned_data['numDocumento']
            obj.fechaNacimiento = formulario.cleaned_data['fechaNacimiento']
            obj.fechaIngreso = formulario.cleaned_data['fechaIngreso']
            obj.save()
            messages.info(request, 'Registro Modificado Correctamente')
            return HttpResponseRedirect(reverse_lazy('asociado:coohoperativitos', args=[kwargs['pkAsociado']]))

class EliminarCoohoperativito(UpdateView):
    model = Coohoperativitos
    template_name = 'base/beneficiario/eliminar.html'

    def get(self, request, *args, **kwargs):
        queryCoohop = Coohoperativitos.objects.get(pk = kwargs['pk'])
        tarifaCooh = Tarifas.objects.filter(id__in=[5,6]).aggregate(total_valor=Sum('valor')) 
        return render(request, self.template_name, {'pkAsociado':kwargs['pkAsociado'],'pk':kwargs['pk'], 'queryCoohop':queryCoohop, 'tarifaCooh':tarifaCooh})

    def post(self, request, *args, **kwargs):
        obj = Coohoperativitos.objects.get(pk = kwargs['pk'])
        obj.estadoRegistro = False
        obj.fechaRetiro = date.today()
        obj.save()
        # Valor quemado de la b social coohoperativios, pk = 5
        objTarifaBsocial = Tarifas.objects.get(pk = 5)
        # Valor quemado del aporte coohoperativios, pk = 6
        objTarifaAporte = Tarifas.objects.get(pk = 6)
        objTarifaAsoc = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
        objTarifaAsoc.cuotaCoohopAporte = objTarifaAsoc.cuotaCoohopAporte - objTarifaAporte.valor
        objTarifaAsoc.cuotaCoohopBsocial = objTarifaAsoc.cuotaCoohopBsocial - objTarifaBsocial.valor
        objTarifaAsoc.total = objTarifaAsoc.total - objTarifaBsocial.valor - objTarifaAporte.valor
        objTarifaAsoc.save()
        messages.info(request, 'Registro Eliminado Correctamente')
        return HttpResponseRedirect(reverse_lazy('asociado:coohoperativitos', args=[kwargs['pkAsociado']]))

class VerHistorialPagos(DetailView):
    model = Asociado
    template_name = 'base/historico/listarHistorialPago.html'
    context_object_name = 'queryAsociado'
    pk_url_kwarg = 'pkAsociado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryPagos = HistorialPagos.objects.filter(asociado = self.object.pk).select_related('formaPago','mesPago', 'convenio_gasolina_id').order_by('fechaPago','id')
        context.update({
            'updateAsociado': 'yes',
            'pkAsociado': self.object.pk,
            'query': queryPagos,
            'queryAsociado': self.object,
            'vista': 9
        })
        return context

class DetalleHistorialPago(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/historico/detallePago.html'
        query = HistorialPagos.objects.get(pk = kwargs['pk'])
        return render(request, template_name, {'query':query})

class DescargarFormatos(DetailView):
    model = Asociado
    template_name = 'base/asociado/formatos.html'
    context_object_name = 'query'
    pk_url_kwarg = 'pkAsociado'

    def get_queryset(self):
        return Asociado.objects.select_related(
                    'tAsociado',
                    'mpioDoc',
                    'deptoResidencia',
                    'dtoNacimiento',
                    'mpioNacimiento',
                    'mpioResidencia'
                )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asociado = self.object
        fecha_actual = date.today()

        try:
            obj_financiera = Financiera.objects.get(asociado=asociado)
            obj_parametro = ParametroAsociado.objects.get(asociado=asociado)
            obj_laboral = Laboral.objects.select_related('mpioTrabajo', 'dptoTrabajo').get(asociado=asociado)
            
            beneficiarios = Beneficiario.objects.filter(
                asociado=asociado,
                estadoRegistro=True
            ).select_related('paisRepatriacion', 'parentesco')

            mascotas = Mascota.objects.filter(asociado=asociado, estadoRegistro=True)

            context.update({
                'updateAsociado': 'yes',
                'pkAsociado': asociado.pk,
                'residenciaExiste': 'yes',
                'queryLaboral': obj_laboral,
                'actualizacion': asociado.fechaIngreso != fecha_actual,
                'objFinanciera': obj_financiera,
                'fechaActual': fecha_actual,
                'objParametroAsociado': obj_parametro,
                'objBeneficiario': beneficiarios,
                'cuentaBeneficiario': beneficiarios.count(),
                'objMascota': mascotas,
                'cuentaMascota': mascotas.count(),
                'vista': 10
            })
        except (Financiera.DoesNotExist, ParametroAsociado.DoesNotExist, Laboral.DoesNotExist):
            messages.warning(self.request, 'Información incompleta para descargar formatos.')
            context.update({
                'mensaje': 'yes',
                'pkAsociado': asociado.pk,
                'vista': 10
            })

        return context

# Descarga Formato Auxilios
class ModalFormato(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/asociado/formato2.html'

        # Formato Auxilio
        if kwargs['formato'] == 3:
            objAuxilio = HistoricoAuxilio.objects.filter(asociado = kwargs['pkAsociado'], estado__in=['REVISION', 'OTORGADO'])
            return render(request, template_name,{'pkAsociado':kwargs['pkAsociado'], 'formato':kwargs['formato'], 'objAuxilio':objAuxilio})
        # Formato Extracto
        elif kwargs['formato'] == 4:
            objParametroAsoc = ParametroAsociado.objects.get(asociado = kwargs['pkAsociado'])
            objMes = MesTarifa.objects.filter(pk__gte = objParametroAsoc.primerMes.pk)
            return render(request, template_name,{'pkAsociado':kwargs['pkAsociado'], 'formato':kwargs['formato'], 'objMes':objMes})
        # Formato Otorgamiento de credito
        elif kwargs['formato'] == 5:
            queryHistoricoCredito = HistoricoCredito.objects.filter(asociado = kwargs['pkAsociado']).order_by('fechaSolicitud')

            # Agregamos prefetch_related para obtener todos los codeudores asociados a cada historicoCredito
            queryHistoricoCredito = queryHistoricoCredito.prefetch_related(
                Prefetch('codeudor_set', queryset=Codeudor.objects.all(), to_attr='codeudores')
            )
            queryAsociado = Asociado.objects.get(pk=kwargs['pkAsociado'])
            queryParametroAsoc = ParametroAsociado.objects.filter(asociado = kwargs['pkAsociado']).values('autorizaciondcto','asociado__tAsociado__concepto').first()
            queryLaboral = Laboral.objects.get(asociado = kwargs['pkAsociado'])
            fechaActual = date.today()
            context = {
                'pkAsociado': kwargs['pkAsociado'],
                'formato': kwargs['formato'],
                'query': queryHistoricoCredito,
                'queryAsociado': queryAsociado,
                'fechaActual': fechaActual,
                'queryLab': queryLaboral,
                'queryParametroAsoc': queryParametroAsoc,
            }
            return render(request, template_name, context)


# Descarga Formato Auxilios
class GenerarFormato(ListView):
    @medir_rendimiento('formato_extracto')
    def get(self, request, *args, **kwargs):
        template_name = 'base/asociado/generar.html'
        fechaActual = date.today()
        objAsoc = Asociado.objects.select_related('mpioResidencia').get(pk = kwargs['pkAsociado'])

        # Formato 3
        if kwargs['formato'] == 3:
            objLaboral = Laboral.objects.get(asociado = kwargs['pkAsociado'])
            objFinanciera = Financiera.objects.get(asociado = kwargs['pkAsociado'])
            objAuxilio = HistoricoAuxilio.objects.get(pk = kwargs['pk'])
            return render(request, template_name,{'pkAsociado':kwargs['pkAsociado'], 'fechaActual':fechaActual,'objAsoc':objAsoc, 'objLaboral':objLaboral, 'objFinanciera':objFinanciera, 'objAuxilio':objAuxilio, 'formato':kwargs['formato']})
        
        # Formato 4
        elif kwargs['formato'] == 4:
            id_asociado = kwargs['pkAsociado']
            saldos = 'saldos' in request.GET
            mes = MesTarifa.objects.get(pk = request.GET['mes'])
            formato = kwargs['formato']
            context = obtenerValorExtracto(id_asociado, saldos, mes)
            context["objAsoc"] = objAsoc
            context["formato"] = formato
            return render(request, template_name, context)

class UtilidadesAsociado(ListView):
    model = Asociado
    template_name = 'base/asociado/utilidades.html'

class CrearRepatriacionTitular(ListView):
    form_class = RepatriacionTitularForm
    template_name = 'base/asociado/repatriacionTitular.html'

    def get(self, request, *args, **kwargs):

        context = {
            'form': self.form_class,
            'create': 'yes',
            'pkAsociado': kwargs['pkAsociado'],
            }

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            objRepat = RepatriacionTitular(
                asociado=get_object_or_404(Asociado, pk=kwargs['pkAsociado']),
                paisRepatriacion=form.cleaned_data['paisRepatriacion'],
                fechaRepatriacion=form.cleaned_data['fechaRepatriacion'],
                ciudadRepatriacion=form.cleaned_data['ciudadRepatriacion'],
                estadoRegistro=True,
            )
            objTarifa = TarifaAsociado.objects.get(pk=kwargs['pkAsociado'])
            TarifaRep = Tarifas.objects.get(pk=4)
            objTarifa.cuotaRepatriacion+=TarifaRep.valor
            objTarifa.total += TarifaRep.valor
            objTarifa.save()
            objRepat.save()
            messages.info(request, 'Repatriación del Titular registrada correctamente.')
            return HttpResponseRedirect(reverse_lazy('asociado:tarifaAsociado', args=[kwargs['pkAsociado']]))
        else:
            # Si el formulario es inválido, re-renderiza el formulario con errores
            return render(request, self.template_name, {
                'form': form,
                'create': 'yes',
                'pkAsociado': kwargs['pkAsociado'],
            })

class VerRepatriacionTitular(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/asociado/verRepatriacionTitular.html'
        form_update = get_object_or_404(RepatriacionTitular, pk = kwargs['pk'])
        form = RepatriacionTitularForm(initial={'fechaRepatriacion':form_update.fechaRepatriacion,
                                                'paisRepatriacion':form_update.paisRepatriacion,
                                                'ciudadRepatriacion':form_update.ciudadRepatriacion,
                                    })
        return render(request, template_name, {'form':form, 'pk':kwargs['pk'], 'pkAsociado':kwargs['pkAsociado']})
    
    def post(self, request, *args, **kwargs):
        form = RepatriacionTitularForm(request.POST)
        if form.is_valid():
            obj = RepatriacionTitular.objects.get(pk = kwargs['pk'])
            obj.fechaRepatriacion = form.cleaned_data['fechaRepatriacion']
            obj.paisRepatriacion = form.cleaned_data['paisRepatriacion']
            obj.ciudadRepatriacion = form.cleaned_data['ciudadRepatriacion']
            obj.save()
            messages.info(request, 'Registro editado correctamente')
            return HttpResponseRedirect(reverse_lazy('asociado:tarifaAsociado', args=[kwargs['pkAsociado']]))

class EliminarRepatriacionTitular(UpdateView):
    template_name = 'base/beneficiario/eliminar.html'

    def get(self, request, *args, **kwargs):
        query = RepatriacionTitular.objects.get(pk = kwargs['pk'])
        return render(request, self.template_name, {'pk':kwargs['pk'], 'pkAsociado':kwargs['pkAsociado'] ,'queryRepatriacionTitular':query})

    def post(self, request, *args, **kwargs):
        obj = RepatriacionTitular.objects.get(pk = kwargs['pk'])
        obj.estadoRegistro = False
        obj.fechaRetiro = date.today()
        obj.save()
        # Valor quemado de la repatriacion, pk = 4
        objTarifa = Tarifas.objects.get(pk = 4)
        objTarifaAsoc = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
        objTarifaAsoc.cuotaRepatriacion = objTarifaAsoc.cuotaRepatriacion - objTarifa.valor
        objTarifaAsoc.total = objTarifaAsoc.total - objTarifa.valor
        objTarifaAsoc.save()
        messages.info(request, 'Registro Eliminado Correctamente')
        return HttpResponseRedirect(reverse_lazy('asociado:tarifaAsociado', args=[kwargs['pkAsociado']]))
    
class CrearConvenio(ListView):
    form_class = ConvenioAsociadoForm
    template_name = 'base/asociado/crearConvenio.html'

    def get(self, request, *args, **kwargs):

        context = {
            'form': self.form_class,
            'create': 'yes',
            'pkAsociado': kwargs['pkAsociado'],
            }

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            objConvenio = ConveniosAsociado(
                asociado=get_object_or_404(Asociado, pk=kwargs['pkAsociado']),
                convenio=form.cleaned_data['convenio'],
                fechaIngreso=form.cleaned_data['fechaIngreso'],
                primerMes=MesTarifa.objects.get(concepto = form.cleaned_data['primerMes']),
                estadoRegistro=True,
            )
            # Tarifa del asociado
            objTarifa = TarifaAsociado.objects.get(asociado=kwargs['pkAsociado'])
            # Tarifa del convenio
            TarifaConvenio = Convenio.objects.get(concepto=form.cleaned_data['convenio'])
            objTarifa.cuotaConvenio += TarifaConvenio.valor
            objTarifa.total += TarifaConvenio.valor
            objTarifa.save()
            objConvenio.save()
            messages.info(request, 'Convenio registrado correctamente.')
            return HttpResponseRedirect(reverse_lazy('asociado:tarifaAsociado', args=[kwargs['pkAsociado']]))
        else:
            # Si el formulario es inválido, re-renderiza el formulario con errores
            return render(request, self.template_name, {
                'form': form,
                'create': 'yes',
                'pkAsociado': kwargs['pkAsociado'],
            })
        
class EditarConvenioAsociado(UpdateView):
    template_name = 'base/asociado/crearConvenio.html'

    def get(self, request, *args, **kwargs):
        query = ConveniosAsociado.objects.get(pk = kwargs['pk'])
        context = {
            'query': query,
            'pkAsociado': kwargs['pkAsociado'],
            'pk': kwargs['pk'],
            'meses': MesTarifa.objects.all()
        }

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        obj = ConveniosAsociado.objects.get(pk = kwargs['pk'])
        obj.fechaIngreso = request.POST['fechaIngreso']
        obj.primerMes = MesTarifa.objects.get(pk = request.POST['primerMes'])
        obj.save()
        messages.info(request, 'Registro Modificado Correctamente')
        return HttpResponseRedirect(reverse_lazy('asociado:tarifaAsociado', args=[kwargs['pkAsociado']]))
    
class EliminarConvenioAsociado(UpdateView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/asociado/eliminarConvenio.html'
        query = ConveniosAsociado.objects.select_related('convenio').only('fechaIngreso', 'id', 'convenio__concepto', 'convenio__valor').get(pk=kwargs['pk'])

        context = {'query': query,
                'pk': kwargs['pk'],
                'pkAsociado': kwargs['pkAsociado'],
                }
        
        if query.convenio.pk == 4:
            valor = 0
            query = ConvenioHistoricoGasolina.objects.filter(asociado=kwargs['pkAsociado'], estado_registro=True)
            for obj in query:
                valor += obj.pendiente_pago
            context.update({
                'valor': valor
            })

        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        obj = ConveniosAsociado.objects.get(pk = kwargs['pk'])
        obj.estadoRegistro = False
        obj.fechaRetiro = date.today()
        obj.save()
        objTarifa = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
        objTarifa.cuotaConvenio = objTarifa.cuotaConvenio - int(request.POST['valor'])
        objTarifa.total = objTarifa.total - int(request.POST['valor'])
        objTarifa.save()
        messages.info(request, 'Registro Eliminado Correctamente')
        return HttpResponseRedirect(reverse_lazy('asociado:tarifaAsociado', args=[kwargs['pkAsociado']]))

class CrearCodeudor(CreateView):
    model = Codeudor
    form_class = CodeudorForm
    template_name = 'base/historico/crearCodeudor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'operation': 'crear',
            'pk': self.kwargs['pk'],
            'pkAsociado': self.kwargs['pkAsociado'],
            'query_dpto' : Departamento.objects.values('id','nombre'),
            'query_mpio' : Municipio.objects.values('id','nombre','departamento','departamento__nombre')
        })
        return context

    def form_valid(self, form):
        codeudor = form.save(commit=False)
        # Asignar valores manualmente
        codeudor.nombre = codeudor.nombre.upper()
        codeudor.apellido = codeudor.apellido.upper()
        codeudor.nacionalidad = codeudor.nacionalidad.upper()
        codeudor.barrio = codeudor.barrio.upper()
        codeudor.direccion = codeudor.direccion.upper()
        codeudor.historicoCredito = HistoricoCredito.objects.get(pk=self.kwargs['pk'])
        codeudor.asociado = Asociado.objects.get(pk=self.kwargs['pkAsociado'])
        codeudor.save()
        messages.info(self.request, "Codeudor creado correctamente.")
        return HttpResponseRedirect(reverse_lazy('asociado:historicoCredito', args=[self.kwargs['pkAsociado']]))

class EditarCodeudor(UpdateView):
    model = Codeudor
    form_class = CodeudorForm
    template_name = 'base/historico/crearCodeudor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_dpto = Departamento.objects.values('id', 'nombre')
        query_mpio = Municipio.objects.values('id', 'nombre', 'departamento', 'departamento__nombre')

        context.update({
            'operation': 'editar',
            'pk': self.kwargs['pk'],
            'pkAsociado': self.kwargs['pkAsociado'],
            'query_dpto': query_dpto,
            'query_mpio': query_mpio,
        })
        return context
    
    def form_valid(self, form):
        # Verifica que el formulario sea válido antes de guardar
        if form.is_valid():
            form.save()  # Asegúrate de que el formulario esté guardando correctamente el objeto
            messages.info(self.request, "Codeudor modificado correctamente.")
            return HttpResponseRedirect(reverse_lazy('asociado:historicoCredito', args=[self.kwargs['pkAsociado']]))
        else:
            # Si el formulario no es válido, muestra errores
            messages.error(self.request, "Error al modificar el codeudor.")
            return self.render_to_response(self.get_context_data(form=form), status=400)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form), status=400)