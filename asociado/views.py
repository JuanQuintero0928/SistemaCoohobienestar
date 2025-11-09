from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View, DeleteView
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Sum, Prefetch, Q, Value, F
from django.db.models.functions import Concat
from datetime import date
from funciones.function import StaffRequiredMixin
import json
from django.core.serializers.json import DjangoJSONEncoder
from .utils.form_utils import asignar_campos
from .models import (
    Asociado,
    ConveniosAsociado,
    Laboral,
    Financiera,
    ParametroAsociado,
    TarifaAsociado,
    RepatriacionTitular,
    ConvenioHistoricoGasolina,
)
from beneficiario.models import Beneficiario, Mascota, Coohoperativitos, Parentesco
from credito.models import Codeudor
from departamento.models import Departamento, Municipio, PaisRepatriacion, Pais
from historico.models import (
    HistoricoAuxilio,
    HistoricoCredito,
    HistoricoSeguroVida,
    HistorialPagos,
)
from parametro.models import (
    Tarifas,
    TipoAsociado,
    TipoAuxilio,
    ServicioFuneraria,
    MesTarifa,
    Convenio,
    TasasInteresCredito,
    FormaPago,
)
from ventas.models import HistoricoVenta

from .form import ConvenioAsociadoForm, RepatriacionTitularForm, TarifaAsociadoAdicionalForm
from beneficiario.form import BeneficiarioForm, MascotaForm, CoohoperativitoForm
from credito.form import CodeudorForm
from historico.form import (
    HistoricoSeguroVidaForm,
    HistoricoAuxilioForm,
    HistoricoCreditoForm,
)
from reportes.utils.medicion import medir_rendimiento
from reportes.utils.extracto import obtenerValorExtracto

# Create your views here.


