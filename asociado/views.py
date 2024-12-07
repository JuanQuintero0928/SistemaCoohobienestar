from multiprocessing import context
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Sum
from datetime import date, timedelta

from .models import Asociado, ConveniosAsociado, Laboral, Financiera, ParametroAsociado, TarifaAsociado, RepatriacionTitular
from .form import ConvenioAsociadoForm, RepatriacionTitularForm
from beneficiario.models import Beneficiario, Mascota, Coohoperativitos, Parentesco
from historico.models import HistoricoAuxilio, HistoricoCredito, HistoricoSeguroVida, HistorialPagos
from departamento.models import Departamento, Municipio, PaisRepatriacion
from parametro.models import Tarifas, TipoAsociado, TipoAuxilio, ServicioFuneraria, MesTarifa, Convenio
from beneficiario.form import BeneficiarioForm, MascotaForm, CoohoperativitoForm
from historico.form import HistoricoSeguroVidaForm, HistoricoAuxilioForm, HistoricoCreditoForm

# Create your views here.

class Asociados(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/asociado/listarAsociado.html'
        query = Asociado.objects.values('id','nombre','apellido','numDocumento','tAsociado__concepto','numCelular','estadoAsociado')
        return render(request, template_name, {'query':query})
    
class CrearAsociado(CreateView):
    query_dpto = Departamento.objects.values('id','nombre')
    query_mpio = Municipio.objects.values('id','nombre','departamento','departamento__nombre')
    query_tAsociado = TipoAsociado.objects.all()
    query_parentesco = Parentesco.objects.all().order_by('nombre')
    template_name = 'base/asociado/crearAsociado.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'query_dpto':self.query_dpto,'query_mpio':self.query_mpio, 'query_tAsociado': self.query_tAsociado, 'query_parentesco':self.query_parentesco, 'create':'yes'})
    
    def post(self, request, *args, **kwargs):
        # try:
        numDoc = request.POST['numDocumento']
        query = Asociado.objects.filter(numDocumento = numDoc).count()
        if query == 0:
            # se guarda informacion en el modelo ASOCIADO
            obj = Asociado()
            obj.tPersona = request.POST['tPersona']
            obj.tAsociado = TipoAsociado.objects.get(pk = request.POST['tAsociado'])
            obj.estadoAsociado = request.POST['estadoAsociado']
            obj.nombre = request.POST['nombre'].upper()
            obj.apellido = request.POST['apellido'].upper()
            obj.tipoDocumento = request.POST['tipoDocumento']
            obj.numDocumento = request.POST['numDocumento']
            obj.fechaExpedicion = request.POST['fechaExpedicion']
            obj.mpioDoc = Municipio.objects.get(pk = int(request.POST['mpioDoc']))
            obj.nacionalidad = request.POST['nacionalidad'].upper()
            obj.genero = request.POST['genero']
            obj.estadoCivil = request.POST['estadoCivil']
            obj.email = request.POST['email'].lower()
            if request.POST['numResidencia'] != "":
                obj.numResidencia = request.POST['numResidencia']
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
                obj.tituloPregrado = request.POST['tituloPregrado'].upper()
            if request.POST['tituloPosgrado'] != "":
                obj.tituloPosgrado = request.POST['tituloPosgrado'].upper()
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
            obj.nombreRF = request.POST['nombreRF'].upper()
            obj.parentesco = request.POST['parentesco']
            obj.numContacto = request.POST['numContacto']
            obj.save()
            
            # se pone valor quemado en la busqueda con el pk, se busca tarifa de aportes y bienestar social
            objTarifaAporte = Tarifas.objects.get(pk = 1)
            objTarifaBSocial = Tarifas.objects.get(pk = 2)
            objTarifaAsoc = TarifaAsociado()
            objTarifaAsoc.asociado = Asociado.objects.get(pk = obj.pk)
            objTarifaAsoc.cuotaAporte = objTarifaAporte.valor
            objTarifaAsoc.cuotaBSocial = objTarifaBSocial.valor
            objTarifaAsoc.total = objTarifaAporte.valor + objTarifaBSocial.valor
            objTarifaAsoc.cuotaMascota = 0
            objTarifaAsoc.cuotaRepatriacion = 0    
            objTarifaAsoc.cuotaSeguroVida = 0
            objTarifaAsoc.cuotaAdicionales = 0
            objTarifaAsoc.cuotaCoohopAporte = 0
            objTarifaAsoc.cuotaCoohopBsocial = 0
            objTarifaAsoc.estadoRegistro = True
            objTarifaAsoc.save()
            # se guarda informacion en el modelo LABORAL
            objLaboral = Laboral()
            objLaboral.asociado = Asociado.objects.get(pk = obj.pk)
            objLaboral.estadoRegistro = True
            objLaboral.save()
            # se guarda informacion en el modelo FINANCIERA
            objFinanciera = Financiera()
            objFinanciera.asociado = Asociado.objects.get(pk = obj.pk)
            objFinanciera.estadoRegistro = True
            objFinanciera.save()
            # se guarda informacion en el modelo PARAMETROASOCIADO
            objParametro = ParametroAsociado()
            objParametro.asociado = Asociado.objects.get(pk = obj.pk)
            # se realiza validacion, si tipoAsociado es = independiente, no se realiza autorizacion de dcto, si es diferente se pone empresa y activa autorizacion
            if obj.tAsociado.pk == 1:
                objParametro.autorizaciondcto = False
            else:
                objParametro.autorizaciondcto = True
                objParametro.empresa = TipoAsociado.objects.get(pk = request.POST['tAsociado'])
            # se selecciona de manera predeterminada la funeraria , = jardines
            objParametro.funeraria = ServicioFuneraria.objects.get(pk = 1)
            objParametro.estadoRegistro = True
            try:
                objParametro.tarifaAsociado = TarifaAsociado.objects.get(pk = objTarifaAsoc.pk)
                objParametro.primerMes = MesTarifa.objects.get(fechaInicio__lte = obj.fechaIngreso, fechaFinal__gte = obj.fechaIngreso)
        
                # Si no hay errores se guarda toda la informacion
                objParametro.save()
                messages.info(request, 'Asociado Creado Correctamente')
                return HttpResponseRedirect(reverse_lazy('asociado:verAsociado', args=[obj.pk]))
            except MesTarifa.DoesNotExist:
                objParametro.primerMes = MesTarifa.objects.get(pk = 1)
                objParametro.save()
                messages.info(request, 'Asociado Creado Correctamente')
                return HttpResponseRedirect(reverse_lazy('asociado:verAsociado', args=[obj.pk]))
        else:
            messages.warning(request, 'El asociado con cedula '+ numDoc + ' ya existe en la base de datos.')
            return HttpResponseRedirect(reverse_lazy('asociado:asociado'))
        # except Exception as e:
        #     messages.warning(request, 'Hubo un problema al guardar la información.')
        #     return HttpResponseRedirect(reverse_lazy('asociado:asociado'))          
        
class VerAsociado(ListView):
    template_name = 'base/asociado/verAsociado.html'

    def get(self, request, *args, **kwargs):
        try:
            query_dpto = Departamento.objects.values('id','nombre')
            query_mpio = Municipio.objects.values('id','nombre','departamento','departamento__nombre')
            objAsociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
            objParentesco = Parentesco.objects.all().order_by('nombre')
            objEmpresa = TipoAsociado.objects.all()
            objServFuneraria = ServicioFuneraria.objects.all()
            # objParametroAsociado = ParametroAsociado.objects.get(asociado = kwargs['pkAsociado'])
            objParametroAsociado = ParametroAsociado.objects.values('id','funeraria','autorizaciondcto','empresa','autorizaciondcto','primerMes').get(asociado = kwargs['pkAsociado'])
            objMes = MesTarifa.objects.all()
            objLaboral = Laboral.objects.get(asociado = kwargs['pkAsociado'])
            objFinanciero = Financiera.objects.get(asociado = kwargs['pkAsociado'])
            return render(request, self.template_name, {'laboral':'no', 'pkAsociado':kwargs['pkAsociado'], 'query_dpto':query_dpto, 'query_mpio':query_mpio, 'objAsociado':objAsociado, 'objFinanciero': objFinanciero, 'objLaboral':objLaboral, 'objParentesco':objParentesco, 'objEmpresa':objEmpresa, 'objServFuneraria':objServFuneraria, 'objParametroAsociado':objParametroAsociado, 'objMes':objMes, 'vista':1})
        except Laboral.DoesNotExist:
            return render(request, self.template_name, {'laboral':'yes', 'pkAsociado':kwargs['pkAsociado'], 'query_dpto':query_dpto, 'query_mpio':query_mpio, 'objAsociado':objAsociado, 'objParentesco':objParentesco, 'objEmpresa':objEmpresa, 'objServFuneraria':objServFuneraria, 'objParametroAsociado':objParametroAsociado, 'objMes':objMes, 'vista':1})

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
        if request.POST['numResidencia'] != "":
            obj.numResidencia = request.POST['numResidencia']
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
        # Si tipo Asociado cambia, se cambia en el modelo PARAMETRO ASOCIADO
        objParamatro = ParametroAsociado.objects.get(asociado = kwargs['pkAsociado'])
        if objParamatro.autorizaciondcto == False:
            if obj.tAsociado.pk != objParamatro.empresa:
                objParamatro.empresa = TipoAsociado.objects.get(pk = obj.tAsociado.pk)
                objParamatro.autorizaciondcto = True
        else:
            if obj.tAsociado.pk == 1:
                objParamatro.empresa = None
                objParamatro.autorizaciondcto = False
            else:
                objParamatro.empresa = TipoAsociado.objects.get(pk = obj.tAsociado.pk)
        objParamatro.save()
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
            objFinanciera.ingresosActPrin = request.POST['ingresosActPrin']
        else:
            objFinanciera.ingresosActPrin = None
        if request.POST['otroIngreso1'] != "":
            objFinanciera.otroIngreso1 = request.POST['otroIngreso1']
        else:
            objFinanciera.otroIngreso1 = None
        if request.POST['otroIngreso2'] != "":
            objFinanciera.otroIngreso2 = request.POST['otroIngreso2']
        else:
            objFinanciera.otroIngreso2 = None
        if request.POST['egresos'] != "":
            objFinanciera.egresos = request.POST['egresos']
        else:
            objFinanciera.egresos = None
        if request.POST['activos'] != "":
            objFinanciera.activos = request.POST['activos']
        else:
            objFinanciera.activos = None
        if request.POST['pasivos'] != "":
            objFinanciera.pasivos = request.POST['pasivos']
        else:
            objFinanciera.pasivos = None
        if request.POST['patrimonio'] != "":
            objFinanciera.patrimonio = request.POST['patrimonio']
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
            obj.empresa = TipoAsociado.objects.get(pk = request.POST['empresaDcto'])
            objAsociado.tAsociado = TipoAsociado.objects.get(pk = request.POST['empresaDcto'])
        else:
            obj.autorizaciondcto = False
            obj.empresa = None
            # Si se desactiva el check el asociado pasa a indenpendeinte
            objAsociado.tAsociado = TipoAsociado.objects.get(pk = 1)
        obj.funeraria = ServicioFuneraria.objects.get(pk = request.POST['servFuneraria'])
        obj.primerMes = MesTarifa.objects.get(pk = request.POST['primesMes'])
        obj.save()
        objAsociado.save()
        messages.info(request, 'Información Modificada Correctamente')
        return HttpResponseRedirect(reverse_lazy('asociado:verAsociado', args=[kwargs['pkAsociado']]))


class Beneficiarios(ListView):
    template_name = 'base/asociado/listarBeneficiarios.html'

    def get(self, request, *args, **kwargs):
        queryBeneficiarios = Beneficiario.objects.filter(asociado = kwargs['pkAsociado']).filter(estadoRegistro = True)
        numBenef = queryBeneficiarios.count()
        queryAsociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
        return render(request, self.template_name, {'updateAsociado':'yes','pkAsociado':kwargs['pkAsociado'],'query':queryBeneficiarios, 'queryAsociado':queryAsociado, 'cuenta':numBenef ,'vista':2})
        
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


class Mascotas(ListView):
    template_name = 'base/asociado/listarMascota.html'

    def get(self, request, *args, **kwargs):
        queryMascotas = Mascota.objects.filter(asociado = kwargs['pkAsociado']).filter(estadoRegistro = True)
        queryAsociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
        return render(request, self.template_name, {'updateAsociado':'yes','pkAsociado':kwargs['pkAsociado'],'query':queryMascotas, 'queryAsociado':queryAsociado, 'vista':3})

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

class VerHistoricoAuxilio(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/historico/listarHistoricoAuxilio.html'
        queryHistorico = HistoricoAuxilio.objects.filter(asociado = kwargs['pkAsociado'], estadoRegistro = True)
        queryAsociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
        return render(request, template_name, {'updateAsociado':'yes','pkAsociado':kwargs['pkAsociado'],'query':queryHistorico, 'queryAsociado':queryAsociado, 'vista':4})

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
        if obj.tipoAuxilio.pk == 3:
            objParentesco = Parentesco.objects.all().order_by('nombre')
        return render(request, template_name, {'obj':obj, 'objParentesco':objParentesco, 'pkAsociado':kwargs['pkAsociado'], 'pk': kwargs['pk']})

    def post(self, request, *args, **kwargs):
        obj = HistoricoAuxilio.objects.get(pk = kwargs['pk'])
        obj.estado = request.POST['estado']
        obj.fechaSolicitud = request.POST['fechaSolicitud']
        obj.entidadBancaria = request.POST['entidadBancaria'].upper()
        obj.numCuenta = request.POST['numCuenta']
        if obj.tipoAuxilio.pk == 3:
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

class VerHistoricoCredito(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/historico/listarHistoricoCredito.html'
        queryCredito = HistoricoCredito.objects.filter(asociado = kwargs['pkAsociado'])
        queryAsociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
        return render(request, template_name, {'updateAsociado':'yes','pkAsociado':kwargs['pkAsociado'],'query':queryCredito, 'queryAsociado':queryAsociado,'vista':5})

# class CrearHistoricoCredito(CreateView):
#     model = HistoricoCredito
#     form_class = HistoricoCreditoForm
#     template_name = 'base/historico/crearHistoricoCredito.html'
#     success_url = reverse_lazy('asociado:historicoCredito')

#     def form_valid(self, form):
#         print("Método POST recibido en form_valid")  # Mensaje de depuración
#         # Obtener el objeto 'Asociado' a partir del `pk` en los kwargs
#         asociado = get_object_or_404(Asociado, pk=self.kwargs['pkAsociado'])

#         # Asignar el objeto 'Asociado' al formulario 
#         form.instance.asociado = asociado

#         # Validaciones adicionales
#         if form.instance.valor < 0 or form.instance.cuotas < 0:
#             form.add_error('valor', 'El valor no puede ser negativo.')
#             return self.form_invalid(form)
        
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         # se llama al contexto original
#         context = super().get_context_data(**kwargs)

#         context['asociado'] = Asociado.objects.get(pk = self.kwargs['pkAsociado'])
#         context['vista'] = {'crear':'yes'}
#         return context

class CrearHistoricoCredito(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/historico/crearHistoricoCredito.html'
        form = HistoricoCreditoForm()
        queryAsociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
        return render(request, template_name, {'crear':'yes','pkAsociado':kwargs['pkAsociado'], 'form':form,'asociado':queryAsociado})

    def post(self, request, *args, **kwargs):
        formulario = HistoricoCreditoForm(request.POST)
        if formulario.is_valid():
            obj = HistoricoCredito()
            obj.fechaSolicitud = formulario.cleaned_data['fechaSolicitud']
            obj.asociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
            obj.valor = formulario.cleaned_data['valor']
            obj.cuotas = formulario.cleaned_data['cuotas']
            obj.estado = formulario.cleaned_data['estado']
            obj.estadoRegistro = True
            obj.save()
            messages.info(request, 'Registro Creado Correctamente')
            return HttpResponseRedirect(reverse_lazy('asociado:historicoCredito', args=[kwargs['pkAsociado']]))

class EditarHistoricoCredito(ListView):
    def get(self, request, *args, **kwargs):
        form_update = get_object_or_404(HistoricoCredito, pk = kwargs['pk'])
        form = HistoricoCreditoForm(initial={'fechaSolicitud':form_update.fechaSolicitud,
                                            'valor':form_update.valor,
                                            'cuotas':form_update.cuotas,
                                            'estado':form_update.estado})
        template_name = 'base/historico/crearHistoricoCredito.html'
        return render(request, template_name, {'editar':'yes','form':form,'pkAsociado':kwargs['pkAsociado'], 'pk':kwargs['pk']})

    def post(self, request, *args, **kwargs):
        formulario = HistoricoCreditoForm(request.POST)
        if formulario.is_valid():
            obj = HistoricoCredito.objects.get(pk = kwargs['pk'])
            obj.fechaSolicitud = formulario.cleaned_data['fechaSolicitud']
            obj.valor = formulario.cleaned_data['valor']
            obj.cuotas = formulario.cleaned_data['cuotas']
            obj.estado = formulario.cleaned_data['estado']
            obj.save()
            messages.info(request, 'Registro Editado Correctamente')
            return HttpResponseRedirect(reverse_lazy('asociado:historicoCredito', args=[kwargs['pkAsociado']]))

class VerTarifaAsociado(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/historico/listarTarifaAsociado.html'
        queryTarifaAsociado = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
        queryConvenio = ConveniosAsociado.objects.filter(asociado = kwargs['pkAsociado'], estadoRegistro = True)
        queryRepatriacionTitular = RepatriacionTitular.objects.filter(asociado = kwargs['pkAsociado'], estadoRegistro = True).exists()
        repatriacionAsociado = 0
        pkRepatriacion = 0
        # se valida si hay titulares de repatriacion
        if queryRepatriacionTitular:
            queryRepatriacionTitular = RepatriacionTitular.objects.filter(asociado = kwargs['pkAsociado'], estadoRegistro = True).first()
            benef = Beneficiario.objects.filter(asociado = kwargs['pkAsociado'], repatriacion = True).count()
            tarifas = Tarifas.objects.get(pk = 4)
            repatriacionAsociado = tarifas.valor
            # for pk in queryRepatriacionTitular:
            #     pkRepatriacion = pk.pk
            # se valida si existen beneficiarios con repatriacion
            if benef > 0:
                # obtenemos el valor de la tarifa de repatriacion
                queryTarifaAsociado.cuotaRepatriacion = benef * tarifas.valor
            else:
                queryTarifaAsociado.cuotaRepatriacion = 0

        adicional = False
        if queryTarifaAsociado.cuotaAdicionales > 0:
            adicional = True
        return render(request, template_name, {'updateAsociado':'yes','pkAsociado':kwargs['pkAsociado'],'query':queryTarifaAsociado, 'adicional':adicional, 'queryRepatriacionTitular':queryRepatriacionTitular,'repatriacion':repatriacionAsociado, 'pk':pkRepatriacion, 'queryConvenio':queryConvenio, 'vista':8})

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
    
class VerSeguroVida(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/asociado/listarSeguroVida.html'
        querySeguroVida = HistoricoSeguroVida.objects.filter(asociado = kwargs['pkAsociado'])
        queryAsociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
        return render(request, template_name, {'updateAsociado':'yes','pkAsociado':kwargs['pkAsociado'],'query':querySeguroVida, 'queryAsociado':queryAsociado, 'vista':6})

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

class VerCoohoperativitos(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/beneficiario/listarCoohoperativitos.html'
        queryCoohoperativitos = Coohoperativitos.objects.filter(asociado = kwargs['pkAsociado'], estadoRegistro=True)
        queryAsociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
        return render(request, template_name, {'updateAsociado':'yes','pkAsociado':kwargs['pkAsociado'],'query':queryCoohoperativitos, 'queryAsociado':queryAsociado ,'vista':7})

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
            numCoohoperativitos = Coohoperativitos.objects.filter(asociado = kwargs['pkAsociado']).count()
            objTarifaAsociado = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
            objTarifaCooho = Tarifas.objects.get(pk = 5)
            objTarifaCoohoBSocial = Tarifas.objects.get(pk = 6)
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

class VerHistorialPagos(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/historico/listarHistorialPago.html'
        queryPagos = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).order_by('fechaPago')
        queryAsociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
        return render(request, template_name, {'updateAsociado':'yes','pkAsociado':kwargs['pkAsociado'],'query':queryPagos, 'queryAsociado':queryAsociado, 'vista':9})
    
class DetalleHistorialPago(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/historico/detallePago.html'
        query = HistorialPagos.objects.get(pk = kwargs['pk'])
        return render(request, template_name, {'query':query})

class DescargarFormatos(ListView):
    def get(self, request, *args, **kwargs):
        # Query completa para el formato 1-2 - Registro y Actualizacion de Asociado
        try:  
            template_name = 'base/asociado/formatos.html'
            queryAsoc = Asociado.objects.get(pk = kwargs['pkAsociado'])
            objFinanciera = Financiera.objects.get(asociado = kwargs['pkAsociado'])
            objParametroAsociado = ParametroAsociado.objects.get(asociado = kwargs['pkAsociado'])
            objLaboral = Laboral.objects.get(asociado = kwargs['pkAsociado'])
            # se verifica si es actualizacion o registro
            fechaActual = date.today()
            if queryAsoc.fechaIngreso == fechaActual:
                actualizacion = False
            else:
                actualizacion = True
            objBeneficiario = Beneficiario.objects.filter(asociado = kwargs['pkAsociado'], estadoRegistro = True)
            cuentaBeneficiario = len(objBeneficiario)
            objMascota = Mascota.objects.filter(asociado = kwargs['pkAsociado'], estadoRegistro = True)
            cuentaMascota = len(objMascota)
            return render(request, template_name, {'updateAsociado':'yes','pkAsociado':kwargs['pkAsociado'], 'residenciaExiste':'yes','query':queryAsoc, 'queryLaboral':objLaboral, 'actualizacion':actualizacion, 'objFinanciera':objFinanciera,'fechaActual':fechaActual ,'objParametroAsociado':objParametroAsociado, 'objBeneficiario':objBeneficiario, 'objMascota':objMascota ,'vista':10, 'cuentaBeneficiario':cuentaBeneficiario, 'cuentaMascota':cuentaMascota})
        except Exception as e:
            messages.warning(request, 'Información incompleta para descargar formatos.')
            return render(request, template_name, {'mensaje':'yes','pkAsociado':kwargs['pkAsociado'], 'vista':10})

# Descarga Formato Auxilios
class ModalFormato(ListView):
    def get(self, request, *args, **kwargs):
        # Formato Auxilio
        if kwargs['formato'] == 3:
            print('formato 3')
            template_name = 'base/asociado/formato2.html'
            objAuxilio = HistoricoAuxilio.objects.filter(asociado = kwargs['pkAsociado'], estado='REVISION')
            return render(request, template_name,{'pkAsociado':kwargs['pkAsociado'], 'formato':kwargs['formato'], 'objAuxilio':objAuxilio})
        # Formato Extracto
        elif kwargs['formato'] == 4:
            template_name = 'base/asociado/formato2.html'
            objParametroAsoc = ParametroAsociado.objects.get(asociado = kwargs['pkAsociado'])
            objMes = MesTarifa.objects.filter(pk__gte = objParametroAsoc.primerMes.pk)
            return render(request, template_name,{'pkAsociado':kwargs['pkAsociado'], 'formato':kwargs['formato'], 'objMes':objMes})


# Descarga Formato Auxilios
class GenerarFormato(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/asociado/generar.html'
        fechaActual = date.today()
        objAsoc = Asociado.objects.get(pk = kwargs['pkAsociado'])

        # Formato 3
        if kwargs['formato'] == 3:
            objLaboral = Laboral.objects.get(asociado = kwargs['pkAsociado'])
            objFinanciera = Financiera.objects.get(asociado = kwargs['pkAsociado'])
            objAuxilio = HistoricoAuxilio.objects.get(pk = kwargs['pk'])
            return render(request, template_name,{'pkAsociado':kwargs['pkAsociado'], 'fechaActual':fechaActual,'objAsoc':objAsoc, 'objLaboral':objLaboral, 'objFinanciera':objFinanciera, 'objAuxilio':objAuxilio, 'formato':kwargs['formato']})
        
        # Formato 4
        elif kwargs['formato'] == 4:
            mes = MesTarifa.objects.get(pk = request.GET['mes'])
            fechaCorte = timedelta(15) + mes.fechaInicio
            objTarifaAsociado = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
            # query del ultimo pago hecho por el asociado
            objHistorialPago = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).last()     
            cuotaPeriodica = objTarifaAsociado.cuotaAporte + objTarifaAsociado.cuotaBSocial
            cuotaCoohop = objTarifaAsociado.cuotaCoohopAporte + objTarifaAsociado.cuotaCoohopBsocial
            # variables iniciacion
            saldo = 0
            valorVencido = 0
            valorVencidoMasc = 0
            valorVencidoRep = 0
            valorVencidoSeg = 0
            valorVencidoAdic = 0
            valorVencidoCoohop = 0
            mensaje = ""
            # query mostrar beneficiarios y mascotas
            objBeneficiario = Beneficiario.objects.filter(asociado = kwargs['pkAsociado'])
            cuentaBeneficiario = len(objBeneficiario)
            objMascota = Mascota.objects.filter(asociado = kwargs['pkAsociado'])
            cuentaMascota = len(objMascota)
            # query que suma la diferencia de pagos
            querySaldoTotal = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).aggregate(total=Sum('diferencia'))
            for valor in querySaldoTotal.values():
                # variable que guarda la diferencia en los saldos(0=esta al dia, > a 0, saldo favor, < a 0, saldo pendiente)
                saldoDiferencia = valor
            
            # Entra al try cuando un asociado no ha realizado ningun pago y no existe informacion en la query
            try:
                # condicional si esta atrasado
                if mes.pk > objHistorialPago.mesPago.pk:
                    cuotaVencida = mes.pk - objHistorialPago.mesPago.pk
                    if objTarifaAsociado.cuotaMascota > 0:
                        valorVencidoMasc = cuotaVencida * objTarifaAsociado.cuotaMascota
                    if objTarifaAsociado.cuotaRepatriacion > 0:
                        valorVencidoRep = cuotaVencida * objTarifaAsociado.cuotaRepatriacion
                    if objTarifaAsociado.cuotaSeguroVida > 0:
                        valorVencidoSeg = cuotaVencida * objTarifaAsociado.cuotaSeguroVida
                    if objTarifaAsociado.cuotaAdicionales > 0:
                        valorVencidoAdic = cuotaVencida * objTarifaAsociado.cuotaAdicionales
                    if objTarifaAsociado.cuotaCoohopAporte > 0:
                        valorVencidoCoohop = cuotaVencida * (objTarifaAsociado.cuotaCoohopAporte + objTarifaAsociado.cuotaCoohopBsocial)
                
                    if saldoDiferencia > 0:
                        # saldo a favor
                        valorVencido = (cuotaPeriodica * cuotaVencida) - saldoDiferencia
                        pagoTotal = valorVencido + valorVencidoMasc + valorVencidoRep + valorVencidoSeg + valorVencidoAdic + valorVencidoCoohop
                        mensaje = "Tiene un saldo a favor de $" + str(saldoDiferencia)
                    elif saldoDiferencia < 0:
                        # saldo a pagar
                        valorVencido = (cuotaPeriodica * cuotaVencida) - saldoDiferencia
                        pagoTotal = valorVencido + valorVencidoMasc + valorVencidoRep + valorVencidoSeg + valorVencidoAdic + valorVencidoCoohop
                        mensaje = "Tiene un saldo pendiente por pagar de $" + str((saldoDiferencia*-1))
                    else:
                        # saldo en 0
                        valorVencido = (cuotaPeriodica * cuotaVencida)
                        pagoTotal = valorVencido + valorVencidoMasc + valorVencidoRep + valorVencidoSeg + valorVencidoAdic + valorVencidoCoohop
                    return render(request, template_name,{'pkAsociado':kwargs['pkAsociado'], 'fechaCorte':fechaCorte,'objAsoc':objAsoc, 'objTarifaAsociado':objTarifaAsociado, 'cuotaPeriodica':cuotaPeriodica, 'cuotaCoohop':cuotaCoohop, 'cuotaVencida':cuotaVencida, 'valorVencido':valorVencido, 'valorVencidoMasc':valorVencidoMasc, 'valorVencidoRep':valorVencidoRep, 'valorVencidoSeg':valorVencidoSeg, 'valorVencidoAdic':valorVencidoAdic, 'valorVencidoCoohop':valorVencidoCoohop, 'pagoTotal':pagoTotal,'mes':mes, 'objBeneficiario':objBeneficiario, 'cuentaBeneficiario':cuentaBeneficiario, 'objMascota':objMascota, 'cuentaMascota':cuentaMascota, 'formato':kwargs['formato'],'vista':0, 'saldo':saldo, 'mensaje':mensaje})
                    
                # condicional si esta al dia
                elif mes.pk == objHistorialPago.mesPago.pk:
                    cuotaVencida = 0
                    valorMensual = objTarifaAsociado.cuotaAporte + objTarifaAsociado.cuotaBSocial + objTarifaAsociado.cuotaMascota + objTarifaAsociado.cuotaRepatriacion + objTarifaAsociado.cuotaSeguroVida + objTarifaAsociado.cuotaAdicionales + objTarifaAsociado.cuotaCoohopAporte + objTarifaAsociado.cuotaCoohopBsocial                
                
                    # se valida si en el ultimo pago no hay diferencia
                    if saldoDiferencia == 0:
                        # no existen saldos
                        saldo = valorMensual
                    elif saldoDiferencia > 0:
                        # existe saldo positivo
                        saldo = valorMensual + saldoDiferencia
                    else:
                        # existe saldo negativo, al estar negativo en la bd, se suma lo que debe
                        saldo = valorMensual + saldoDiferencia
                    
                    # comparamos el valor que va en la casilla saldo frente a lo que realmente paga el asociado
                    if saldo == valorMensual:
                        # si es igual, se muestra 0 en el extracto a pagar
                        pagoTotal = 0
                        valorVencido = 0
                    elif saldo > valorMensual:
                        # si saldo es mayor, es porque tiene un saldo a favor, se muestra 0 y se envia mensaje
                        valorVencido = 0
                        pagoTotal = 0
                        dif = saldo - valorMensual
                        mensaje = 'Tiene un saldo a favor de ' + str(dif) + '.'
                    else:
                        # si saldo es menor, es porque tiene un saldo pendiente x pagar, se muestra el valor y se envia mensaje
                        valorVencido = valorMensual - saldo
                        pagoTotal = valorMensual - saldo
                        dif = valorMensual - saldo
                        mensaje = 'Tiene un saldo pendiente por pagar de ' + str(dif) + '.'
                    return render(request, template_name,{'pkAsociado':kwargs['pkAsociado'], 'fechaCorte':fechaCorte,'objAsoc':objAsoc, 'objTarifaAsociado':objTarifaAsociado, 'cuotaPeriodica':cuotaPeriodica, 'cuotaCoohop':cuotaCoohop, 'cuotaVencida':cuotaVencida, 'valorVencido':valorVencido, 'valorVencidoMasc':valorVencidoMasc, 'valorVencidoRep':valorVencidoRep, 'valorVencidoSeg':valorVencidoSeg, 'valorVencidoAdic':valorVencidoAdic, 'valorVencidoCoohop':valorVencidoCoohop, 'pagoTotal':pagoTotal,'mes':mes, 'objBeneficiario':objBeneficiario, 'cuentaBeneficiario':cuentaBeneficiario, 'objMascota':objMascota, 'cuentaMascota':cuentaMascota, 'formato':kwargs['formato'], 'saldo':saldo, 'mensaje':mensaje})
                
                # condicional si esta adelantado
                else:
                    cuotaVencida = 0
                    pagoTotal = 0
                    # obtenemos el valor total que tiene pago el asociado, desde el mes seleccionado en la query hasta el pago en la bd
                    query = HistorialPagos.objects.filter(mesPago__gte = mes.pk, asociado = kwargs['pkAsociado']).aggregate(total=Sum('valorPago'))
                    for valor in query.values():
                        saldoActual = valor
                    
                    valorMensual = (objTarifaAsociado.cuotaAporte + objTarifaAsociado.cuotaBSocial + objTarifaAsociado.cuotaMascota + objTarifaAsociado.cuotaRepatriacion + objTarifaAsociado.cuotaSeguroVida + objTarifaAsociado.cuotaAdicionales + objTarifaAsociado.cuotaCoohopAporte + objTarifaAsociado.cuotaCoohopBsocial) * ((objHistorialPago.mesPago.pk - mes.pk)+1)
                    
                    if saldoDiferencia > 0:
                        saldo = valorMensual + saldoDiferencia
                    elif saldoDiferencia < 0:
                        saldo = valorMensual + saldoDiferencia
                    else:
                        saldo = valorMensual

                    mensaje = "Tiene Pago hasta el mes de " + objHistorialPago.mesPago.concepto + "."
                    
                    return render(request, template_name,{'pkAsociado':kwargs['pkAsociado'], 'fechaCorte':fechaCorte,'objAsoc':objAsoc, 'objTarifaAsociado':objTarifaAsociado, 'cuotaPeriodica':cuotaPeriodica, 'cuotaCoohop':cuotaCoohop, 'cuotaVencida':cuotaVencida, 'valorVencido':valorVencido, 'valorVencidoMasc':valorVencidoMasc, 'valorVencidoRep':valorVencidoRep, 'valorVencidoSeg':valorVencidoSeg, 'valorVencidoAdic':valorVencidoAdic, 'valorVencidoCoohop':valorVencidoCoohop, 'pagoTotal':pagoTotal,'mes':mes, 'objBeneficiario':objBeneficiario, 'cuentaBeneficiario':cuentaBeneficiario, 'objMascota':objMascota, 'cuentaMascota':cuentaMascota, 'formato':kwargs['formato'], 'saldo':saldo, 'mensaje':mensaje})
            
            # si no hay pagos en la bd
            except Exception as e:
                valorVencidoMasc = objTarifaAsociado.cuotaMascota
                valorVencidoRep = objTarifaAsociado.cuotaRepatriacion
                valorVencidoSeg = objTarifaAsociado.cuotaSeguroVida
                valorVencidoAdic = objTarifaAsociado.cuotaAdicionales
                valorVencidoCoohop = objTarifaAsociado.cuotaCoohopAporte + objTarifaAsociado.cuotaCoohopBsocial
                # obtenemos el parametro del primer mes q debe pagar
                objParametroAsoc = ParametroAsociado.objects.get(asociado = kwargs['pkAsociado'])
                cuotaVencida = mes.pk - objParametroAsoc.primerMes.pk
                cuotaVencida += 1
                if cuotaVencida == 0:
                    # mes seleccionado igual al parametro.primerMes
                    valorVencido = cuotaPeriodica
                    pagoTotal = valorVencido + valorVencidoMasc + valorVencidoRep + valorVencidoSeg + valorVencidoAdic + valorVencidoCoohop
                elif cuotaVencida > 0:
                    # mes adelantado al parametro.primerMes
                    valorVencido = cuotaPeriodica * cuotaVencida
                    valorVencidoMasc = objTarifaAsociado.cuotaMascota * cuotaVencida
                    valorVencidoRep = objTarifaAsociado.cuotaRepatriacion * cuotaVencida
                    valorVencidoSeg = objTarifaAsociado.cuotaSeguroVida * cuotaVencida
                    valorVencidoAdic = objTarifaAsociado.cuotaAdicionales * cuotaVencida
                    valorVencidoCoohop = (objTarifaAsociado.cuotaCoohopAporte + objTarifaAsociado.cuotaCoohopBsocial) * cuotaVencida
                    pagoTotal = valorVencido + valorVencidoMasc + valorVencidoRep + valorVencidoSeg + valorVencidoAdic + valorVencidoCoohop
                else:
                    pass
                return render(request, template_name,{'pkAsociado':kwargs['pkAsociado'], 'fechaCorte':fechaCorte,'objAsoc':objAsoc, 'objTarifaAsociado':objTarifaAsociado, 'cuotaPeriodica':cuotaPeriodica, 'cuotaCoohop':cuotaCoohop, 'cuotaVencida':cuotaVencida, 'valorVencido':valorVencido, 'valorVencidoMasc':valorVencidoMasc, 'valorVencidoRep':valorVencidoRep, 'valorVencidoSeg':valorVencidoSeg, 'valorVencidoAdic':valorVencidoAdic, 'valorVencidoCoohop':valorVencidoCoohop, 'pagoTotal':pagoTotal,'mes':mes, 'objBeneficiario':objBeneficiario, 'cuentaBeneficiario':cuentaBeneficiario, 'objMascota':objMascota, 'cuentaMascota':cuentaMascota, 'formato':kwargs['formato'],'saldo':saldo})

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
                estadoRegistro=True,
            )
            # Tarifa del asociado
            objTarifa = TarifaAsociado.objects.get(pk=kwargs['pkAsociado'])
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
            'pk': kwargs['pk']
        }

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        obj = ConveniosAsociado.objects.get(pk = kwargs['pk'])
        obj.fechaIngreso = request.POST['fechaIngreso']
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