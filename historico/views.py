import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.views.generic import ListView, DeleteView, TemplateView, DetailView, View
from usuarios.models import UsuarioAsociado
from django.contrib import messages
from django.db.models import Sum, F, Q, Subquery, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from django.db import transaction
from django.core.paginator import Paginator
from django.utils.timezone import timedelta

from .models import HistoricoAuxilio, HistorialPagos, HistoricoCredito
from parametro.models import MesTarifa, FormaPago, Tarifas, TipoAsociado
from asociado.models import Asociado, ParametroAsociado, TarifaAsociado, ConvenioHistoricoGasolina
from .form import CargarArchivoForm
from ventas.models import HistoricoVenta
from funciones.function import procesar_csv

# Create your views here.


class InformacionHistorico(ListView):
    def get(self, request, *args, **kwargs):
        template_name = "proceso/informacion.html"
        return render(request, template_name)


class VerHistoricoAuxilio(ListView):
    def get(self, request, *args, **kwargs):
        template_name = "base/asociado/listarAsociado.html"
        query = HistoricoAuxilio.objects.all()
        return render(request, template_name, {"query": query})


class VerHistoricoPagos(ListView):
    def get(self, request, *args, **kwargs):
        template_name = "proceso/pago/listarPagos.html"

        # Capturar el valor de búsqueda del formulario
        busqueda = request.GET.get("numDocumento")
        mensaje = None  # Variable para el mensaje

        if busqueda:
            try:
                # se valida si es un numero
                valorBuscado = int(busqueda.replace(".", ""))
                query = HistorialPagos.objects.select_related(
                    "asociado", "mesPago", "formaPago", "asociado__tAsociado"
                ).filter(asociado__numDocumento__icontains=valorBuscado)
            except ValueError:
                # si salta error, se busca por nombre o apellido
                query = HistorialPagos.objects.select_related(
                    "asociado", "mesPago", "formaPago", "asociado__tAsociado"
                ).filter(
                    Q(asociado__apellido__icontains=busqueda)
                    | Q(asociado__nombre__icontains=busqueda)
                )
        else:
            # Consulta para obtener los registros
            query = HistorialPagos.objects.select_related(
                "asociado", "mesPago", "formaPago", "asociado__tAsociado"
            ).all()

        # Verificar si no hay resultados
        if not query.exists():
            mensaje = "No se encontraron resultados para la búsqueda."

        # Configurar el paginador
        paginator = Paginator(query, 10)  # Muestra 10 registros por página
        page_number = request.GET.get("page")  # Obtén el número de página de la URL
        page_obj = paginator.get_page(page_number)  # Obtén la página actual

        return render(
            request, template_name, {"page_obj": page_obj, "mensaje": mensaje}
        )


class VerAsociadoPagos(ListView):
    def get(self, request, *args, **kwargs):
        template_name = "proceso/pago/realizarPago.html"
        query = TarifaAsociado.objects.values(
            "id",
            "asociado__nombre",
            "asociado__id",
            "asociado__apellido",
            "asociado__numDocumento",
            "total",
            "asociado__tAsociado__concepto",
        )
        return render(request, template_name, {"query": query})