class Asociados(LoginRequiredMixin, StaffRequiredMixin, ListView):
    template_name = "base/asociado/listarAsociado.html"

    def get(self, request, *args, **kwargs):
        # Si es una petición AJAX, devolver JSON con paginación

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            start = int(request.GET.get("start", 0))
            length = int(request.GET.get("length", 10))
            search_value = request.GET.get("search_value", "").strip()

            # Obtener columna y dirección de ordenación
            order_column_index = int(request.GET.get("order[0][column]", 0))
            order_direction = request.GET.get("order[0][dir]", "asc")

            # Mapeo de columnas para ordenación
            column_map = [
                "id",
                "nombre",
                "apellido",
                "numDocumento",
                "tAsociado__concepto",
                "numCelular",
                "estadoAsociado",
            ]

            # Obtener columna de ordenación (por defecto 'id')
            order_column = (
                column_map[order_column_index]
                if order_column_index < len(column_map)
                else "id"
            )

            # Aplicar orden ascendente o descendente
            if order_direction == "desc":
                order_column = f"-{order_column}"

            # Obtener datos ordenados
            query = (
                Asociado.objects.annotate(
                    nombre_completo=Concat(F("nombre"), Value(" "), F("apellido"))
                )
                .values(
                    "id",
                    "nombre_completo",
                    "numDocumento",
                    "tAsociado__concepto",
                    "numCelular",
                    "estadoAsociado",
                )
                .order_by(order_column)
            )

            # Aplicar filtro de búsqueda
            if search_value:
                query = query.filter(
                    Q(id__icontains=search_value)
                    | Q(nombre__icontains=search_value)
                    | Q(apellido__icontains=search_value)
                    | Q(nombre_completo__icontains=search_value)
                    | Q(numDocumento__icontains=search_value)
                    | Q(tAsociado__concepto__icontains=search_value)
                    | Q(numCelular__icontains=search_value)
                    | Q(estadoAsociado__icontains=search_value)
                )

            total_records = query.count()

            # Aplicar paginación
            paginator = Paginator(query, length)
            page_number = (start // length) + 1
            page = paginator.get_page(page_number)

            return JsonResponse(
                {
                    "data": list(page),
                    "recordsTotal": total_records,
                    "recordsFiltered": total_records,
                }
            )

        else:
            # Renderizar la plantilla en la primera carga
            return render(request, self.template_name)


class CrearAsociado(CreateView):
    def get(self, request, *args, **kwargs):
        template_name = "base/asociado/crearAsociado.html"
        query_dpto = Departamento.objects.values("id", "nombre")
        query_tAsociado = TipoAsociado.objects.all()
        query_parentesco = Parentesco.objects.all().order_by("nombre")
        # seleccionamos el valor de la vinculacion del adulto
        query_tarifa = Tarifas.objects.get(pk=7)
        query_formaPago = FormaPago.objects.values("id", "formaPago")

        context = {
            "query_dpto": query_dpto,
            "query_tAsociado": query_tAsociado,
            "query_parentesco": query_parentesco,
            "query_tarifa": query_tarifa.valor,
            "query_formaPago": query_formaPago,
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        numDoc = request.POST["numDocumento"]

        if Asociado.objects.filter(numDocumento=numDoc).exists():
            return JsonResponse(
                {
                    "ok": False,
                    "mensaje": f"El asociado con el número de documento {numDoc} ya existe.",
                }
            )
        try:
            with transaction.atomic():

                # Variables modelo ASOCIADO
                envio_correo = request.POST.getlist("envioInfoCorreo")
                envio_mensaje = request.POST.getlist("envioInfoMensaje")
                envio_whatsapp = request.POST.getlist("envioInfoWhatsapp")

                # se guarda informacion en el modelo ASOCIADO
                obj = Asociado.objects.create(
                    tPersona=request.POST["tPersona"],
                    tAsociado=TipoAsociado.objects.get(pk=request.POST["tAsociado"]),
                    estadoAsociado=request.POST["estadoAsociado"],
                    nombre=request.POST["nombre"].upper(),
                    apellido=request.POST["apellido"].upper(),
                    tipoDocumento=request.POST["tipoDocumento"],
                    numDocumento=request.POST["numDocumento"],
                    fechaExpedicion=request.POST["fechaExpedicion"],
                    mpioDoc=Municipio.objects.get(pk=int(request.POST["mpioDoc"])),
                    nacionalidad=request.POST["nacionalidad"].upper(),
                    genero=request.POST["genero"],
                    estadoCivil=request.POST["estadoCivil"],
                    email=request.POST["email"].lower(),
                    numResidencia=(
                        request.POST["numResidencia"]
                        if request.POST["numResidencia"]
                        else ""
                    ),
                    numCelular=request.POST["numCelular"],
                    indicativoCelular=Pais.objects.get(pk=request.POST["indicativo"]),
                    envioInfoCorreo=True if len(envio_correo) == 1 else False,
                    envioInfoMensaje=True if len(envio_mensaje) == 1 else False,
                    envioInfoWhatsapp=True if len(envio_whatsapp) == 1 else False,
                    nivelEducativo=request.POST["nivelEducativo"],
                    tituloPregrado=(
                        request.POST["tituloPregrado"].upper()
                        if request.POST["tituloPregrado"] != ""
                        else None
                    ),
                    tituloPosgrado=(
                        request.POST["tituloPosgrado"].upper()
                        if request.POST["tituloPosgrado"] != ""
                        else None
                    ),
                    fechaIngreso=request.POST["fechaIngreso"],
                    fechaActualizacionDatos=request.POST["fechaActualizacionDatos"],
                    estadoRegistro=True,
                    tipoVivienda=request.POST["tipoVivienda"].upper(),
                    estrato=request.POST["estrato"],
                    direccion=request.POST["direccion"].upper(),
                    barrio=request.POST["barrio"].upper(),
                    deptoResidencia=Departamento.objects.get(
                        pk=request.POST["deptoResidencia"]
                    ),
                    mpioResidencia=Municipio.objects.get(
                        pk=request.POST["mpioResidencia"]
                    ),
                    fechaNacimiento=request.POST["fechaNacimiento"],
                    dtoNacimiento=Departamento.objects.get(
                        pk=request.POST["dtoNacimiento"]
                    ),
                    mpioNacimiento=Municipio.objects.get(
                        pk=request.POST["mpioNacimiento"]
                    ),
                    nombreRF=request.POST["nombreRF"].upper(),
                    parentesco=request.POST["parentesco"],
                    numContacto=request.POST["numContacto"],
                    zonaUbicacion=request.POST["zonaUbicacion"],
                    empleadoCooho=request.POST["empleadoCoohobienestar"],
                    nPersonasCargo=(
                        request.POST["nPersonasCargo"]
                        if request.POST["nPersonasCargo"] != ""
                        else 0
                    ),
                    nHijos=(
                        request.POST["nHijos"] if request.POST["nHijos"] != "" else 0
                    ),
                    cabezaFamilia=request.POST["cabezaFamilia"],
                )

                # se guarda informacion en el modelo LABORAL
                objLaboral = Laboral.objects.create(
                    id=obj.pk,
                    asociado=obj,
                    estadoRegistro=True,
                )

                # se guarda informacion en el modelo FINANCIERA
                objFinanciera = Financiera.objects.create(
                    id=obj.pk,
                    asociado=obj,
                    estadoRegistro=True,
                )

                # Consulta del valor de la tarifa de aporte, bSocial y vinculacion
                tarifas = Tarifas.objects.filter(pk__in=[1, 2, 7])

                # Convierte la lista de objetos en un diccionario
                tarifas_dict = {t.pk: t for t in tarifas}

                objTarifaAporte = tarifas_dict.get(1)
                objTarifaBSocial = tarifas_dict.get(2)

                # se guarda informacion en el modelo TARIFA ASOCIADO
                objTarifaAsoc = TarifaAsociado.objects.create(
                    id=obj.pk,
                    asociado=obj,
                    cuotaAporte=objTarifaAporte.valor,
                    cuotaBSocial=objTarifaBSocial.valor,
                    total=objTarifaAporte.valor + objTarifaBSocial.valor,
                    cuotaMascota=0,
                    cuotaRepatriacionBeneficiarios=0,
                    cuotaRepatriacionTitular=0,
                    cuotaSeguroVida=0,
                    cuotaAdicionales=0,
                    cuotaCoohopAporte=0,
                    cuotaCoohopBsocial=0,
                    cuotaConvenio=0,
                    estadoAdicional=False,
                    estadoRegistro=True,
                )

                # Se selecciona la forma de pago de la vinculacion
                formaPago = request.POST["formaPago"]

                # Variables modelo PARAMETROASOCIADO
                try:
                    primerMesPago = MesTarifa.objects.get(
                        fechaInicio__lte=obj.fechaIngreso,
                        fechaFinal__gte=obj.fechaIngreso,
                    )
                except MesTarifa.DoesNotExist:
                    primerMesPago = MesTarifa.objects.get(pk=1)

                vinculacionForma = FormaPago.objects.get(pk=formaPago)
                servicioFuneraria = ServicioFuneraria.objects.get(pk=1)

                # se guarda informacion en el modelo PARAMETROASOCIADO
                objParametro = ParametroAsociado.objects.create(
                    id=obj.pk,
                    asociado=obj,
                    autorizaciondcto=False if obj.tAsociado.pk == 1 else True,
                    funeraria=servicioFuneraria,
                    primerMes=primerMesPago,
                    tarifaAsociado=objTarifaAsoc,
                    vinculacionFormaPago=vinculacionForma,
                    vinculacionCuotas=(
                        request.POST["cuotasPago"] if vinculacionForma.pk == 2 else None
                    ),
                    vinculacionValor=(
                        request.POST["valorCuota"] if vinculacionForma.pk == 2 else None
                    ),
                    vinculacionPendientePago=(
                        int(request.POST["valorCuota"])
                        * int(request.POST["cuotasPago"])
                        if vinculacionForma.pk == 2
                        else None
                    ),
                    estadoRegistro=True,
                )

                if vinculacionForma.pk != 2:
                    # Pk de la vinculacion adulto
                    mes_Pago = MesTarifa.objects.get(pk=9995)

                    HistorialPagos.objects.create(
                        asociado=obj,
                        mesPago=mes_Pago,
                        fechaPago=obj.fechaIngreso,
                        valorPago=tarifas_dict.get(7).valor,
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
                        formaPago=vinculacionForma,
                        userCreacion=request.user,
                        estadoRegistro=True,
                    )

                # messages.info(request, "Asociado Creado Correctamente")
                # return HttpResponseRedirect(reverse_lazy('asociado:verAsociado', args=[obj.pk]))
                return JsonResponse(
                    {
                        "ok": True,
                        "mensaje": "Asociado creado correctamente",
                        "redirect": reverse_lazy("asociado:verAsociado", args=[obj.pk]),
                    }
                )

        except Exception as e:
            return JsonResponse(
                {"ok": False, "mensaje": f"Error al crear el asociado: {str(e)}"}
            )


class VerAsociado(DetailView):
    model = Asociado
    template_name = "base/asociado/verAsociado.html"
    context_object_name = "objAsociado"
    pk_url_kwarg = "pkAsociado"

    def get_queryset(self):
        return Asociado.objects.select_related(
            "tAsociado",
            "mpioNacimiento",
            "mpioResidencia",
            "mpioDoc",
            "deptoResidencia",
            "dtoNacimiento",
            "indicativoCelular",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asociado = self.object

        context.update(
            {
                "pkAsociado": asociado.pk,
                "query_dpto": Departamento.objects.values("id", "nombre"),
                "objParentesco": Parentesco.objects.all().order_by("nombre"),
                "objEmpresa": TipoAsociado.objects.all(),
                "objServFuneraria": ServicioFuneraria.objects.all(),
                "objParametroAsociado": ParametroAsociado.objects.values(
                    "id", "funeraria", "autorizaciondcto", "primerMes"
                ).get(asociado=asociado.pk),
                "objMes": MesTarifa.objects.all(),
                "objLaboral": Laboral.objects.select_related(
                    "mpioTrabajo", "dptoTrabajo"
                ).get(asociado=asociado.pk),
                "objFinanciero": Financiera.objects.get(asociado=asociado.pk),
                "pais_seleccionado": (
                    asociado.indicativoCelular.id
                    if asociado.indicativoCelular
                    else None
                ),
                "vista": 1,
            }
        )
        return context

    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)


class EditarAsociado(UpdateView):

    def post(self, request, *args, **kwargs):
        obj = Asociado.objects.get(pk=kwargs["pkAsociado"])
        obj.tPersona = request.POST["tPersona"]
        obj.tAsociado = TipoAsociado.objects.get(pk=request.POST["tAsociado"])
        obj.fechaActualizacionDatos = request.POST["fechaActualizacionDatos"]
        # se valida si cambia el estado del asociado
        if obj.estadoAsociado != request.POST["estadoAsociado"]:
            # se valida si en el form se paso de activo a retiro
            if request.POST["estadoAsociado"] == "RETIRO":
                obj.fechaRetiro = request.POST["fechaRetiro"]
                obj.estadoAsociado = request.POST["estadoAsociado"]
            # si pasa de retiro o inactivo a activo
            elif request.POST["estadoAsociado"] == "ACTIVO":
                obj.fechaRetiro = None
                obj.estadoAsociado = request.POST["estadoAsociado"]
            # INACTIVO
            else:
                obj.estadoAsociado = request.POST["estadoAsociado"]
        elif obj.estadoAsociado == "RETIRO":
            obj.fechaRetiro = request.POST["fechaRetiro"]
        obj.nombre = request.POST["nombre"].upper()
        obj.apellido = request.POST["apellido"].upper()
        obj.tipoDocumento = request.POST["tipoDocumento"]
        obj.numDocumento = request.POST["numDocumento"]
        obj.fechaExpedicion = request.POST["fechaExpedicion"]
        obj.mpioDoc = Municipio.objects.get(pk=int(request.POST["mpioDoc"]))
        obj.nacionalidad = request.POST["nacionalidad"].upper()
        obj.genero = request.POST["genero"]
        obj.estadoCivil = request.POST["estadoCivil"]
        obj.email = request.POST["email"]
        if request.POST["numResidencia"] != None:
            obj.numResidencia = request.POST["numResidencia"]
        else:
            obj.numResidencia = None
        obj.indicativoCelular = Pais.objects.get(pk=request.POST["indicativo"])
        obj.numCelular = request.POST["numCelular"]
        envioCorreo = request.POST.getlist("envioInfoCorreo")
        envioMensaje = request.POST.getlist("envioInfoMensaje")
        envioWhatsapp = request.POST.getlist("envioInfoWhatsapp")

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
        obj.nivelEducativo = request.POST["nivelEducativo"]
        if request.POST["tituloPregrado"] != "":
            obj.tituloPregrado = request.POST["tituloPregrado"].upper()
        if request.POST["tituloPosgrado"] != "":
            obj.tituloPosgrado = request.POST["tituloPosgrado"].upper()
        obj.fechaIngreso = request.POST["fechaIngreso"]
        obj.estadoRegistro = True
        obj.tipoVivienda = request.POST["tipoVivienda"].upper()
        obj.estrato = request.POST["estrato"]
        obj.direccion = request.POST["direccion"].upper()
        obj.barrio = request.POST["barrio"].upper()
        obj.deptoResidencia = Departamento.objects.get(
            pk=request.POST["deptoResidencia"]
        )
        obj.mpioResidencia = Municipio.objects.get(pk=request.POST["mpioResidencia"])
        obj.fechaNacimiento = request.POST["fechaNacimiento"]
        obj.dtoNacimiento = Departamento.objects.get(pk=request.POST["dtoNacimiento"])
        obj.mpioNacimiento = Municipio.objects.get(pk=request.POST["mpioNacimiento"])
        obj.nombreRF = request.POST["nombreRF"]
        obj.parentesco = request.POST["parentesco"]
        obj.numContacto = request.POST["numContacto"]
        obj.zonaUbicacion = request.POST["zonaUbicacion"]
        obj.empleadoCooho = request.POST["empleadoCoohobienestar"]
        obj.nPersonasCargo = (
            request.POST["nPersonasCargo"]
            if request.POST["nPersonasCargo"] != ""
            else 0
        )
        obj.nHijos = request.POST["nHijos"] if request.POST["nHijos"] != "" else 0
        obj.cabezaFamilia = request.POST["cabezaFamilia"]

        obj.save()
        messages.info(request, "Información Modificada Correctamente")
        return HttpResponseRedirect(
            reverse_lazy("asociado:verAsociado", args=[kwargs["pkAsociado"]])
        )


class EditarLaboral(CreateView):
    def post(self, request, *args, **kwargs):
        try:
            asociado = Asociado.objects.get(pk=kwargs["pkAsociado"])
            laboral = Laboral.objects.get(asociado=asociado)
            financiera = Financiera.objects.get(asociado=asociado)
            # --- Laboral ---
            asignar_campos(
                laboral,
                request.POST,
                campos=[
                    "ocupacion",
                    "ocupacionOtro",
                    "tipoEmpresa",
                    "tipoEmpresaOtro",
                    "nombreEmpresa",
                    "cargo",
                    "nomRepresenLegal",
                    "nomJefeInmediato",
                    "direccion",
                    "activEcono",
                    "banco",
                    "tipoCuenta",
                    "regimenTributario",
                ],
                upper=True,
            )

            asignar_campos(
                laboral,
                request.POST,
                campos=[
                    "numDocRL",
                    "telefonoJefeInmediato",
                    "telefonoLaboral",
                    "numCuenta",
                    "ciiu",
                ],
                enteros=False,
            )

            asignar_campos(
                laboral,
                request.POST,
                campos=["fechaInicio", "fechaTerminacion"],
                fechas=True,
            )

            asignar_campos(
                laboral,
                request.POST,
                campos=[
                    "admRP",
                    "pep",
                    "declaraRenta",
                    "responsableIva",
                    "tipoContrato",
                    "correoLaboral",
                ],
            )

            asignar_campos(
                laboral,
                request.POST,
                campos=[],
                relaciones={"dptoTrabajo": Departamento, "mpioTrabajo": Municipio},
            )

            laboral.estadoRegistro = True
            laboral.asociado = asociado
            laboral.save()

            # --- Financiera ---
            asignar_campos(
                financiera,
                request.POST,
                campos=[
                    "ingrSalario",
                    "ingrHorasExtras",
                    "ingrPension",
                    "ingrCompensacion",
                    "ingrHonorarios",
                    "ingrVentas",
                    "ingrIntereses",
                    "ingrGiros",
                    "ingrArrendamientos",
                    "ingrOtros",
                    "egrArrendamiento",
                    "egrServiciosPublicos",
                    "egrAportesSalud",
                    "egrTransporte",
                    "egrAlimentacion",
                    "egrObligaciones",
                    "egrTarjetas",
                    "egrCostos",
                    "egrEmbargos",
                    "egrOtros",
                    "operacionesMonedaMonto",
                    "poseeCuentasCuenta",
                ],
                enteros=True,
            )

            asignar_campos(
                financiera,
                request.POST,
                campos=["operacionesMonedaExtranjera", "poseeCuentasMonedaExtranjera"],
            )

            asignar_campos(
                financiera,
                request.POST,
                campos=[
                    "ingrDescripcionOtros",
                    "egrDescripcionOtros",
                    "operacionesMonedaCuales",
                    "operacionesMonedaTipo",
                    "operacionesMoneda",
                    "poseeCuentasMonedaExtranjera",
                    "poseeCuentasBanco",
                    "poseeCuentasMoneda",
                    "poseeCuentasCiudad",
                    "poseeCuentasPais",
                ],
                upper=True,
            )

            financiera.estadoRegistro = True
            financiera.asociado = asociado
            financiera.save()

            # messages.info(request, "Información Modificada Correctamente")
            # return HttpResponseRedirect(
            #     reverse_lazy("asociado:verAsociado", args=[kwargs["pkAsociado"]])
            # )
            return JsonResponse(
                {
                    "ok": True,
                    "mensaje": "Información actualizada correctamente.",
                    "redirect": reverse_lazy(
                        "asociado:verAsociado", args=[kwargs["pkAsociado"]]
                    ),
                }
            )
        except Exception as e:
            return JsonResponse(
                {
                    "ok": False,
                    "mensaje": f"Error al actualizar la información: {str(e)}",
                }
            )


class EditarParametroAsociado(CreateView):

    def post(self, request, *args, **kwargs):
        obj = ParametroAsociado.objects.get(asociado=kwargs["pkAsociado"])
        autorizacion = request.POST.getlist("autorizaciondcto")
        objAsociado = Asociado.objects.get(pk=kwargs["pkAsociado"])
        if len(autorizacion) >= 1:
            obj.autorizaciondcto = True
            objAsociado.tAsociado = TipoAsociado.objects.get(
                pk=request.POST["empresaDcto"]
            )
        else:
            obj.autorizaciondcto = False
            # Si se desactiva el check el asociado pasa a indenpendeinte
            # objAsociado.tAsociado = TipoAsociado.objects.get(pk=1)
        obj.funeraria = ServicioFuneraria.objects.get(pk=request.POST["servFuneraria"])
        obj.primerMes = MesTarifa.objects.get(pk=request.POST["primesMes"])
        obj.save()
        objAsociado.save()
        messages.info(request, "Información Modificada Correctamente")
        return HttpResponseRedirect(
            reverse_lazy("asociado:verAsociado", args=[kwargs["pkAsociado"]])
        )


class Beneficiarios(DetailView):
    model = Asociado
    template_name = "base/asociado/listarBeneficiarios.html"
    context_object_name = "queryAsociado"
    pk_url_kwarg = "pkAsociado"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        beneficiarios = Beneficiario.objects.filter(
            asociado=self.object.pk, estadoRegistro=True
        ).select_related("parentesco", "paisRepatriacion")
        context.update(
            {
                "query": beneficiarios,
                "cuenta": beneficiarios.count(),
                "updateAsociado": "yes",
                "pkAsociado": self.object.pk,
                "vista": 2,
            }
        )
        return context


class CrearBeneficiario(CreateView):
    model = Beneficiario
    form_class = BeneficiarioForm
    template_name = "base/beneficiario/crearBeneficiario.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["asociado_id"] = self.kwargs.get("pkAsociado")
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_asociado = self.kwargs.get("pkAsociado")
        context["pkAsociado"] = pk_asociado
        context["query"] = get_object_or_404(Asociado, pk = pk_asociado)
        context["create"] = "yes"
        return context
    
    def form_valid(self, form):
        pk_asociado = self.kwargs.get("pkAsociado")
        asociado = get_object_or_404(Asociado, pk=pk_asociado)
        
        # Crea el objeto sin guardarlo todavia
        obj = form.save(commit=False)
        obj.asociado = asociado
        obj.nombre = obj.nombre.upper()
        obj.apellido = obj.apellido.upper()
        obj.estadoRegistro = True

        if obj.paisRepatriacion:
            obj.repatriacion = True
            obj.ciudadRepatriacion = obj.ciudadRepatriacion.upper()
        else:
            obj.repatriacion = False
        obj.save()
        
        if obj.repatriacion:
            obj_tarifa = Tarifas.objects.get(pk=4)
            obj_tarifa_asociado = TarifaAsociado.objects.get(asociado_id=asociado)
            obj_tarifa_asociado.cuotaRepatriacionBeneficiarios = (
                (obj_tarifa_asociado.cuotaRepatriacionBeneficiarios or 0) + obj_tarifa.valor
            )
            obj_tarifa_asociado.total += obj_tarifa.valor
            obj_tarifa_asociado.save()
        
        messages.success(self.request, "Beneficiario creado correctamente")

        return super().form_valid(form)
    

    def get_success_url(self):
        return reverse_lazy("asociado:beneficiario", args=[self.kwargs["pkAsociado"]])


class EditarBeneficiario(UpdateView):
    model = Beneficiario
    form_class = BeneficiarioForm
    template_name = "base/beneficiario/editarBeneficiario.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["asociado_id"] = self.kwargs.get("pkAsociado")
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_asociado = self.kwargs.get("pkAsociado")
        id_beneficiario = self.kwargs.get("pk")
        asociado = get_object_or_404(Asociado, id=pk_asociado)
        context["pkAsociado"] = pk_asociado
        context["pk"] = id_beneficiario
        context["query"] = asociado
        context["paisRepatriacion"] = (
            self.object.paisRepatriacion.id if self.object.paisRepatriacion else None
        )

        return context

    def form_valid(self, form):
        obj_original = self.get_object()
        pais_repatriacion_anterior = obj_original.paisRepatriacion

        obj = form.save(commit=False)
        obj.nombre = obj.nombre.upper()
        obj.apellido = obj.apellido.upper()
        obj.estadoRegistro = True

        pk_asociado = self.kwargs.get("pkAsociado")
        asociado = get_object_or_404(Asociado, pk=pk_asociado)
        tarifa_repatriacion = Tarifas.objects.get(pk=4)
        tarifa_asociado = TarifaAsociado.objects.get(asociado=asociado)

        paisRepatriacion = form.cleaned_data["paisRepatriacion"]
        num_repatriaciones = Beneficiario.objects.filter(
            asociado=asociado, repatriacion=True
        ).exclude(pk=obj.pk).count()

        commit = False  # bandera

        # --- CASO 1: quitar repatriación ---
        if pais_repatriacion_anterior and paisRepatriacion is None:
            obj.repatriacion = False
            obj.paisRepatriacion = None
            obj.fechaRepatriacion = None
            obj.ciudadRepatriacion = ""
            obj.primerMesRepatriacion = None
            tarifa_asociado.cuotaRepatriacionBeneficiarios -= tarifa_repatriacion.valor
            tarifa_asociado.total -= tarifa_repatriacion.valor
            tarifa_asociado.save()
            messages.success(self.request, "Repatriación eliminada correctamente")
            commit = True

        # --- CASO 2: agregar nueva repatriación ---
        elif not pais_repatriacion_anterior and paisRepatriacion:
            obj.repatriacion = True
            obj.paisRepatriacion = paisRepatriacion
            obj.fechaRepatriacion = form.cleaned_data["fechaRepatriacion"]
            obj.ciudadRepatriacion = form.cleaned_data["ciudadRepatriacion"].upper()
            if num_repatriaciones > 0:
                tarifa_asociado.cuotaRepatriacionBeneficiarios += tarifa_repatriacion.valor
            else:
                tarifa_asociado.cuotaRepatriacionBeneficiarios = tarifa_repatriacion.valor
            tarifa_asociado.total += tarifa_repatriacion.valor
            tarifa_asociado.save()
            messages.success(self.request, "Repatriación agregada correctamente")
            commit = True

        # --- CASO 3: cambiar país ---
        elif pais_repatriacion_anterior and paisRepatriacion and pais_repatriacion_anterior != paisRepatriacion:
            obj.repatriacion = True
            obj.paisRepatriacion = paisRepatriacion
            obj.fechaRepatriacion = form.cleaned_data["fechaRepatriacion"]
            obj.ciudadRepatriacion = form.cleaned_data["ciudadRepatriacion"].upper()
            messages.success(self.request, "País de repatriación actualizado correctamente")
            commit = True

        else:
            messages.success(self.request, "Beneficiario actualizado correctamente")

        if commit:
            obj.save()

        return super().form_valid(form)


    def get_success_url(self):
        """Redirigir al listado de beneficiarios del asociado"""
        return reverse_lazy("asociado:beneficiario", args=[self.kwargs["pkAsociado"]])


class EliminarBeneficiario(UpdateView):
    model = Beneficiario
    template_name = "base/beneficiario/eliminar.html"

    def get(self, request, *args, **kwargs):
        query = Beneficiario.objects.get(pk=kwargs["pk"])
        return render(
            request,
            self.template_name,
            {
                "pkAsociado": kwargs["pkAsociado"],
                "pk": kwargs["pk"],
                "queryBeneficiario": query,
            },
        )

    def post(self, request, *args, **kwargs):
        obj = Beneficiario.objects.get(pk=kwargs["pk"])
        obj.estadoRegistro = False
        obj.fechaRetiro = date.today()
        if obj.repatriacion == True:
            obj.repatriacion = False
            objTarifa = TarifaAsociado.objects.get(asociado=kwargs["pkAsociado"])
            tarifaRepatriacion = Tarifas.objects.get(pk=4)
            objTarifa.cuotaRepatriacionBeneficiarios = (
                objTarifa.cuotaRepatriacionBeneficiarios - tarifaRepatriacion.valor
            )
            objTarifa.total = objTarifa.total - tarifaRepatriacion.valor
            objTarifa.save()
        obj.save()
        messages.info(request, "Registro Eliminado Correctamente")
        return HttpResponseRedirect(
            reverse_lazy("asociado:beneficiario", args=[kwargs["pkAsociado"]])
        )


class Mascotas(DetailView):
    model = Asociado
    template_name = "base/asociado/listarMascota.html"
    context_object_name = "queryAsociado"
    pk_url_kwarg = "pkAsociado"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryMascotas = Mascota.objects.filter(
            asociado=self.object.pk, estadoRegistro=True
        )
        context.update(
            {"query": queryMascotas, "pkAsociado": self.object.pk, "vista": 3}
        )
        return context


class CrearMascota(CreateView):
    model = Mascota
    form_class = MascotaForm
    template_name = "base/beneficiario/crearMascota.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["asociado_id"] = self.kwargs.get("pkAsociado")
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asociado_id = self.kwargs.get("pkAsociado")
        asociado = get_object_or_404(Asociado, id=asociado_id)
        context["create"] = "yes"
        context["pkAsociado"] = asociado_id
        context["query"] = asociado
        return context
    
    def form_valid(self, form):
        asociado_id = self.kwargs.get("pkAsociado")
        asociado = get_object_or_404(Asociado, pk=asociado_id)
        obj = form.save(commit=False)
        obj.asociado = asociado
        obj.nombre = obj.nombre.upper()
        obj.raza = obj.raza.upper()
        obj.estadoRegistro = True
        obj.save()

        tarifa_mascota = Tarifas.objects.get(pk=3)
        tarifa_asociado = TarifaAsociado.objects.get(asociado = asociado_id)
        tarifa_asociado.cuotaMascota += tarifa_mascota.valor
        tarifa_asociado.total += tarifa_mascota.valor
        tarifa_asociado.save()

        messages.success(self.request, "Mascota creada correctamente")
        return super().form_valid(form)

    def get_success_url(self):
        """Redirigir al listado de mascotas del asociado"""
        return reverse_lazy("asociado:mascota", args=[self.kwargs["pkAsociado"]])


class EditarMascota(UpdateView):
    model = Mascota
    form_class = MascotaForm
    template_name = "base/beneficiario/editarMascota.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["asociado_id"] = self.kwargs.get("pkAsociado")
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asociado_id = self.kwargs.get("pkAsociado")
        mascota_id = self.kwargs.get("pk")
        context["pkAsociado"] = asociado_id
        context["pk"] = mascota_id
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.nombre = obj.nombre.upper()
        obj.raza = obj.raza.upper()
        obj.save()

        messages.success(self.request, "Mascota actualizada correctamente")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("asociado:mascota", args=[self.kwargs["pkAsociado"]])


class EliminarMascota(View):
    template_name = "base/beneficiario/eliminar.html"

    def get(self, request, *args, **kwargs):
        mascota = get_object_or_404(Mascota, pk=kwargs["pk"])
        return render(request, self.template_name, {
            "pkAsociado": kwargs["pkAsociado"],
            "queryMascota": mascota,
            "pk": kwargs["pk"]
        })

    def post(self, request, *args, **kwargs):
        mascota = get_object_or_404(Mascota, pk=kwargs["pk"])
        asociado_id = kwargs["pkAsociado"]

        mascota.estadoRegistro = False
        mascota.fechaRetiro = date.today()
        mascota.save()

        tarifa_mascota = Tarifas.objects.get(pk=3)
        tarifa_asociado = TarifaAsociado.objects.get(asociado=asociado_id)
        tarifa_asociado.cuotaMascota -= tarifa_mascota.valor
        tarifa_asociado.total -= tarifa_mascota.valor
        tarifa_asociado.save()

        messages.success(request, "Mascota eliminada correctamente.")
        return redirect(reverse_lazy("asociado:mascota", args=[asociado_id]))


class VerHistoricoAuxilio(DetailView):
    model = Asociado
    template_name = "base/historico/listarHistoricoAuxilio.html"
    context_object_name = "queryAsociado"
    pk_url_kwarg = "pkAsociado"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryHistorico = HistoricoAuxilio.objects.filter(
            asociado=self.object.pk, estadoRegistro=True
        ).select_related("tipoAuxilio")
        context.update(
            {
                "updateAsociado": "yes",
                "pkAsociado": self.object.pk,
                "query": queryHistorico,
                "queryAsociado": self.object,
                "vista": 4,
            }
        )
        return context


class CrearAuxilio(CreateView):
    form_class = HistoricoAuxilioForm
    template_name = "base/historico/crearAuxilio.html"

    def get(self, request, *args, **kwargs):
        query = Asociado.objects.get(pk=kwargs["pkAsociado"])
        return render(
            request,
            self.template_name,
            {
                "form": self.form_class,
                "create": "yes",
                "pkAsociado": kwargs["pkAsociado"],
                "query": query,
            },
        )

    def post(self, request, *args, **kwargs):
        formulario = HistoricoAuxilioForm(request.POST)
        if formulario.is_valid():
            obj = HistoricoAuxilio()
            obj.fechaSolicitud = formulario.cleaned_data["fechaSolicitud"]
            obj.asociado = Asociado.objects.get(pk=kwargs["pkAsociado"])
            obj.tipoAuxilio = TipoAuxilio.objects.get(
                nombre=formulario.cleaned_data["tipoAuxilio"]
            )
            if obj.entidadBancaria is not None:
                obj.entidadBancaria = formulario.cleaned_data["entidadBancaria"].upper()
            if obj.numCuenta is not None:
                obj.numCuenta = formulario.cleaned_data["numCuenta"]
            obj.valor = obj.tipoAuxilio.valor
            obj.estado = formulario.cleaned_data["estado"]
            obj.estadoRegistro = True
            obj.save()
            messages.info(request, "Auxilio Creado Correctamente")
            return HttpResponseRedirect(
                reverse_lazy("asociado:historicoAuxilio", args=[kwargs["pkAsociado"]])
            )


class DetalleAuxilio(ListView):
    def get(self, request, *args, **kwargs):
        template_name = "base/historico/detalleAuxilio.html"
        obj = HistoricoAuxilio.objects.get(pk=kwargs["pk"])
        objParentesco = None
        if (
            obj.tipoAuxilio.pk == 4
            or obj.tipoAuxilio.pk == 5
            or obj.tipoAuxilio.pk == 6
            or obj.tipoAuxilio.pk == 9
        ):
            objParentesco = Parentesco.objects.all().order_by("nombre")
        return render(
            request,
            template_name,
            {
                "obj": obj,
                "objParentesco": objParentesco,
                "pkAsociado": kwargs["pkAsociado"],
                "pk": kwargs["pk"],
            },
        )

    def post(self, request, *args, **kwargs):
        obj = HistoricoAuxilio.objects.get(pk=kwargs["pk"])
        obj.estado = request.POST["estado"]
        obj.fechaSolicitud = request.POST["fechaSolicitud"]
        obj.entidadBancaria = request.POST["entidadBancaria"].upper()
        obj.numCuenta = request.POST["numCuenta"]
        if (
            obj.tipoAuxilio.pk == 4
            or obj.tipoAuxilio.pk == 5
            or obj.tipoAuxilio.pk == 6
            or obj.tipoAuxilio.pk == 9
        ):
            if obj.nombre is not None:
                obj.nombre = request.POST["nombre"].upper()
                obj.numDoc = request.POST["numDoc"]
                obj.nivelEducativo = request.POST["nivelEducativo"].upper()
            if obj.parentesco is not None:
                obj.parentesco = Parentesco.objects.get(pk=request.POST["parentesco"])
        if request.POST["anexoOne"] != "":
            obj.anexoOne = request.POST["anexoOne"].upper()
        else:
            obj.anexoOne = None
        if request.POST["anexoTwo"] != "":
            obj.anexoTwo = request.POST["anexoTwo"].upper()
        else:
            obj.anexoTwo = None
        if request.POST["anexoThree"] != "":
            obj.anexoThree = request.POST["anexoThree"].upper()
        else:
            obj.anexoThree = None
        if request.POST["anexoFour"] != "":
            obj.anexoFour = request.POST["anexoFour"].upper()
        else:
            obj.anexoFour = None
        if request.POST["anexoFive"] != "":
            obj.anexoFive = request.POST["anexoFive"].upper()
        else:
            obj.anexoFive = None
        if request.POST["anexoSix"] != "":
            obj.anexoSix = request.POST["anexoSix"].upper()
        else:
            obj.anexoSix = None
        if request.POST["anexoSeven"] != "":
            obj.anexoSeven = request.POST["anexoSeven"].upper()
        else:
            obj.anexoSeven = None
        if request.POST["anexoEight"] != "":
            obj.anexoEight = request.POST["anexoEight"].upper()
        else:
            obj.anexoEight = None
        if obj.estado == "OTORGADO" and request.POST["fechaDesembolso"] != "":
            obj.fechaDesembolso = request.POST["fechaDesembolso"]
            obj.observacion = None
        if obj.estado == "DENEGADO":
            obj.fechaDesembolso = None
            obj.observacion = request.POST["observacion"]
        if obj.estado == "REVISION":
            obj.fechaDesembolso = None
            obj.observacion = None
        obj.save()

        messages.info(request, "Información Actualizada Correctamente")
        return HttpResponseRedirect(
            reverse_lazy("asociado:historicoAuxilio", args=[kwargs["pkAsociado"]])
        )


class EliminarAuxilio(UpdateView):
    def get(self, request, *args, **kwargs):
        template_name = "base/historico/eliminar.html"
        queryAuxilio = HistoricoAuxilio.objects.get(pk=kwargs["pk"])
        return render(
            request,
            template_name,
            {
                "pk": kwargs["pk"],
                "pkAsociado": kwargs["pkAsociado"],
                "queryAuxilio": queryAuxilio,
            },
        )

    def post(self, request, *args, **kwargs):
        queryAuxilio = HistoricoAuxilio.objects.get(pk=kwargs["pk"])
        queryAuxilio.estadoRegistro = False
        queryAuxilio.motivoEliminacion = request.POST["observacion"]
        queryAuxilio.save()
        messages.info(request, "Registro Eliminado Correctamente")
        return HttpResponseRedirect(
            reverse_lazy("asociado:historicoAuxilio", args=[kwargs["pkAsociado"]])
        )


class VerHistoricoCredito(DetailView):
    model = Asociado
    template_name = "base/historico/listarHistoricoCredito.html"
    context_object_name = "queryAsociado"
    pk_url_kwarg = "pkAsociado"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryHistorico = (
            HistoricoCredito.objects.prefetch_related(
                Prefetch("codeudor_set", queryset=Codeudor.objects.all())
            )
            .filter(asociado=self.object.pk)
            .select_related("tasaInteres")
        )
        context.update(
            {
                "pkAsociado": self.object.pk,
                "query": queryHistorico,
                "queryAsociado": self.object,
                "vista": 5,
            }
        )
        return context

    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)


@require_http_methods(["GET"])
def verPagosCredito(request, pk):
    if request.method == "GET":
        pagos = HistorialPagos.objects.filter(creditoId=pk)
        forma_pago = FormaPago.objects.all()
        total_pagado = pagos.aggregate(total=Sum("valorPago"))["total"] or 0
        return render(
            request,
            "base/historico/verPagosHistoricoCredito.html",
            {"data": pagos, "total_pagado": total_pagado, "forma_pago": forma_pago},
        )


class CrearHistoricoCredito(ListView):
    def get(self, request, *args, **kwargs):
        template_name = "base/historico/crearHistoricoCredito.html"
        form = HistoricoCreditoForm()
        queryAsociado = Asociado.objects.get(pk=kwargs["pkAsociado"])
        queryFinanciera = queryAsociado.financiera.all().first()
        queryCodeudor = Codeudor.objects.filter()
        context = {
            "pkAsociado": kwargs["pkAsociado"],
            "form": form,
            "asociado": queryAsociado,
            "financiera": queryFinanciera,
            "tasasInteresCredito": TasasInteresCredito.objects.all(),
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        formulario = HistoricoCreditoForm(request.POST)
        if formulario.is_valid():
            obj = HistoricoCredito()
            obj.fechaSolicitud = formulario.cleaned_data["fechaSolicitud"]
            obj.asociado = Asociado.objects.get(pk=kwargs["pkAsociado"])
            obj.lineaCredito = formulario.cleaned_data["lineaCredito"]
            obj.amortizacion = formulario.cleaned_data["amortizacion"]

            # cuando se utiliza en el form model ModelChoiceField, se obtiene es la instancia del objeto
            tasas = formulario.cleaned_data["tasaInteres"]
            obj.tasaInteres = TasasInteresCredito.objects.get(pk=tasas.pk)

            obj.valor = formulario.cleaned_data["valor"]
            obj.cuotas = formulario.cleaned_data["cuotas"]
            obj.valorCuota = formulario.cleaned_data["valorCuota"]
            obj.totalCredito = formulario.cleaned_data["totalCredito"]
            obj.medioPago = formulario.cleaned_data["medioPago"]
            obj.formaDesembolso = formulario.cleaned_data["formaDesembolso"]
            obj.estado = formulario.cleaned_data["estado"]
            obj.pendientePago = formulario.cleaned_data["totalCredito"]
            obj.cuotasPagas = 0
            obj.estadoRegistro = True
            obj.save()
            messages.info(request, "Registro Creado Correctamente")
            return HttpResponseRedirect(
                reverse_lazy("asociado:historicoCredito", args=[kwargs["pkAsociado"]])
            )
        else:
            messages.error(
                request,
                "Hubo un problema al guardar la información, comuniquese con el administrador del sitio.",
            )
            return HttpResponseRedirect(
                reverse_lazy("asociado:historicoCredito", args=[kwargs["pkAsociado"]])
            )


class EditarHistoricoCredito(ListView):
    def get(self, request, *args, **kwargs):
        form_update = get_object_or_404(HistoricoCredito, pk=kwargs["pk"])
        form = HistoricoCreditoForm(
            initial={
                "fechaSolicitud": form_update.fechaSolicitud,
                "valor": form_update.valor,
                "lineaCredito": form_update.lineaCredito,
                "amortizacion": form_update.amortizacion,
                "tasaInteres": form_update.tasaInteres,
                "cuotas": form_update.cuotas,
                "valorCuota": form_update.valorCuota,
                "totalCredito": form_update.totalCredito,
                "medioPago": form_update.medioPago,
                "formaDesembolso": form_update.formaDesembolso,
                "estado": form_update.estado,
                "banco": form_update.banco,
                "numCuenta": form_update.numCuenta,
                "tipoCuenta": form_update.tipoCuenta,
            }
        )
        template_name = "base/historico/editarHistoricoCredito.html"
        context = {
            "form": form,
            "pkAsociado": kwargs["pkAsociado"],
            "pk": kwargs["pk"],
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        formulario = HistoricoCreditoForm(request.POST)
        if formulario.is_valid():
            obj = HistoricoCredito.objects.get(pk=kwargs["pk"])
            obj.fechaSolicitud = formulario.cleaned_data["fechaSolicitud"]
            obj.valor = formulario.cleaned_data["valor"]
            obj.lineaCredito = formulario.cleaned_data["lineaCredito"]
            obj.amortizacion = formulario.cleaned_data["amortizacion"]
            obj.valorCuota = formulario.cleaned_data["valorCuota"]
            obj.totalCredito = formulario.cleaned_data["totalCredito"]
            tasa_interes = formulario.cleaned_data["tasaInteres"]
            obj.tasaInteres = TasasInteresCredito.objects.get(pk=tasa_interes.pk)
            obj.medioPago = formulario.cleaned_data["medioPago"]
            obj.cuotas = formulario.cleaned_data["cuotas"]
            obj.formaDesembolso = formulario.cleaned_data["formaDesembolso"]
            obj.estado = formulario.cleaned_data["estado"]
            obj.banco = (formulario.cleaned_data["banco"] or "").upper()
            obj.tipoCuenta = formulario.cleaned_data["tipoCuenta"]
            obj.numCuenta = formulario.cleaned_data["numCuenta"]
            obj.save()
            messages.info(request, "Registro Editado Correctamente")
            return HttpResponseRedirect(
                reverse_lazy("asociado:historicoCredito", args=[kwargs["pkAsociado"]])
            )


class VerTarifaAsociado(ListView):
    template_name = "base/historico/listarTarifaAsociado.html"

    def get_repatriacion_data(self, asociado):
        repatriacion_titular = RepatriacionTitular.objects.filter(
            asociado=asociado, estadoRegistro=True
        ).first()

        return repatriacion_titular
    
    def get_contadores_data(self, asociado):
        count_repatriacion_beneficiario = Beneficiario.objects.filter(
            asociado=asociado, estadoRegistro=True, repatriacion=True
        ).count()

        count_mascotas = Mascota.objects.filter(
            asociado=asociado, estadoRegistro=True
        ).count()

        return count_repatriacion_beneficiario, count_mascotas

    def get_credito_productos_data(self, asociado):
        queryset = HistoricoVenta.objects.filter(
            asociado=asociado,
            formaPago__in=["CREDITO", "DESCUENTO NOMINA"],
            estadoRegistro=True,
            pendientePago__gt=0,
        )
        total = 0
        for obj_venta in queryset:
            if (obj_venta.cuotas - obj_venta.cuotasPagas) == 1:
                obj_venta.valorCuotas = obj_venta.pendientePago
                total += obj_venta.valorCuotas
            else:
                if (
                    obj_venta.cuotas - obj_venta.cuotasPagas
                ) <= 0 and obj_venta.pendientePago > 0:
                    obj_venta.valorCuotas = obj_venta.pendientePago
                    total += obj_venta.valorCuotas
                elif obj_venta.pendientePago == 0:
                    obj_venta.valorCuotas = 0
                    total += obj_venta.valorCuotas
                elif (
                    obj_venta.pendientePago < obj_venta.valorCuotas
                    and (obj_venta.cuotas - obj_venta.cuotasPagas) >= 1
                ):
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
            estado="OTORGADO",
        )
        total = 0
        for obj_credito in queryset:
            if (obj_credito.cuotas - obj_credito.cuotasPagas) == 1:
                obj_credito.valorCuota = obj_credito.pendientePago
                total += obj_credito.valorCuota
            else:
                if (
                    obj_credito.cuotas - obj_credito.cuotasPagas
                ) <= 0 and obj_credito.pendientePago > 0:
                    obj_credito.valorCuota = obj_credito.pendientePago
                    total += obj_credito.valorCuota
                elif obj_credito.pendientePago == 0:
                    obj_credito.valorCuota = 0
                    total += obj_credito.valorCuota
                elif (
                    obj_credito.pendientePago < obj_credito.valorCuota
                    and (obj_credito.cuotas - obj_credito.cuotasPagas) >= 1
                ):
                    obj_credito.valorCuota = obj_credito.pendientePago
                    total += obj_credito.valorCuota
                else:
                    obj_credito.valorCuota = obj_credito.valorCuota
                    total += obj_credito.valorCuota
        return queryset, total

    def get_vinculacion_data(self, asociado):
        param = ParametroAsociado.objects.filter(
            asociado=asociado, vinculacionPendientePago__gt=0
        ).first()
        if param and param.vinculacionValor:
            cuotas_pendientes = (
                round(param.vinculacionPendientePago / param.vinculacionValor)
                - param.vinculacionCuotas
            )
        else:
            cuotas_pendientes = None
        return param, param.vinculacionValor if param else 0, cuotas_pendientes

    def get_valor_convenio_gasolina(self, asociado):
        convenio_gasolina = 0
        query_convenio = ConvenioHistoricoGasolina.objects.filter(
            asociado=asociado, estado_registro=True
        )
        if query_convenio:
            for obj in query_convenio:
                if obj.pendiente_pago > 0:
                    convenio_gasolina += obj.pendiente_pago
        return convenio_gasolina

    def get(self, request, *args, **kwargs):
        asociado = get_object_or_404(Asociado, pk=kwargs["pkAsociado"])
        tarifa_asociado = TarifaAsociado.objects.select_related("asociado").get(
            asociado=asociado
        )

        convenios = ConveniosAsociado.objects.filter(
            asociado=asociado, estadoRegistro=True
        )

        valor_convenio_gasolina = self.get_valor_convenio_gasolina(asociado)

        adicional = tarifa_asociado.cuotaAdicionales > 0

        repatriacion_titular = self.get_repatriacion_data(asociado)

        count_repatriacion_beneficiario, count_mascotas = self.get_contadores_data(asociado)

        credito_productos_qs, total_credito_productos = self.get_credito_productos_data(
            asociado
        )
        credito_general_qs, total_credito_general = self.get_credito_general_data(
            asociado
        )
        vinculacion_param, cuota_vinculacion, vinculacion_cuotas_pte = (
            self.get_vinculacion_data(asociado)
        )

        qs_seguro_vida = (
            HistoricoSeguroVida.objects.filter(asociado_id=asociado, estadoRegistro=True)
            .first()
        )

        total_tarifa = (
            # (tarifa_asociado.cuotaAporte or 0)
            # + (tarifa_asociado.cuotaBSocial or 0)
            # + (tarifa_asociado.cuotaMascota or 0)
            # + (tarifa_asociado.cuotaSeguroVida or 0)
            # + (tarifa_asociado.cuotaAdicionales or 0)
            # + (tarifa_asociado.cuotaCoohopAporte or 0)
            # + (tarifa_asociado.cuotaCoohopBsocial or 0)
            # + (tarifa_asociado.cuotaConvenio or 0)
            # + (tarifa_asociado.cuotaRepatriacionBeneficiarios or 0)
            # + (tarifa_asociado.cuotaRepatriacionTitular or 0)
            + tarifa_asociado.total
            + (total_credito_productos or 0)
            + (total_credito_general or 0)
            + (cuota_vinculacion or 0)
            + (valor_convenio_gasolina or 0)
        )
        
        context = {
            "updateAsociado": "yes",
            "pkAsociado": asociado.pk,
            "query": tarifa_asociado,
            "adicional": adicional,
            "queryRepatriacionTitular": repatriacion_titular,
            "count_repatriacion_beneficiario": count_repatriacion_beneficiario,
            "count_mascota": count_mascotas,
            "queryConvenio": convenios,
            "vista": 8,
            "query_credito_prod": credito_productos_qs,
            "queryCredito": credito_general_qs,
            "queryVinculacion": vinculacion_param,
            "vinculacionCuotasPte": vinculacion_cuotas_pte,
            "cuotaGasolina": valor_convenio_gasolina,
            "qs_seguro_vida":qs_seguro_vida,
            "totalTarifaAsociado": total_tarifa,
        }
        return render(request, self.template_name, context)


@require_http_methods(["POST", "GET"])
def EditarConvenioGasolina(request, pkConvenio):
    if request.method == "POST":
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
                        estado_registro=True,
                    )
                    nuevos_ids.append(
                        {"id": nuevo.id, "mes_id": mes_id, "valor": valor}
                    )

            return JsonResponse(
                {
                    "success": True,
                    "nuevos": nuevos_ids,
                    "message": "Datos guardados correctamente.",
                }
            )

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    else:
        convenio = ConveniosAsociado.objects.get(pk=pkConvenio)
        meses = MesTarifa.objects.filter(
            pk__gte=convenio.primerMes.pk, pk__lte=9000
        ).values("id", "concepto")
        meses_seleccionados = ConvenioHistoricoGasolina.objects.filter(
            convenio=pkConvenio
        ).values_list("mes_tarifa_id", flat=True)
        meses = meses.exclude(id__in=meses_seleccionados)
        historico = ConvenioHistoricoGasolina.objects.filter(convenio=pkConvenio)
        return render(
            request,
            "base/historico/convenio_gasolina.html",
            {"meses": list(meses), "pkConvenio": pkConvenio, "historico": historico},
        )


@require_http_methods(["POST"])
def EliminarDetalleGasolina(request, pkConvenio):
    if request.method == "POST":
        detalle = get_object_or_404(ConvenioHistoricoGasolina, pk=pkConvenio)
        detalle.delete()
        return JsonResponse({"status": "ok"})
    else:
        return JsonResponse({"error": "Metodo no permitido"})


class CrearAdicionalAsociado(UpdateView):
    model = TarifaAsociado
    form_class = TarifaAsociadoAdicionalForm
    template_name = "base/historico/crearAdicional.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pkAsociado"] = self.object.asociado_id
        context["create"] = True
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["asociado_id"] = self.object.asociado_id
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.estadoAdicional = True

        # Recuperar el valor anterior antes de guardar
        valor_anterior = TarifaAsociado.objects.get(pk=obj.pk).cuotaAdicionales or 0
        valor_nuevo = obj.cuotaAdicionales or 0

        diferencia = valor_nuevo - valor_anterior
        obj.total = (obj.total or 0) + diferencia

        obj.save()
        messages.success(self.request, "Adicional guardado correctamente.")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("asociado:tarifaAsociado", args=[self.object.asociado_id])


class EliminarAdicionalAsociado(UpdateView):
    def get(self, request, *args, **kwargs):
        template_name = "base/asociado/eliminarAdicional.html"
        query = TarifaAsociado.objects.only(
            "cuotaAdicionales", "id", "fechaInicioAdicional"
        ).get(pk=kwargs["pk"])
        context = {
            "query": query,
            "pk": kwargs["pk"],
            "pkAsociado": kwargs["pkAsociado"],
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        obj = TarifaAsociado.objects.get(pk=kwargs["pk"])
        obj.total = obj.total - obj.cuotaAdicionales
        obj.cuotaAdicionales = 0
        obj.fechaFinAdicional = date.today()
        obj.estadoAdicional = False
        obj.save()
        messages.info(request, "Registro Eliminado Correctamente")
        return HttpResponseRedirect(
            reverse_lazy("asociado:tarifaAsociado", args=[kwargs["pkAsociado"]])
        )


class VerSeguroVida(DetailView):
    model = Asociado
    template_name = "base/asociado/listarSeguroVida.html"
    context_object_name = "queryAsociado"
    pk_url_kwarg = "pkAsociado"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        querySeguroVida = HistoricoSeguroVida.objects.filter(asociado=self.object.pk)
        context.update(
            {
                "pkAsociado": self.object.pk,
                "query": querySeguroVida,
                "queryAsociado": self.object,
                "vista": 6,
            }
        )
        return context


class CrearSeguroVida(CreateView):
    model = HistoricoSeguroVida
    form_class = HistoricoSeguroVidaForm
    template_name = "base/historico/crearSeguroVida.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["asociado_id"] = self.kwargs.get("pkAsociado")
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asociado_id = self.kwargs.get("pkAsociado")
        context["pkAsociado"] = asociado_id
        context["create"] = "yes"
        context["query"] = get_object_or_404(Asociado, id = asociado_id)
        return context
    
    def form_valid(self, form):
        asociado_id = self.kwargs.get('pkAsociado')
        asociado = get_object_or_404(Asociado, pk = asociado_id)

        obj = form.save(commit=False)
        obj.asociado = asociado
        obj.estadoRegistro = True
        obj.save()

        obj_tarifa_asociado = TarifaAsociado.objects.get(asociado_id = asociado_id)
        obj_tarifa_asociado.cuotaSeguroVida = obj.valorPago
        obj_tarifa_asociado.total += obj.valorPago
        obj_tarifa_asociado.save()
        
        messages.info(self.request, "Seguro de Vida Creado Correctamente")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("asociado:seguroVida", args=[self.kwargs["pkAsociado"]]) 


class EditarSeguroVida(UpdateView):
    model = HistoricoSeguroVida
    form_class = HistoricoSeguroVidaForm
    template_name = "base/historico/crearSeguroVida.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["asociado_id"] = self.kwargs.get("pkAsociado")
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asociado_id = self.kwargs.get('pkAsociado')
        seguro_vida_id = self.kwargs.get('pk')
        context["pkAsociado"] = asociado_id
        context["pk"] = seguro_vida_id
        return context
    
    def form_valid(self, form):
        asociado_id = self.kwargs.get('pkAsociado')

        obj = form.save(commit=False)
        valor_actual = self.get_object().valorPago

        obj_tarifa_asociado = TarifaAsociado.objects.get(asociado = asociado_id)

        fecha_retiro = form.cleaned_data.get("fechaRetiro")

        if fecha_retiro:
            obj.fecha_retiro = fecha_retiro
            obj.estadoRegistro = False
            obj_tarifa_asociado.cuotaSeguroVida = 0
            obj_tarifa_asociado.total -= valor_actual
            obj_tarifa_asociado.save()
            messages.info(self.request, "Seguro de vida Eliminado Correctamente")
            return super().form_valid(form)
        
        obj.save()
        obj_tarifa_asociado.cuotaSeguroVida = obj.valorPago

        diferencia = obj.valorPago - valor_actual
        obj_tarifa_asociado.total += diferencia
        obj_tarifa_asociado.save()

        messages.info(self.request, "Seguro de vida Modificado Correctamente")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("asociado:seguroVida", args=[self.kwargs["pkAsociado"]])


class VerCoohoperativitos(DetailView):
    model = Asociado
    template_name = "base/beneficiario/listarCoohoperativitos.html"
    context_object_name = "queryAsociado"
    pk_url_kwarg = "pkAsociado"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryCoohoperativitos = Coohoperativitos.objects.filter(
            asociado=self.object.pk, estadoRegistro=True
        )
        context.update(
            {
                "updateAsociado": "yes",
                "pkAsociado": self.object.pk,
                "query": queryCoohoperativitos,
                "queryAsociado": self.object,
                "vista": 7,
            }
        )
        return context


class CrearCoohoperativito(UpdateView):
    form_class = CoohoperativitoForm
    template_name = "base/beneficiario/crearCoohoperativito.html"

    def get(self, request, *args, **kwargs):
        query = Asociado.objects.get(pk=kwargs["pkAsociado"])
        return render(
            request,
            self.template_name,
            {
                "form": self.form_class,
                "create": "yes",
                "pkAsociado": kwargs["pkAsociado"],
                "query": query,
            },
        )

    def post(self, request, *args, **kwargs):
        formulario = CoohoperativitoForm(request.POST)
        if formulario.is_valid():
            obj = Coohoperativitos()
            obj.asociado = Asociado.objects.get(pk=kwargs["pkAsociado"])
            obj.nombre = formulario.cleaned_data["nombre"].upper()
            obj.apellido = formulario.cleaned_data["apellido"].upper()
            obj.tipoDocumento = formulario.cleaned_data["tipoDocumento"]
            obj.numDocumento = formulario.cleaned_data["numDocumento"]
            obj.fechaNacimiento = formulario.cleaned_data["fechaNacimiento"]
            obj.estadoRegistro = True
            obj.fechaIngreso = formulario.cleaned_data["fechaIngreso"]
            obj.save()
            # se consulta cuantos coohoperativitos tiene actualmente
            numCoohoperativitos = Coohoperativitos.objects.filter(
                asociado=kwargs["pkAsociado"], estadoRegistro=True
            ).count()
            objTarifaAsociado = TarifaAsociado.objects.get(
                asociado=kwargs["pkAsociado"]
            )
            # valor de aportes coohoperativitos
            objTarifaCooho = Tarifas.objects.get(pk=6)
            # valor de b social coohoperativitos
            objTarifaCoohoBSocial = Tarifas.objects.get(pk=5)
            objTarifaAsociado.cuotaCoohopAporte = (
                objTarifaCooho.valor * numCoohoperativitos
            )
            objTarifaAsociado.cuotaCoohopBsocial = (
                objTarifaCoohoBSocial.valor * numCoohoperativitos
            )
            objTarifaAsociado.total = (
                objTarifaAsociado.total
                + objTarifaCooho.valor
                + objTarifaCoohoBSocial.valor
            )
            objTarifaAsociado.save()
            messages.info(request, "Registro Creado Correctamente")
            return HttpResponseRedirect(
                reverse_lazy("asociado:coohoperativitos", args=[kwargs["pkAsociado"]])
            )


class EditarCoohoperativito(UpdateView):
    template_name = "base/beneficiario/crearCoohoperativito.html"

    def get(self, request, *args, **kwargs):
        form_update = get_object_or_404(Coohoperativitos, pk=kwargs["pk"])
        form = CoohoperativitoForm(
            initial={
                "nombre": form_update.nombre,
                "apellido": form_update.apellido,
                "tipoDocumento": form_update.tipoDocumento,
                "numDocumento": form_update.numDocumento,
                "fechaNacimiento": form_update.fechaNacimiento,
                "fechaIngreso": form_update.fechaIngreso,
            }
        )
        return render(
            request,
            self.template_name,
            {"form": form, "pkAsociado": kwargs["pkAsociado"], "pk": kwargs["pk"]},
        )

    def post(self, request, *args, **kwargs):
        formulario = CoohoperativitoForm(request.POST)
        if formulario.is_valid():
            obj = Coohoperativitos.objects.get(pk=kwargs["pk"])
            obj.nombre = formulario.cleaned_data["nombre"].upper()
            obj.apellido = formulario.cleaned_data["apellido"].upper()
            obj.tipoDocumento = formulario.cleaned_data["tipoDocumento"]
            obj.numDocumento = formulario.cleaned_data["numDocumento"]
            obj.fechaNacimiento = formulario.cleaned_data["fechaNacimiento"]
            obj.fechaIngreso = formulario.cleaned_data["fechaIngreso"]
            obj.save()
            messages.info(request, "Registro Modificado Correctamente")
            return HttpResponseRedirect(
                reverse_lazy("asociado:coohoperativitos", args=[kwargs["pkAsociado"]])
            )


class EliminarCoohoperativito(UpdateView):
    model = Coohoperativitos
    template_name = "base/beneficiario/eliminar.html"

    def get(self, request, *args, **kwargs):
        queryCoohop = Coohoperativitos.objects.get(pk=kwargs["pk"])
        tarifaCooh = Tarifas.objects.filter(id__in=[5, 6]).aggregate(
            total_valor=Sum("valor")
        )
        return render(
            request,
            self.template_name,
            {
                "pkAsociado": kwargs["pkAsociado"],
                "pk": kwargs["pk"],
                "queryCoohop": queryCoohop,
                "tarifaCooh": tarifaCooh,
            },
        )

    def post(self, request, *args, **kwargs):
        obj = Coohoperativitos.objects.get(pk=kwargs["pk"])
        obj.estadoRegistro = False
        obj.fechaRetiro = date.today()
        obj.save()
        # Valor quemado de la b social coohoperativios, pk = 5
        objTarifaBsocial = Tarifas.objects.get(pk=5)
        # Valor quemado del aporte coohoperativios, pk = 6
        objTarifaAporte = Tarifas.objects.get(pk=6)
        objTarifaAsoc = TarifaAsociado.objects.get(asociado=kwargs["pkAsociado"])
        objTarifaAsoc.cuotaCoohopAporte = (
            objTarifaAsoc.cuotaCoohopAporte - objTarifaAporte.valor
        )
        objTarifaAsoc.cuotaCoohopBsocial = (
            objTarifaAsoc.cuotaCoohopBsocial - objTarifaBsocial.valor
        )
        objTarifaAsoc.total = (
            objTarifaAsoc.total - objTarifaBsocial.valor - objTarifaAporte.valor
        )
        objTarifaAsoc.save()
        messages.info(request, "Registro Eliminado Correctamente")
        return HttpResponseRedirect(
            reverse_lazy("asociado:coohoperativitos", args=[kwargs["pkAsociado"]])
        )


class VerHistorialPagos(DetailView):
    model = Asociado
    template_name = "base/historico/listarHistorialPago.html"
    context_object_name = "queryAsociado"
    pk_url_kwarg = "pkAsociado"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryPagos = (
            HistorialPagos.objects.filter(asociado=self.object.pk)
            .select_related("formaPago", "mesPago", "convenio_gasolina_id")
            .order_by("fechaPago", "id")
        )
        context.update(
            {
                "updateAsociado": "yes",
                "pkAsociado": self.object.pk,
                "query": queryPagos,
                "queryAsociado": self.object,
                "vista": 9,
            }
        )
        return context


class DetalleHistorialPago(ListView):
    def get(self, request, *args, **kwargs):
        template_name = "base/historico/detallePago.html"
        query = HistorialPagos.objects.get(pk=kwargs["pk"])
        return render(request, template_name, {"query": query})


class DescargarFormatos(DetailView):
    model = Asociado
    template_name = "base/asociado/formatos.html"
    context_object_name = "query"
    pk_url_kwarg = "pkAsociado"

    def get_queryset(self):
        return Asociado.objects.select_related(
            "tAsociado",
            "mpioDoc",
            "deptoResidencia",
            "dtoNacimiento",
            "mpioNacimiento",
            "mpioResidencia",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asociado = self.object
        fecha_actual = date.today()

        try:
            obj_financiera = Financiera.objects.get(asociado=asociado)
            obj_parametro = ParametroAsociado.objects.get(asociado=asociado)
            obj_laboral = Laboral.objects.select_related(
                "mpioTrabajo", "dptoTrabajo"
            ).get(asociado=asociado)

            beneficiarios = Beneficiario.objects.filter(
                asociado=asociado, estadoRegistro=True
            ).select_related("paisRepatriacion", "parentesco")

            mascotas = Mascota.objects.filter(asociado=asociado, estadoRegistro=True)

            context.update(
                {
                    "updateAsociado": "yes",
                    "pkAsociado": asociado.pk,
                    "residenciaExiste": "yes",
                    "queryLaboral": obj_laboral,
                    "actualizacion": asociado.fechaIngreso != fecha_actual,
                    "objFinanciera": obj_financiera,
                    "fechaActual": fecha_actual,
                    "objParametroAsociado": obj_parametro,
                    "objBeneficiario": beneficiarios,
                    "cuentaBeneficiario": beneficiarios.count(),
                    "objMascota": mascotas,
                    "cuentaMascota": mascotas.count(),
                    "vista": 10,
                }
            )
        except (
            Financiera.DoesNotExist,
            ParametroAsociado.DoesNotExist,
            Laboral.DoesNotExist,
        ):
            messages.warning(
                self.request, "Información incompleta para descargar formatos."
            )
            context.update({"mensaje": "yes", "pkAsociado": asociado.pk, "vista": 10})

        return context


# Descarga Formato Auxilios
class ModalFormato(ListView):
    def get(self, request, *args, **kwargs):
        template_name = "base/asociado/formato2.html"

        # Formato Vinculacion y Actualizacion Datos
        if kwargs["formato"] == 1:
            qs_asociado = Asociado.objects.values('fechaActualizacionDatos').get(id = kwargs["pkAsociado"])
            return render (
                request,
                template_name,
                {
                    "pkAsociado": kwargs["pkAsociado"],
                    "formato": kwargs["formato"],
                    "fechaActualizacionDatos": qs_asociado,
                }
            )
        # Formato Auxilio
        elif kwargs["formato"] == 3:
            objAuxilio = HistoricoAuxilio.objects.filter(
                asociado=kwargs["pkAsociado"], estado__in=["REVISION", "OTORGADO"], estadoRegistro=True
            )
            return render(
                request,
                template_name,
                {
                    "pkAsociado": kwargs["pkAsociado"],
                    "formato": kwargs["formato"],
                    "objAuxilio": objAuxilio,
                },
            )
        # Formato Extracto
        elif kwargs["formato"] == 4:
            objParametroAsoc = ParametroAsociado.objects.get(
                asociado=kwargs["pkAsociado"]
            )
            objMes = MesTarifa.objects.filter(pk__gte=objParametroAsoc.primerMes.pk)
            return render(
                request,
                template_name,
                {
                    "pkAsociado": kwargs["pkAsociado"],
                    "formato": kwargs["formato"],
                    "objMes": objMes,
                },
            )
        # Formato Otorgamiento de credito
        elif kwargs["formato"] == 5:
            queryHistoricoCredito = HistoricoCredito.objects.filter(
                asociado=kwargs["pkAsociado"]
            ).order_by("fechaSolicitud")

            # Agregamos prefetch_related para obtener todos los codeudores asociados a cada historicoCredito
            queryHistoricoCredito = queryHistoricoCredito.prefetch_related(
                Prefetch(
                    "codeudor_set",
                    queryset=Codeudor.objects.all(),
                    to_attr="codeudores",
                )
            )
            queryAsociado = Asociado.objects.get(pk=kwargs["pkAsociado"])
            queryParametroAsoc = (
                ParametroAsociado.objects.filter(asociado=kwargs["pkAsociado"])
                .values("autorizaciondcto", "asociado__tAsociado__concepto")
                .first()
            )
            queryLaboral = Laboral.objects.get(asociado=kwargs["pkAsociado"])
            fechaActual = date.today()
            context = {
                "pkAsociado": kwargs["pkAsociado"],
                "formato": kwargs["formato"],
                "query": queryHistoricoCredito,
                "queryAsociado": queryAsociado,
                "fechaActual": fechaActual,
                "queryLab": queryLaboral,
                "queryParametroAsoc": queryParametroAsoc,
            }
            return render(request, template_name, context)


# Descarga Formato Auxilios
class GenerarFormato(View):
    @medir_rendimiento("formato_extracto")
    def get(self, request, *args, **kwargs):
        template_name = "base/asociado/generar.html"
        objAsoc = Asociado.objects.select_related("mpioResidencia").get(
            pk=kwargs["pkAsociado"]
        )

        # Formato 4
        if kwargs["formato"] == 4:
            id_asociado = kwargs["pkAsociado"]
            saldos = "saldos" in request.GET
            mes = MesTarifa.objects.get(pk=request.GET["mes"])
            formato = kwargs["formato"]
            context = obtenerValorExtracto(id_asociado, saldos, mes)
            
            context["objAsoc"] = objAsoc
            context["formato"] = formato
    
            # Preparar datos para JSON
            context_serializable = {
                # ================================================================
                # IDENTIFICACIÓN Y ENCABEZADO
                # ================================================================
                "formato": formato,
                "fechaCorte": context["fechaCorte"].strftime("%Y-%m-%d"),
                "nombre": f"{objAsoc.nombre} {objAsoc.apellido}",
                "numDocumento": objAsoc.numDocumento,
                "mpioResidencia": str(objAsoc.mpioResidencia),
                "direccion": objAsoc.direccion,
                "numCelular": objAsoc.numCelular,

                # ================================================================
                # INFORMACIÓN GENERAL DEL EXTRACTO
                # ================================================================
                "mes": context["mes"].concepto,
                "saldo": context["saldo"],
                "saldoDiferencia": context["saldoDiferencia"],  # ← NUEVO
                "pagoTotal": context["pagoTotal"],
                "mensaje": context["mensaje"],

                # ================================================================
                # CUOTAS Y TARIFAS GENERALES
                # ================================================================
                "cuotaPeriodica": context["cuotaPeriodica"],
                "cuotaCoohop": context["cuotaCoohop"],
                "cuotaVencida": context["cuotaVencida"],
                "valorVencido": context["valorVencido"],

                # ================================================================
                # SERVICIOS (totales por categoría)
                # ================================================================
                "valorVencidoMasc": context["valorVencidoMasc"],
                "valorVencidoRep": context["valorVencidoRep"],
                "valorVencidoRepBeneficiarios": context["valorVencidoRepBeneficiarios"],
                "valorVencidoRepTitular": context["valorVencidoRepTitular"],
                "valorVencidoSeg": context["valorVencidoSeg"],
                "valorVencidoAdic": context["valorVencidoAdic"],
                "valorVencidoCoohop": context["valorVencidoCoohop"],

                # ================================================================
                # CONVENIOS
                # ================================================================
                "valorVencidoConvenio": context["valorVencidoConvenio"],
                "valorVencidoConveniosNormales": context["valorVencidoConveniosNormales"],
                "valorVencidoGasolina": context["valorVencidoGasolina"],
                
                "convenios": [
                    {
                        "concepto": conv.convenio.concepto,
                        "cantidad_meses": conv.cantidad_meses,
                        "valor_mes": conv.convenio.valor,
                        "valor_vencido": conv.valor_vencido_convenio,
                    }
                    for conv in context["objConvenio"]
                ],
                "convenioGasolina": context["convenioGasolina"],

                # ================================================================
                # CRÉDITOS Y VENTAS HOME ELEMENTS
                # ================================================================
                "creditos": context["creditos"],
                "ventasHomeElements": context["ventasHomeElements"],
                "valorTotalCreditos": context["valorTotalCreditos"],

                # ================================================================
                # BENEFICIARIOS
                # ================================================================
                "beneficiarios": [
                    {
                        "nombre": f"{b.nombre} {b.apellido}",
                        "parentesco": str(b.parentesco),
                        "paisRepatriacion": str(b.paisRepatriacion) if b.paisRepatriacion else "",
                        "repatriacion": b.repatriacion,  # Indica si tiene repatriación
                    }
                    for b in context["objBeneficiario"]
                ],
                "cuentaBeneficiario": context["cuentaBeneficiario"],
                "cuentaBeneficiarioConRepatriacion": context["cuentaBeneficiarioConRepatriacion"],

                # ================================================================
                # MASCOTAS
                # ================================================================
                "mascotas": [
                    {
                        "nombre": m.nombre,
                        "tipo": m.tipo,
                    }
                    for m in context["objMascota"]
                ],
                "cuentaMascota": context["cuentaMascota"],

                # ================================================================
                # REPATRIACIÓN TITULAR Y SEGUROS
                # ================================================================
                "repatriacionTitular": (
                    {
                        "pais": str(context["objRepatriacionTitular"].paisRepatriacion),
                        "valor": context["valorVencidoRepTitular"],
                    }
                    if context["objRepatriacionTitular"]
                    else None
                ),
                "seguroVida": (
                    {
                        "valorPago": context["objSeguroVida"].valorPago,
                        "valor": context["valorVencidoSeg"],
                    }
                    if context["objSeguroVida"]
                    else None
                ),

                # ================================================================
                # CONCEPTOS DETALLADOS PARA PDF
                # ================================================================
                "conceptos_detallados": context["conceptos_detallados"],
            }

            context["context_json"] = context_serializable
            
            return render(request, template_name, context)


class UtilidadesAsociado(ListView):
    model = Asociado
    template_name = "base/asociado/utilidades.html"


class CrearRepatriacionTitular(CreateView):
    model = RepatriacionTitular
    form_class = RepatriacionTitularForm
    template_name = "base/asociado/repatriacionTitular.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asociado_id = self.kwargs.get('pkAsociado')
        context['create'] = True
        context['pkAsociado'] = asociado_id
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['asociado_id'] = self.kwargs.get('pkAsociado')
        return kwargs

    def form_valid(self, form):
        asociado_id = self.kwargs['pkAsociado']
        obj_asociado = get_object_or_404(Asociado, pk = asociado_id)
        obj_tarifa_asociado = TarifaAsociado.objects.get(asociado = asociado_id)
        obj_tarifa = Tarifas.objects.get(pk = 4)
        obj = form.save(commit=False)
        obj.estadoRegistro = True
        obj.asociado = obj_asociado
        obj.ciudadRepatriacion = obj.ciudadRepatriacion.upper()

        
        obj_tarifa_asociado.cuotaRepatriacionTitular = obj_tarifa.valor
        obj_tarifa_asociado.total += obj_tarifa.valor
        obj_tarifa_asociado.save()

        obj.save()
        messages.info(self.request, "Repatriación titular creada correctamente")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("asociado:tarifaAsociado", args=[self.kwargs["pkAsociado"]])


class VerRepatriacionTitular(UpdateView):
    model = RepatriacionTitular
    form_class = RepatriacionTitularForm
    template_name = 'base/asociado/repatriacionTitular.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asociado_id = self.kwargs.get('pkAsociado')
        context['pkAsociado'] = asociado_id
        context['create'] = False
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['asociado_id'] = self.kwargs.get('pkAsociado')
        return kwargs
    
    def form_valid(self, form):
        # Guardar los cambios primero
        obj = form.save(commit=False)
        obj.ciudadRepatriacion = obj.ciudadRepatriacion.upper()
        obj.save()

        messages.info(self.request, 'Repatriación actualizada correctamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('asociado:tarifaAsociado', args=[self.kwargs['pkAsociado']])


class EliminarRepatriacionTitular(DeleteView):
    model = RepatriacionTitular
    template_name = 'base/beneficiario/eliminar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asociado_id = self.kwargs.get('pkAsociado')
        obj_repatriacion = get_object_or_404(RepatriacionTitular, pk = self.kwargs.get('pk'))
        context['pkAsociado'] = asociado_id
        context['queryRepatriacionTitular'] = obj_repatriacion
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        asociado_id = self.kwargs.get('pkAsociado')

        obj_tarifa_asociado = get_object_or_404(TarifaAsociado, asociado=asociado_id)

        self.object.estadoRegistro = False
        self.object.fechaRetiro = date.today()
        self.object.save()

        obj_tarifa_asociado.total -= obj_tarifa_asociado.cuotaRepatriacionTitular
        obj_tarifa_asociado.cuotaRepatriacionTitular = 0
        obj_tarifa_asociado.save()

        messages.info(self.request, "Repatriación eliminada correctamente.")
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('asociado:tarifaAsociado', args=[self.kwargs['pkAsociado']])


class CrearConvenio(CreateView):
    model = ConveniosAsociado
    form_class = ConvenioAsociadoForm
    template_name = 'base/asociado/crearConvenio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create'] = True
        context['pkAsociado'] = self.kwargs.get('pkAsociado')
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['asociado_id'] = self.kwargs.get('pkAsociado')
        return kwargs

    def form_valid(self, form):
        asociado_id = self.kwargs.get('pkAsociado')
        obj_asociado = get_object_or_404(Asociado, pk = asociado_id)
        obj_tarifa_asociado = TarifaAsociado.objects.get(asociado = asociado_id)
        obj = form.save(commit=False)

        # Obtenemos el objeto del convenio a crear
        obj_convenio = Convenio.objects.get(id = obj.convenio_id)

        obj.asociado = obj_asociado
        obj.estadoRegistro = True

        obj_tarifa_asociado.cuotaConvenio += obj_convenio.valor
        obj_tarifa_asociado.total += obj_convenio.valor

        obj.save()
        obj_tarifa_asociado.save()

        messages.info(self.request, "Convenio registrado correctamente.")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("asociado:tarifaAsociado", args=[self.kwargs['pkAsociado']])


class EditarConvenioAsociado(UpdateView):
    template_name = "base/asociado/crearConvenio.html"

    def get(self, request, *args, **kwargs):
        query = ConveniosAsociado.objects.get(pk=kwargs["pk"])
        context = {
            "query": query,
            "pkAsociado": kwargs["pkAsociado"],
            "pk": kwargs["pk"],
            "meses": MesTarifa.objects.all(),
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        obj = ConveniosAsociado.objects.get(pk=kwargs["pk"])
        obj.fechaIngreso = request.POST["fechaIngreso"]
        obj.primerMes = MesTarifa.objects.get(pk=request.POST["primerMes"])
        obj.save()
        messages.info(request, "Registro Modificado Correctamente")
        return HttpResponseRedirect(
            reverse_lazy("asociado:tarifaAsociado", args=[kwargs["pkAsociado"]])
        )


class EliminarConvenioAsociado(UpdateView):
    def get(self, request, *args, **kwargs):
        template_name = "base/asociado/eliminarConvenio.html"
        query = (
            ConveniosAsociado.objects.select_related("convenio")
            .only("fechaIngreso", "id", "convenio__concepto", "convenio__valor")
            .get(pk=kwargs["pk"])
        )

        context = {
            "query": query,
            "pk": kwargs["pk"],
            "pkAsociado": kwargs["pkAsociado"],
        }

        if query.convenio.pk == 4:
            valor = 0
            query = ConvenioHistoricoGasolina.objects.filter(
                asociado=kwargs["pkAsociado"], estado_registro=True
            )
            for obj in query:
                valor += obj.pendiente_pago
            context.update({"valor": valor})

        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        obj = ConveniosAsociado.objects.get(pk=kwargs["pk"])
        obj.estadoRegistro = False
        obj.fechaRetiro = date.today()
        obj.save()
        objTarifa = TarifaAsociado.objects.get(asociado=kwargs["pkAsociado"])
        objTarifa.cuotaConvenio = objTarifa.cuotaConvenio - int(request.POST["valor"])
        objTarifa.total = objTarifa.total - int(request.POST["valor"])
        objTarifa.save()
        messages.info(request, "Registro Eliminado Correctamente")
        return HttpResponseRedirect(
            reverse_lazy("asociado:tarifaAsociado", args=[kwargs["pkAsociado"]])
        )


class CrearCodeudor(CreateView):
    model = Codeudor
    form_class = CodeudorForm
    template_name = "base/historico/crearCodeudor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "operation": "crear",
                "pk": self.kwargs["pk"],
                "pkAsociado": self.kwargs["pkAsociado"],
                "query_dpto": Departamento.objects.values("id", "nombre"),
                "query_mpio": Municipio.objects.values(
                    "id", "nombre", "departamento", "departamento__nombre"
                ),
            }
        )
        return context

    def form_valid(self, form):
        codeudor = form.save(commit=False)
        # Asignar valores manualmente
        codeudor.nombre = codeudor.nombre.upper()
        codeudor.apellido = codeudor.apellido.upper()
        codeudor.nacionalidad = codeudor.nacionalidad.upper()
        codeudor.barrio = codeudor.barrio.upper()
        codeudor.direccion = codeudor.direccion.upper()
        codeudor.historicoCredito = HistoricoCredito.objects.get(pk=self.kwargs["pk"])
        codeudor.asociado = Asociado.objects.get(pk=self.kwargs["pkAsociado"])
        codeudor.save()
        messages.info(self.request, "Codeudor creado correctamente.")
        return HttpResponseRedirect(
            reverse_lazy("asociado:historicoCredito", args=[self.kwargs["pkAsociado"]])
        )


class EditarCodeudor(UpdateView):
    model = Codeudor
    form_class = CodeudorForm
    template_name = "base/historico/crearCodeudor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_dpto = Departamento.objects.values("id", "nombre")
        query_mpio = Municipio.objects.values(
            "id", "nombre", "departamento", "departamento__nombre"
        )

        context.update(
            {
                "operation": "editar",
                "pk": self.kwargs["pk"],
                "pkAsociado": self.kwargs["pkAsociado"],
                "query_dpto": query_dpto,
                "query_mpio": query_mpio,
            }
        )
        return context

    def form_valid(self, form):
        # Verifica que el formulario sea válido antes de guardar
        if form.is_valid():
            form.save()  # Asegúrate de que el formulario esté guardando correctamente el objeto
            messages.info(self.request, "Codeudor modificado correctamente.")
            return HttpResponseRedirect(
                reverse_lazy(
                    "asociado:historicoCredito", args=[self.kwargs["pkAsociado"]]
                )
            )
        else:
            # Si el formulario no es válido, muestra errores
            messages.error(self.request, "Error al modificar el codeudor.")
            return self.render_to_response(self.get_context_data(form=form), status=400)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form), status=400)