class ModalPago(ListView):
    def get(self, request, *args, **kwargs):
        template_name = "proceso/pago/modalPago.html"
        queryValor = TarifaAsociado.objects.get(asociado=kwargs["pkAsociado"])
        queryParamAsoc = ParametroAsociado.objects.get(asociado=kwargs["pkAsociado"])
        queryHistorial = HistorialPagos.objects.filter(
            asociado=kwargs["pkAsociado"]
        ).exists()

        # Obtener la suma de los adicionales del asociado, se suma todo menos el aporte y el bSocial
        queryTarifa = TarifaAsociado.objects.filter(
            asociado=kwargs["pkAsociado"]
        ).aggregate(
            total_tarifa_asociado=Sum(
                Coalesce(F("cuotaMascota"), Value(0)) +
                Coalesce(F("cuotaRepatriacionBeneficiarios"), Value(0)) +
                Coalesce(F("cuotaRepatriacionTitular"), Value(0)) +
                Coalesce(F("cuotaSeguroVida"), Value(0)) +
                Coalesce(F("cuotaAdicionales"), Value(0)) +
                Coalesce(F("cuotaCoohopAporte"), Value(0)) +
                Coalesce(F("cuotaCoohopBsocial"), Value(0)) +
                Coalesce(F("cuotaConvenio"), Value(0))
            )
        )

        total_tarifa_asociado = (
            queryTarifa["total_tarifa_asociado"] or 0
        )

        if queryHistorial:
            mesesPagados = HistorialPagos.objects.filter(
                asociado=kwargs["pkAsociado"], mesPago_id__lt=9990
            ).values("mesPago")
            queryMes = (
                MesTarifa.objects.exclude(pk__in=Subquery(mesesPagados))
                .exclude(pk__range=(9992, 9993))
                .filter(pk__gte=queryParamAsoc.primerMes.pk)
                .annotate(
                    total=Case(
                        When(
                            pk__gte=9990, then=Value(0)
                        ),  # Se envia valor en 0 para mostrar en el template
                        default=F("aporte")
                        + F("bSocial")
                        + total_tarifa_asociado,  # se suma al resto de pk el valor de aporte, bsocial y total tarifa
                        output_field=IntegerField(),
                    )
                )
            )
        else:
            queryMes = (
                MesTarifa.objects.filter(pk__gte=queryParamAsoc.primerMes.pk)
                .annotate(total=F("aporte") + F("bSocial") + total_tarifa_asociado)
                .exclude(pk=9993)
            )

        queryPago = FormaPago.objects.all()

        queryHistorial = HistorialPagos.objects.filter(
            asociado=kwargs["pkAsociado"]
        ).aggregate(total=Sum("diferencia"))
        total_diferencia = (
            queryHistorial["total"] or 0
        )  # Se obtiene el valor de la suma a 0 si no hay datos

        # Se valida si el asociado cuenta con credito de productos home elements
        queryValidacion = HistoricoVenta.objects.filter(
            asociado=kwargs["pkAsociado"],
            estadoRegistro=True,
            formaPago__in=["CREDITO", "DESCUENTO NOMINA"],
        ).exists()
        queryCreditoProd = None
        if queryValidacion:
            queryCreditoProd = HistoricoVenta.objects.filter(
                asociado=kwargs["pkAsociado"],
                formaPago__in=["CREDITO", "DESCUENTO NOMINA"],
                estadoRegistro=True,
                pendientePago__gt=0,
            )

            for homeElements in queryCreditoProd:
                # if homeElements.valorNeto % homeElements.pendientePago != 0:
                #     if homeElements.cuotas - homeElements.cuotasPagas == 1:
                #         homeElements.valorCuotas = homeElements.pendientePago
                # elif homeElements.cuotas == homeElements.cuotasPagas:
                #     homeElements.valorCuotas = homeElements.pendientePago
                if (homeElements.cuotas - homeElements.cuotasPagas) == 1:
                    homeElements.valorCuotas = homeElements.pendientePago
                else:
                    if (homeElements.cuotas - homeElements.cuotasPagas) <= 0 and homeElements.pendientePago > 0:
                        homeElements.valorCuotas = homeElements.pendientePago
                    elif homeElements.pendientePago == 0:
                        homeElements.valorCuotas = 0
                    else:
                        # Se deja el valor cuota como esta en la db
                        pass

        # Se valida si el asociado cuenta con credito
        queryValidacionCredito = HistoricoCredito.objects.filter(
            asociado=kwargs["pkAsociado"], estadoRegistro=True, pendientePago__gt=0
        ).exists()
        queryCredito = None
        if queryValidacionCredito:
            queryCredito = HistoricoCredito.objects.filter(
                asociado=kwargs["pkAsociado"], estadoRegistro=True, pendientePago__gt=0
            )
            for credito in queryCredito:
                # if credito.totalCredito % credito.pendientePago != 0:
                #     if credito.cuotas - credito.cuotasPagas == 1:
                #         credito.valorCuota = credito.pendientePago
                if (credito.cuotas - credito.cuotasPagas) == 1:
                    credito.valorCuota = credito.pendientePago
                else:
                    if (credito.cuotas - credito.cuotasPagas) <= 0 and credito.pendientePago > 0:
                        credito.valorCuota = credito.pendientePago
                    elif credito.pendientePago == 0:
                        credito.valorCuota = 0
                    else:
                        # Se deja el valor cuota como esta en la db
                        pass
        # Se valida si el asociado debe cuotas de la vinculación
        cuotaVinculacion = None
        cuotaVinculacionMenorEdad = Tarifas.objects.values("valor").get(pk=8)
        if (
            queryParamAsoc.vinculacionFormaPago
            and queryParamAsoc.vinculacionFormaPago.pk == 2
            and queryParamAsoc.vinculacionPendientePago > 0
        ):
            queryPagosVinculacion = HistorialPagos.objects.filter(
                asociado=kwargs["pkAsociado"],
                mesPago=9995,  # Id de la vinculación Adulto
                estadoRegistro=True,
            ).count()

            if queryPagosVinculacion == (queryParamAsoc.vinculacionCuotas - 1):
                cuotaVinculacion = queryParamAsoc.vinculacionPendientePago
            else:
                cuotaVinculacion = queryParamAsoc.vinculacionValor

        query_gasolina = ConvenioHistoricoGasolina.objects.select_related("convenio", "mes_tarifa").filter(asociado=kwargs["pkAsociado"], estado_registro=True, pendiente_pago__gt=0).first()

        context = {
            "pkAsociado": kwargs["pkAsociado"],
            "vista": kwargs["vista"],
            "query": queryValor,
            "queryMes": queryMes,
            "queryPago": queryPago,
            "diferencia": total_diferencia,
            "queryCreditoProd": queryCreditoProd,
            "queryCredito": queryCredito,
            "cuotaVinculacion": cuotaVinculacion,
            "cuotaVinculacionMenorEdad": cuotaVinculacionMenorEdad,
            "query_gasolina": query_gasolina,
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        fechaPago = request.POST["fechaPago"]
        formaPago = request.POST["formaPago"]
        valorPago = int(request.POST["valorPago"])
        tarifaAsociado = TarifaAsociado.objects.get(asociado=kwargs["pkAsociado"])
        diferencia = request.POST["diferencia"]
        valorDiferencia = int(diferencia.replace(".", ""))

        # creamos un array para guardar los pagos que se marcaron como activos
        datos_pagos = []

        # obtenemos los switchs que se marcaron como activos en el modal
        switches_activos = request.POST.getlist("switches") or []

        # saber el tamaño de los botones marcados
        cantidadSwitches = len(switches_activos)

        usuario = request.user

        # Se recorre los switch activos, con el pk del mes activo
        for contador, pk in enumerate(switches_activos, start=1):
            split = pk.split("-")

            if len(split) == 1:
                # Aplica para abonos, se crea un registro de pago con el valor de abono
                if pk == "9999":
                    pago = {
                        "asociado": Asociado.objects.get(pk=kwargs["pkAsociado"]),
                        "mesPago": MesTarifa.objects.get(pk=pk),
                        "fechaPago": fechaPago,
                        "formaPago": FormaPago.objects.get(pk=formaPago),
                        "aportePago": MesTarifa.objects.get(pk=pk).aporte,
                        "bSocialPago": MesTarifa.objects.get(pk=pk).bSocial,
                        "mascotaPago": 0,
                        "repatriacionPago": 0,
                        "seguroVidaPago": 0,
                        "adicionalesPago": 0,
                        "coohopAporte": 0,
                        "coohopBsocial": 0,
                        "convenioPago": 0,
                        "creditoHomeElements": 0,
                        "diferencia": valorDiferencia
                        if cantidadSwitches == contador
                        else 0,
                        "valorPago": valorDiferencia
                        if cantidadSwitches == contador
                        else 0,
                        "estadoRegistro": True,
                        "userCreacion": usuario,
                    }
                    datos_pagos.append(pago)

                # Aplica para pagos de boletas de cine y certificado, pk 9997, 9996, 9991
                elif pk in ["9997", "9996", "9991"]:
                    if pk == "9997":
                        valorPago = (
                            request.POST["valorCine"]
                            if contador < cantidadSwitches
                            else int(request.POST["valorCine"]) + valorDiferencia
                        )
                    elif pk == "9996":
                        valorPago = (
                            request.POST["valorCertificado"]
                            if contador < cantidadSwitches
                            else int(request.POST["valorCertificado"]) + valorDiferencia
                        )
                    elif pk == "9991":
                        valorPago = (
                            request.POST["valorViaje"]
                            if contador < cantidadSwitches
                            else int(request.POST["valorViaje"]) + valorDiferencia
                        )

                    pago = {
                        "asociado": Asociado.objects.get(pk=kwargs["pkAsociado"]),
                        "mesPago": MesTarifa.objects.get(pk=pk),
                        "fechaPago": fechaPago,
                        "formaPago": FormaPago.objects.get(pk=formaPago),
                        "aportePago": 0,
                        "bSocialPago": 0,
                        "mascotaPago": 0,
                        "repatriacionPago": 0,
                        "seguroVidaPago": 0,
                        "adicionalesPago": 0,
                        "coohopAporte": 0,
                        "coohopBsocial": 0,
                        "convenioPago": 0,
                        "creditoHomeElements": 0,
                        "diferencia": valorDiferencia
                        if cantidadSwitches == contador
                        else 0,
                        "valorPago": valorPago,
                        "estadoRegistro": True,
                        "userCreacion": usuario,
                    }
                    datos_pagos.append(pago)

                # Aplica para pagos de mes normal, se crea un registro de pago con el valor del mes
                else:
                    tarifa = MesTarifa.objects.get(pk=pk)
                    valorMes = (
                        (tarifa.aporte or 0)
                        + (tarifa.bSocial or 0)
                        + (tarifaAsociado.cuotaMascota or 0)
                        + (tarifaAsociado.cuotaRepatriacionBeneficiarios or 0)
                        + (tarifaAsociado.cuotaRepatriacionTitular or 0)
                        + (tarifaAsociado.cuotaSeguroVida or 0)
                        + (tarifaAsociado.cuotaAdicionales or 0)
                        + (tarifaAsociado.cuotaCoohopAporte or 0)
                        + (tarifaAsociado.cuotaCoohopBsocial or 0)
                        + (tarifaAsociado.cuotaConvenio or 0)
                    )
                    valorPago = (
                        valorMes
                        if contador < cantidadSwitches
                        else valorMes + valorDiferencia
                    )

                    pago = {
                        "asociado": Asociado.objects.get(pk=kwargs["pkAsociado"]),
                        "mesPago": tarifa,
                        "fechaPago": fechaPago,
                        "formaPago": FormaPago.objects.get(pk=formaPago),
                        "aportePago": tarifa.aporte,
                        "bSocialPago": tarifa.bSocial,
                        "mascotaPago": tarifaAsociado.cuotaMascota,
                        "repatriacionPago": (tarifaAsociado.cuotaRepatriacionBeneficiarios or 0) + (tarifaAsociado.cuotaRepatriacionTitular or 0),
                        "seguroVidaPago": tarifaAsociado.cuotaSeguroVida,
                        "adicionalesPago": tarifaAsociado.cuotaAdicionales,
                        "coohopAporte": tarifaAsociado.cuotaCoohopAporte,
                        "coohopBsocial": tarifaAsociado.cuotaCoohopBsocial,
                        "convenioPago": tarifaAsociado.cuotaConvenio,
                        "creditoHomeElements": 0,
                        "diferencia": valorDiferencia
                        if cantidadSwitches == contador
                        else 0,
                        "valorPago": valorPago,
                        "estadoRegistro": True,
                        "userCreacion": usuario,
                    }
                    datos_pagos.append(pago)

            # Aplica para Pagos de vinculacion de adulto y menores edad, pk 9994, 9995
            elif len(split) == 2:
                pk = split[0]  # pk del mes (9994-9995)
                cuotaVinculacion = int(split[1])  # valor pagado

                valorPago = (
                    cuotaVinculacion + valorDiferencia
                    if cantidadSwitches == contador
                    else cuotaVinculacion
                )

                pago = {
                    "asociado": Asociado.objects.get(pk=kwargs["pkAsociado"]),
                    "mesPago": MesTarifa.objects.get(pk=pk),
                    "fechaPago": fechaPago,
                    "formaPago": FormaPago.objects.get(pk=formaPago),
                    "aportePago": 0,
                    "bSocialPago": 0,
                    "mascotaPago": 0,
                    "repatriacionPago": 0,
                    "seguroVidaPago": 0,
                    "adicionalesPago": 0,
                    "coohopAporte": 0,
                    "coohopBsocial": 0,
                    "convenioPago": 0,
                    "creditoHomeElements": 0,
                    "diferencia": valorDiferencia
                    if cantidadSwitches == contador
                    else 0,
                    "valorPago": valorPago,
                    "estadoRegistro": True,
                    "userCreacion": usuario,
                }
                datos_pagos.append(pago)

                if pk == "9995":
                    # Si es vinculacion de adulto, actualizamos el pendiente de pago
                    ParametroAsociado.objects.filter(
                        asociado=kwargs["pkAsociado"]
                    ).update(
                        vinculacionPendientePago=F("vinculacionPendientePago")
                        - valorPago
                    )

            # Aplica para Creditos Home Elements
            # desde el modalPago se envia, pkVenta, 9998, valorCuota
            else:
                extra_param = split[0]  # pk de la venta
                pk = split[1]  # identificador del tipo de pago, credito home elements
                valorCuota = int(split[2].replace(".", ""))  # valor de la cuota

                # Creditos Home Elements
                if pk == "9998":
                    queryCreditoProd = HistoricoVenta.objects.get(pk=extra_param)
                    pago = {
                        "asociado": Asociado.objects.get(pk=kwargs["pkAsociado"]),
                        "mesPago": MesTarifa.objects.get(pk=pk),
                        "fechaPago": fechaPago,
                        "formaPago": FormaPago.objects.get(pk=formaPago),
                        "aportePago": 0,
                        "bSocialPago": 0,
                        "mascotaPago": 0,
                        "repatriacionPago": 0,
                        "seguroVidaPago": 0,
                        "adicionalesPago": 0,
                        "coohopAporte": 0,
                        "coohopBsocial": 0,
                        "convenioPago": 0,
                        "creditoHomeElements": queryCreditoProd.valorCuotas,
                        "diferencia": valorCuota
                        - queryCreditoProd.valorCuotas
                        + valorDiferencia
                        if cantidadSwitches == contador
                        else 0,
                        "valorPago": queryCreditoProd.valorCuotas
                        if contador < cantidadSwitches
                        else valorCuota + valorDiferencia,
                        "ventaHE": queryCreditoProd,
                        "estadoRegistro": True,
                        "userCreacion": usuario,
                    }
                    datos_pagos.append(pago)
                    if contador < cantidadSwitches:
                        queryCreditoProd.valorCuotas
                    elif queryCreditoProd.valorCuotas:
                        queryCreditoProd.valorCuotas + valorDiferencia
                    queryCreditoProd.pendientePago = (
                        queryCreditoProd.pendientePago - pago["valorPago"]
                    )
                    queryCreditoProd.cuotasPagas = queryCreditoProd.cuotasPagas + 1

                    queryCreditoProd.save()

                # Pk 9993 credito
                elif pk == "9993":
                    queryCredito = HistoricoCredito.objects.get(pk=extra_param)
                    valorPago = (
                        queryCredito.valorCuota
                        if contador < cantidadSwitches
                        else valorCuota + valorDiferencia
                    )
                    pago = {
                        "asociado": Asociado.objects.get(pk=kwargs["pkAsociado"]),
                        "mesPago": MesTarifa.objects.get(pk=pk),
                        "fechaPago": fechaPago,
                        "formaPago": FormaPago.objects.get(pk=formaPago),
                        "aportePago": 0,
                        "bSocialPago": 0,
                        "mascotaPago": 0,
                        "repatriacionPago": 0,
                        "seguroVidaPago": 0,
                        "adicionalesPago": 0,
                        "coohopAporte": 0,
                        "coohopBsocial": 0,
                        "convenioPago": 0,
                        "creditoHomeElements": 0,
                        "credito": queryCredito.valorCuota,
                        "diferencia": valorCuota
                        - queryCredito.valorCuota
                        + valorDiferencia
                        if cantidadSwitches == contador
                        else 0,
                        "creditoId": queryCredito,
                        "valorPago": valorPago,
                        "estadoRegistro": True,
                        "userCreacion": usuario,
                    }
                    datos_pagos.append(pago)
                    queryCredito.pendientePago = queryCredito.pendientePago - valorPago
                    queryCredito.cuotasPagas = queryCredito.cuotasPagas + 1
                    queryCredito.save()
                
                elif pk == "9990":
                    query = ConvenioHistoricoGasolina.objects.get(pk=extra_param)
                    valorPago = (
                        query.pendiente_pago
                        if contador < cantidadSwitches
                        else valorCuota + valorDiferencia
                    )
                    diferencia = (
                        valorPago if query.valor_pagar != query.pendiente_pago else valorCuota - query.pendiente_pago + valorDiferencia
                    )
                    pago = {
                        "asociado": Asociado.objects.get(pk=kwargs["pkAsociado"]),
                        "mesPago": MesTarifa.objects.get(pk=pk),
                        "fechaPago": fechaPago,
                        "formaPago": FormaPago.objects.get(pk=formaPago),
                        "aportePago": 0,
                        "bSocialPago": 0,
                        "mascotaPago": 0,
                        "repatriacionPago": 0,
                        "seguroVidaPago": 0,
                        "adicionalesPago": 0,
                        "coohopAporte": 0,
                        "coohopBsocial": 0,
                        "convenioPago": 0,
                        "creditoHomeElements": 0,
                        "diferencia": diferencia,
                        "valorPago": valorPago,
                        "convenio_gasolina_id": query,
                        "estadoRegistro": True,
                        "userCreacion": usuario,
                    }
                    datos_pagos.append(pago)
                    query.pendiente_pago -= valorPago
                    query.save()

        # Crear cada registro en un bucle
        for data in datos_pagos:
            HistorialPagos.objects.create(**data)

        messages.info(request, "Pago Registrado Correctamente")
        url = reverse("proceso:asociadoPago")

        # Ajusta la URL según el valor de vista
        if kwargs["vista"] == 1:
            url = reverse("asociado:historialPagos", args=[kwargs["pkAsociado"]])

        return HttpResponseRedirect(url)


@require_http_methods(["POST", "GET"])
def modal_pago_ventas(request, pkVenta, pkAsociado, tipo):
    if request.method == "POST":
        fechaPago = request.POST["fechaPago"]
        formaPago = request.POST["formaPago"]
        valorPago = int(request.POST["valorPago"])
        diferencia = request.POST["diferencia"]
        valorDiferencia = int(diferencia.replace(".",""))
        
        # creamos un array para guardar los pagos que se marcaron como activos
        datos_pagos = []

        # obtenemos los switchs que se marcaron como activos en el modal
        switches_activos = request.POST.getlist("switches") or []

        usuario = request.user

        # Se recorre los switch activos, con el pk del mes activo
        for contador, pk in enumerate(switches_activos, start=1):
            if tipo == "HOME-ELEMENT":
                query_credito_venta = HistoricoVenta.objects.get(pk = pkVenta)

                pago = {
                        "asociado": Asociado.objects.get(pk=pkAsociado),
                        "mesPago": MesTarifa.objects.get(pk=9998),
                        "fechaPago": fechaPago,
                        "formaPago": FormaPago.objects.get(pk=formaPago),
                        "aportePago": 0,
                        "bSocialPago": 0,
                        "mascotaPago": 0,
                        "repatriacionPago": 0,
                        "seguroVidaPago": 0,
                        "adicionalesPago": 0,
                        "coohopAporte": 0,
                        "coohopBsocial": 0,
                        "convenioPago": 0,
                        "creditoHomeElements": query_credito_venta.valorCuotas,
                        "diferencia": valorDiferencia,
                        "valorPago": valorPago,
                        "ventaHE": query_credito_venta,
                        "estadoRegistro": True,
                        "userCreacion": usuario,
                }
                datos_pagos.append(pago)
                query_credito_venta.pendientePago = query_credito_venta.pendientePago - valorPago
                query_credito_venta.cuotasPagas = query_credito_venta.cuotasPagas + 1
                query_credito_venta.save()

                url = reverse("asociado:listarVentasAsociado", args=[pkAsociado])

            elif tipo == "CREDITO":
                query_credito = HistoricoCredito.objects.get(pk = pkVenta)

                pago = {
                        "asociado": Asociado.objects.get(pk=pkAsociado),
                        "mesPago": MesTarifa.objects.get(pk=9993),
                        "fechaPago": fechaPago,
                        "formaPago": FormaPago.objects.get(pk=formaPago),
                        "aportePago": 0,
                        "bSocialPago": 0,
                        "mascotaPago": 0,
                        "repatriacionPago": 0,
                        "seguroVidaPago": 0,
                        "adicionalesPago": 0,
                        "coohopAporte": 0,
                        "coohopBsocial": 0,
                        "convenioPago": 0,
                        "credito": query_credito.valorCuota,
                        "creditoHomeElements": 0,
                        "diferencia": valorDiferencia,
                        "valorPago": valorPago,
                        "creditoId": query_credito,
                        "estadoRegistro": True,
                        "userCreacion": usuario,
                }
                datos_pagos.append(pago)
                query_credito.pendientePago = query_credito.pendientePago - valorPago
                query_credito.cuotasPagas = query_credito.cuotasPagas + 1
                query_credito.save()

                url = reverse("asociado:historicoCredito", args=[pkAsociado])
            elif tipo == "GASOLINA":
                query_gasolina = ConvenioHistoricoGasolina.objects.get(pk=pkVenta)
        
                diferencia = (
                    valorPago if query_gasolina.valor_pagar != query_gasolina.pendiente_pago else valorPago - query_gasolina.pendiente_pago
                )

                pago = {
                        "asociado": Asociado.objects.get(pk=pkAsociado),
                        "mesPago": MesTarifa.objects.get(pk=9990),
                        "fechaPago": fechaPago,
                        "formaPago": FormaPago.objects.get(pk=formaPago),
                        "aportePago": 0,
                        "bSocialPago": 0,
                        "mascotaPago": 0,
                        "repatriacionPago": 0,
                        "seguroVidaPago": 0,
                        "adicionalesPago": 0,
                        "coohopAporte": 0,
                        "coohopBsocial": 0,
                        "convenioPago": 0,
                        "diferencia": diferencia,
                        "valorPago": valorPago,
                        "convenio_gasolina_id": query_gasolina,
                        "estadoRegistro": True,
                        "userCreacion": usuario,
                }
                datos_pagos.append(pago)
                query_gasolina.pendiente_pago -= valorPago
                query_gasolina.save()

                url = reverse("asociado:tarifaAsociado", args=[pkAsociado])

        # Crear cada registro en un bucle
        for data in datos_pagos:
            HistorialPagos.objects.create(**data)

        messages.info(request, "Pago Registrado Correctamente")
        return HttpResponseRedirect(url)


    else:
        formaPago = FormaPago.objects.all()

        if tipo == "HOME-ELEMENT":
            query = HistoricoVenta.objects.get(pk = pkVenta)
            # Se valida si es la ultima cuota para enviar el pendiente por pagar
            if (query.cuotas - query.cuotasPagas) == 1:
                valorCuota = query.pendientePago
            else:
                if (query.cuotas - query.cuotasPagas) <= 0 and query.pendientePago > 0:
                    valorCuota = query.pendientePago
                elif query.pendientePago == 0:
                    valorCuota = 0
                else:
                    valorCuota = query.valorCuotas
            observacion = "HOME ELEMENTS"
        elif tipo == "CREDITO":
            query = HistoricoCredito.objects.get(pk = pkVenta)
            if (query.cuotas - query.cuotasPagas) == 1:
                valorCuota = query.pendientePago
            else:
                if (query.cuotas - query.cuotasPagas) <= 0 and query.pendientePago > 0:
                    valorCuota = query.pendientePago
                elif query.pendientePago == 0:
                    valorCuota = 0
                else:
                    valorCuota = query.valorCuota
            observacion = query.lineaCredito
        elif tipo == "GASOLINA":
            # pkVenta es el pk del convenio gasolina}
            
            query = ConvenioHistoricoGasolina.objects.select_related("convenio", "mes_tarifa").filter(convenio = pkVenta, estado_registro = True,  pendiente_pago__gt = 0).first()
            
            if query:
                valorCuota = query.pendiente_pago
                observacion = f"CHIP GASOLINA - {query.mes_tarifa.concepto}"
            else:
                valorCuota = 0
                observacion = f"SIN REGISTROS POR PAGAR"


        context = {
            "objeto": query,
            "pkAsociado": pkAsociado,
            "formaPago": formaPago,
            "valorCuota": valorCuota,
            "tipo": tipo,
            "observacion": observacion
        }

        return render(request, "proceso/pago/modalPagoVentas.html", context)


@csrf_exempt
def actualizar_pago(request, pk, tipo):
    if request.method == "POST":
        data = json.loads(request.body)
        valor_pago = int(data.get("valorPago"))
        fecha_pago = data.get("fechaPago")
        forma_pago = data.get("formaPago")
        obj_forma_pago = FormaPago.objects.get(pk = forma_pago)

        try:
            pago = HistorialPagos.objects.get(pk = pk)
            # Valor pago anterior
            pago_anterior = pago.valorPago
            # Valor pago nuevo
            pago.valorPago = valor_pago
            # Opcion Home elements
            if tipo == 1:
                pago.fechaPago = fecha_pago
                pago.formaPago = obj_forma_pago
                
                # Si es Anticipo no se deja diferencia
                if pago.mesPago.pk != 9988: 
                    pago.diferencia = valor_pago - pago.creditoHomeElements
                else:
                    pago.diferencia = 0
                pago.userModificacion = request.user
                pago.save()
                venta_he = HistoricoVenta.objects.get(pk = pago.ventaHE.id)
                venta_he.pendientePago = venta_he.pendientePago + pago_anterior - pago.valorPago
                venta_he.save()
                total_pagado = venta_he.valorNeto - venta_he.pendientePago
                return JsonResponse({
                    "status":"ok",
                    "diferencia":pago.diferencia,
                    "total_pagado": total_pagado
                    })
            # Opcion Credito
            elif tipo == 2:
                pago.fechaPago = fecha_pago
                pago.formaPago = obj_forma_pago
                pago.diferencia = valor_pago - pago.credito
                pago.userModificacion = request.user
                pago.save()
                credito = HistoricoCredito.objects.get(pk = pago.creditoId.id)
                credito.pendientePago = credito.pendientePago + pago_anterior - pago.valorPago
                credito.save()
                total_pagado = credito.totalCredito - credito.pendientePago
                return JsonResponse({
                    "status":"ok",
                    "diferencia":pago.diferencia,
                    "total_pagado": total_pagado
                    })
            
        except HistorialPagos.DoesNotExist:
            return JsonResponse({"error":"Pago no encontrado"}, status=404)
        
    return JsonResponse({"error":"Metodo no permitido"}, status=405)


@csrf_exempt
def eliminar_pago(request, pk, tipo):
    if request.method == "POST":
        pago = get_object_or_404(HistorialPagos, pk=pk)
        if tipo == 1:
            venta_he = get_object_or_404(HistoricoVenta, pk = pago.ventaHE.pk)
            # Si es diferente a Anticipo, se resta la cuota, de lo contrario no hace nada
            if pago.mesPago.pk != 9988:
                venta_he.cuotasPagas -= 1
            venta_he.pendientePago += pago.valorPago
            venta_he.save()
            pago.delete()
            total_pagado = venta_he.valorNeto - venta_he.pendientePago
            return JsonResponse({
                'status': 'ok',
                'total_pagado': total_pagado
                })
        elif tipo == 2:
            credito = get_object_or_404(HistoricoCredito, pk = pago.creditoId.pk)
            credito.cuotasPagas -= 1
            credito.pendientePago += pago.valorPago
            credito.save()
            pago.delete()
            total_pagado = credito.totalCredito - credito.pendientePago
            return JsonResponse({
                'status': 'ok',
                'total_pagado': total_pagado
                })
    else:
        return JsonResponse({'error':"Metodo no permitido"})

class EditarPago(ListView):
    def get(self, request, *args, **kwargs):
        template_name = "proceso/pago/editarPagoAsociado.html"
        queryPago = HistorialPagos.objects.select_related("mesPago", "formaPago").get(
            pk=kwargs["pk"]
        )
        mesesPagados = HistorialPagos.objects.filter(
            asociado=kwargs["pkAsociado"]
        ).values("mesPago")
        queryMes = MesTarifa.objects.exclude(Q(pk__in=Subquery(mesesPagados)) | Q(pk__in=[9991,9992,9993,9994,9995,9996,9997,9998,9999]))
        queryFormaPago = FormaPago.objects.all()
        return render(
            request,
            template_name,
            {
                "queryPago": queryPago,
                "queryFormaPago": queryFormaPago,
                "queryMes": queryMes,
                "pk": kwargs["pk"],
                "pkAsociado": kwargs["pkAsociado"],
                "vista": kwargs["vista"],
            },
        )

    def post(self, request, *args, **kwargs):
        mesPago = request.POST["mesPago"]

        objHistorico = HistorialPagos.objects.get(pk=kwargs["pk"])

        objHistorico.mesPago = MesTarifa.objects.get(pk=mesPago)
        objHistorico.formaPago = FormaPago.objects.get(pk=request.POST["formaPago"])
        objHistorico.fechaPago = request.POST["fechaPago"]
        objHistorico.valorPago = request.POST["valorPago"]
        objHistorico.aportePago = request.POST["aportePago"]
        objHistorico.bSocialPago = request.POST["bSocialPago"]
        objHistorico.diferencia = request.POST["diferencia"]
        if objHistorico.mascotaPago != 0:
            objHistorico.mascotaPago = request.POST["mascotaPago"]
        if objHistorico.repatriacionPago != 0:
            objHistorico.repatriacionPago = request.POST["repatriacionPago"]
        if objHistorico.seguroVidaPago != 0:
            objHistorico.seguroVidaPago = request.POST["seguroVidaPago"]
        if objHistorico.adicionalesPago != 0:
            objHistorico.adicionalesPago = request.POST["adicionalesPago"]
        if objHistorico.coohopAporte != 0:
            objHistorico.coohopAporte = request.POST["coohopAporte"]
        if objHistorico.coohopBsocial != 0:
            objHistorico.coohopBsocial = request.POST["coohopBsocial"]
        if objHistorico.convenioPago != 0:
            objHistorico.convenioPago = request.POST["convenioPago"]
        objHistorico.userModificacion = UsuarioAsociado.objects.get(pk=request.user.pk)
        objHistorico.save()
        messages.info(request, "Pago Modificado Correctamente")

        # Recupera el valor de num_documento del POST
        num_documento = request.POST.get("num_documento", "")
        # Inicializar la URL por defecto
        url = reverse("proceso:historicoPagos")

        # Ajusta la URL según el valor de vista
        if kwargs["vista"] == 1:
            url = reverse("asociado:historialPagos", args=[kwargs["pkAsociado"]])

        # Añadir el filtro de num_documento como parámetro en la URL
        if num_documento:
            url += f"?numDocumento={num_documento}"

        return HttpResponseRedirect(url)


class EliminarPago(DeleteView):
    def get(self, request, *args, **kwargs):
        template_name = "proceso/pago/eliminar.html"
        query = HistorialPagos.objects.get(pk=kwargs["pk"])
        context = {
            "query": query,
            "pk": kwargs["pk"],
            "pkAsociado": kwargs["pkAsociado"],
            "vista": kwargs["vista"],
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        obj = HistorialPagos.objects.get(pk=kwargs["pk"])

        # si es credito home elements, se elimina el registro y se actualiza el valor de credito
        if obj.mesPago.pk == 9998:
            credito = HistoricoVenta.objects.get(
                asociado=kwargs["pkAsociado"],
                valorCuotas=obj.creditoHomeElements,
                estadoRegistro=True,
            )
            credito.pendientePago = credito.pendientePago + obj.valorPago
            credito.cuotasPagas = credito.cuotasPagas - 1
            credito.save()

        # Si es credito, se elimina registro y se actualiza valor de credito
        if obj.mesPago.pk == 9993:
            credito = HistoricoCredito.objects.get(
                id = obj.creditoId.id
            )
            credito.cuotasPagas = credito.cuotasPagas - 1
            credito.pendientePago += obj.valorPago
            credito.save()

        if obj.mesPago.pk == 9990:
            convenio = ConvenioHistoricoGasolina.objects.get(
                id = obj.convenio_gasolina_id.id
            )
            convenio.pendiente_pago += obj.valorPago
            convenio.save()

        # Si es anticipo, se elimina registro y se actualiza valor de credito productos
        if obj.mesPago.pk == 9988:
            venta = HistoricoVenta.objects.get(
                id = obj.ventaHE_id
            )
            venta.pendientePago += obj.valorPago
            venta.save()

        obj.delete()
        messages.info(request, "Pago Eliminado Correctamente")

        # Recupera el valor de num_documento del POST
        num_documento = request.POST.get("num_documento", "")
        # Inicializar la URL por defecto
        url = reverse("proceso:historicoPagos")

        # Ajusta la URL según el valor de vista
        if kwargs["vista"] == 1:
            url = reverse("asociado:historialPagos", args=[kwargs["pkAsociado"]])

        # Añadir el filtro de num_documento como parámetro en la URL
        if num_documento:
            url += f"?numDocumento={num_documento}"

        return HttpResponseRedirect(url)


class cargarCSV(ListView):
    def get(self, request, *args, **kwargs):
        template_name = "proceso/cargarCSV.html"
        form = CargarArchivoForm()
        return render(request, template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        archivo_csv = request.FILES.get("archivo_csv")
        if archivo_csv:
            try:
                user_creacion_id = request.user.pk
                registros = procesar_csv(archivo_csv, user_creacion_id)
                HistorialPagos.objects.bulk_create(registros)
                messages.success(
                    request,
                    f"✓ Datos insertados correctamente: Se han registrado {len(registros)} registro(s).",
                )
            except ValueError as e:
                # Los errores acumulados vendrán aquí con saltos de línea
                mensaje_html = str(e).replace('\n', '<br>')
                messages.error(request, mark_safe(mensaje_html))
            except Exception as e:
                messages.error(request, f"Error inesperado: {str(e)}")
        else:
            messages.warning(request, "No se ha seleccionado ningún archivo CSV.")

        return redirect("proceso:cargarCSV")

class ActualizarEstadoAsoc(TemplateView):
    template_name = "proceso/actualizarEstadoAsoc.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["TipoAsociado"] = TipoAsociado.objects.all()
        context["mes"] = MesTarifa.objects.filter(pk__lte=9990)
        return context

    def post(self, request, *args, **kwargs):
        tipoAsociado = request.POST["tipoAsociado"]
        mes = int(request.POST["mes"])

        resultado = []

        if tipoAsociado == "0":
            asociados = Asociado.objects.filter(~Q(estadoAsociado="RETIRO")).values(
                "id", "nombre", "apellido", "numDocumento", "estadoAsociado"
            )
        else:
            asociados = Asociado.objects.filter(
                ~Q(estadoAsociado="RETIRO"), tAsociado=tipoAsociado
            ).values("id", "nombre", "apellido", "numDocumento", "estadoAsociado")

        for asociado in asociados:
            # query de primer mes del asociado
            primerMes = (
                ParametroAsociado.objects.filter(asociado=asociado["id"])
                .values_list("primerMes", flat=True)
                .first()
            )
            print(asociado, primerMes)

            if primerMes is None:
                resultado.append({
                    "id": asociado["id"],
                    "numero_documento": asociado["numDocumento"],
                    "nombre_completo": f"{asociado['nombre']} {asociado['apellido']}",
                    "estado_actual": asociado["estadoAsociado"],
                    "estado_calculado": "INACTIVO",
                    "observaciones": "No tiene registrado el primer mes en ParametroAsociado",
                })
                continue

            if primerMes <= mes:
                # numero de pagos del asociado del mes seleccionado hacia atras
                pagosRealizados = HistorialPagos.objects.filter(
                    asociado=asociado["id"], mesPago__lte=mes
                ).count()
                pagosEsperados = mes - (primerMes - 1)
                # tiene el mismo numero de pagos que el mes seleccionado
                if pagosEsperados == pagosRealizados:
                    diferencia = (
                        HistorialPagos.objects.filter(
                            asociado=asociado["id"], mesPago__lte=mes
                        ).aggregate(totalDiferencia=Sum("diferencia"))[
                            "totalDiferencia"
                        ]
                        or 0
                    )
                    # Activo
                    if diferencia >= 0:
                        resultado.append(
                            {
                                "id": asociado["id"],
                                "numero_documento": asociado["numDocumento"],
                                "nombre_completo": asociado["nombre"]
                                + " "
                                + asociado["apellido"],
                                "estado_actual": asociado["estadoAsociado"],
                                "estado_calculado": "ACTIVO",
                                "observaciones": "",
                            }
                        )
                    # Inactivo, diferencia negativa
                    else:
                        resultado.append(
                            {
                                "id": asociado["id"],
                                "numero_documento": asociado["numDocumento"],
                                "nombre_completo": asociado["nombre"]
                                + " "
                                + asociado["apellido"],
                                "estado_actual": asociado["estadoAsociado"],
                                "estado_calculado": "INACTIVO",
                                "observaciones": f"Inactivo, diferencia negativa {diferencia}",
                            }
                        )
                else:
                    # listado de meses los cuales el asociado debe tener pagado
                    listaMeses = MesTarifa.objects.filter(
                        id__gte=primerMes, id__lte=mes
                    ).values_list("id", "concepto")
                    mesesPagados = HistorialPagos.objects.filter(
                        asociado_id=asociado["id"],
                        mesPago__id__gte=primerMes,
                        mesPago__id__lte=mes,
                    ).values_list("mesPago__id", flat=True)
                    mesesFaltantes = [
                        mes for mes in listaMeses if mes[0] not in mesesPagados
                    ]
                    soloMeses = [mes[1] for mes in mesesFaltantes]
                    resultado.append(
                        {
                            "id": asociado["id"],
                            "numero_documento": asociado["numDocumento"],
                            "nombre_completo": asociado["nombre"]
                            + " "
                            + asociado["apellido"],
                            "estado_actual": asociado["estadoAsociado"],
                            "estado_calculado": "INACTIVO",
                            "observaciones": f"Meses faltantes: {soloMeses}",
                        }
                    )
            # El asociado se vinculo despues del mes seleccionado, activo
            else:
                resultado.append(
                    {
                        "id": asociado["id"],
                        "numero_documento": asociado["numDocumento"],
                        "nombre_completo": asociado["nombre"]
                        + " "
                        + asociado["apellido"],
                        "estado_actual": asociado["estadoAsociado"],
                        "estado_calculado": "ACTIVO",
                        "observaciones": "",
                    }
                )
        return JsonResponse({"resultados": resultado})


def actualizarEstadoMasivo(request):
    if request.method == "POST":
        data = json.loads(request.body)  # Convertir la peticion Json a un diccionario
        asociados = data.get("asociados", [])  # Obtenemos los datos enviados

        if not asociados:
            return JsonResponse(
                {"success": False, "error": "No se enviaron datos"}, status=400
            )

        with transaction.atomic():  #  se usa una transacción para mayor eficiencia
            registroActualizar = []
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

        pagos_relacionados = (
            HistorialPagos.objects.filter(
                asociado=asociado,
                fechaCreacion__range=(rango_inicio, rango_fin),
                fechaPago=pago_principal.fechaPago,
            )
            .order_by("fechaCreacion")
            .annotate(
                total_aporte_bsocial=Sum(F("aportePago") + F("bSocialPago")),
                total_coohop=Sum(F("coohopAporte") + F("coohopBsocial")),
            )
        )

        pago_total = pagos_relacionados.aggregate(total=Sum("valorPago"))["total"] or 0

        context["pagos_relacionados"] = pagos_relacionados
        context["pago_total"] = pago_total

        return context
