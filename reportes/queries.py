from django.db.models.functions import TruncSecond, Coalesce
from django.db.models import (
    OuterRef,
    Subquery,
    Count,
    IntegerField,
    Value,
    Case,
    When,
    F,
    Q,
    Sum,
    Exists
)

from beneficiario.models import Asociado, Mascota, Beneficiario, Coohoperativitos
from historico.models import HistorialPagos, HistoricoCredito, HistoricoSeguroVida
from ventas.models import HistoricoVenta
from asociado.models import (
    Asociado,
    ParametroAsociado,
    RepatriacionTitular,
    ConvenioHistoricoGasolina,
    ConveniosAsociado,
    TarifaAsociado,
)
from parametro.models import Tarifas, MesTarifa
from beneficiario.models import Beneficiario, Mascota
from historico.models import HistoricoCredito, HistorialPagos
from ventas.models import HistoricoVenta


def obtenerNovedades(fecha_inicial, fecha_final):
    asociadoRetiro = Asociado.objects.filter(
        fechaRetiro__range=[fecha_inicial, fecha_final]
    )

    asociadoIngreso = Asociado.objects.filter(
        fechaIngreso__range=[fecha_inicial, fecha_final]
    )

    queryMascota = (
        Mascota.objects.filter(fechaModificacion__range=[fecha_inicial, fecha_final])
        .annotate(
            fechaModificacion_truncada=TruncSecond("fechaModificacion"),
            fechaCreacion_truncada=TruncSecond("fechaCreacion"),
        )
        .select_related("asociado")
    )

    queryBeneficiario = (
        Beneficiario.objects.filter(
            fechaModificacion__range=[fecha_inicial, fecha_final]
        )
        .annotate(
            fechaModificacion_truncada=TruncSecond("fechaModificacion"),
            fechaCreacion_truncada=TruncSecond("fechaCreacion"),
        )
        .select_related("asociado", "paisRepatriacion", "parentesco")
    )

    queryRepatriacionTitular = RepatriacionTitular.objects.filter(
        fechaRepatriacion__range=[fecha_inicial, fecha_final]
    ).select_related("asociado", "paisRepatriacion")

    return {
        "asociadoRetiro": asociadoRetiro,
        "asociadoIngreso": asociadoIngreso,
        "queryMascota": queryMascota,
        "queryBeneficiario": queryBeneficiario,
        "queryRepatriacionTitular": queryRepatriacionTitular,
    }


def obtenerDescuentoNomina(empresa_pk, mes_seleccionado):
    # Pagos de vinculación (ya existente)
    pagos_vinculacion = (
        HistorialPagos.objects.filter(
            asociado=OuterRef("asociado"), mesPago=9995, estadoRegistro=True
        )
        .values("asociado")
        .annotate(total_pagos=Count("id"))
        .values("total_pagos")
    )

    # Pagos de crédito realizados
    pagos_credito = (
        HistorialPagos.objects.filter(
            asociado=OuterRef("asociado"),
            credito__gt=0,  # Solo pagos que tienen valor en el campo credito
            estadoRegistro=True,
        )
        .values("asociado")
        .annotate(total_pagos_credito=Count("id"))
        .values("total_pagos_credito")
    )

    # Pagos de home elements realizados
    pagos_home_elements = (
        HistorialPagos.objects.filter(
            asociado=OuterRef("asociado"),
            creditoHomeElements__gt=0,  # Solo pagos que tienen valor en creditoHomeElements
            estadoRegistro=True,
        )
        .values("asociado")
        .annotate(total_pagos_home=Count("id"))
        .values("total_pagos_home")
    )

    # Información de créditos pendientes
    credito_info = (
        HistoricoCredito.objects.filter(
            asociado=OuterRef("asociado"),
            estadoRegistro=True,
            pendientePago__gt=0,
            estado="OTORGADO",
        )
        .values("asociado")
        .annotate(
            total_cuotas_credito=Sum("valorCuota"),
            pendiente_pago_credito=Sum("pendientePago"),
            cuotas_totales_credito=Sum("cuotas"),
            cuotas_pagas_credito=Sum("cuotasPagas"),
        )
        .values(
            "total_cuotas_credito",
            "pendiente_pago_credito",
            "cuotas_totales_credito",
            "cuotas_pagas_credito",
        )
    )

    # Suma de convenios de gasolina pendientes
    convenios_gasolina = (
        ConvenioHistoricoGasolina.objects.filter(
            asociado=OuterRef("asociado"),
            estado_registro=True,
            pendiente_pago__gt=0,
            mes_tarifa__pk__lte = mes_seleccionado
        )
        .values("asociado")
        .annotate(total_pendiente_gasolina=Sum("pendiente_pago"))
        .values("total_pendiente_gasolina")
    )

    # Calcular cuota individual para cada home element pendiente
    # usando CASE para determinar si usar cuota normal o pendiente
    home_elements_cuota_total = (
        HistoricoVenta.objects.filter(
            asociado=OuterRef("asociado"),
            formaPago="DESCUENTO NOMINA",
            estadoRegistro=True,
            pendientePago__gt=0
        )
        .annotate(
            cuota_calculada=Case(
                # Si no hay pendiente de pago, la cuota es 0
                When(Q(pendientePago=0), then=Value(0)),
                # Si ya se pagaron todas las cuotas o más
                When(
                    Q(cuotasPagas__gte=F("cuotas")) & Q(pendientePago__gt=0),
                    then=F("pendientePago"),
                ),
                # Si estamos en la última cuota
                When(
                    Q(cuotasPagas=F("cuotas") - 1) & Q(pendientePago__gt=0),
                    then=F("pendientePago"),
                ),
                # NUEVO: Si el pendiente es menor que la cuota original (pago parcial)
                # y aún quedan cuotas por pagar
                When(
                    Q(pendientePago__lt=F("valorCuotas"))
                    & Q(cuotasPagas__lt=F("cuotas"))
                    & Q(pendientePago__gt=0),
                    then=F("pendientePago"),
                ),
                # En cualquier otro caso, usar la cuota original
                default=F("valorCuotas"),
                output_field=IntegerField(),
            )
        )
        .values("asociado")
        .annotate(total_cuota_home_calculada=Sum("cuota_calculada"))
        .values("total_cuota_home_calculada")
    )

    # Informacion convenios, obtener convenios que el pk mes seleccionado sea mayor al primerMes Cobro del convenio
    convenios_vigentes_sum = (
        ConveniosAsociado.objects.filter(
            asociado = OuterRef("asociado"),
            estadoRegistro = True,
            primerMes__pk__lte=mes_seleccionado
        ).values("asociado")
        .annotate(total_cuota=Sum("convenio__valor"))
        .values("total_cuota")
    )

    # Informacion mascotas
    valor_mascota = Tarifas.objects.get(pk=3).valor

    mascotas_vigentes_count = (
        Mascota.objects.filter(
            asociado = OuterRef("asociado"),
            estadoRegistro = True,
            primerMes__pk__lte = mes_seleccionado,
        ).values("asociado")
        .annotate(total=Count("id"))
        .values("total")
    )

    # Informacion repatriaciones
    valor_repatriacion = Tarifas.objects.get(pk=4).valor
    
    repatriaciones_vigentes_count = (
        Beneficiario.objects.filter(
            asociado = OuterRef("asociado"),
            estadoRegistro = True,
            primerMesRepatriacion__pk__lte = mes_seleccionado
        ).values("asociado")
        .annotate(total=Count("id"))
        .values("total")
    )

    # Informacion seguro de vida
    seguro_vida_vigente_sum = (
        HistoricoSeguroVida.objects.filter(
            asociado = OuterRef("asociado"),
            estadoRegistro = True, 
            primerMesSeguroVida__pk__lte = mes_seleccionado
        ).values("asociado")
        .annotate(total_cuota_seguro_vida=Sum("valorPago"))
        .values("total_cuota_seguro_vida")
    )

    # Informacion repatriacion titular
    repatriacion_titular_count = (
        RepatriacionTitular.objects.filter(
            asociado = OuterRef("asociado"),
            estadoRegistro = True,
            primerMes__pk__lte = mes_seleccionado
        ).values("asociado")
        .annotate(total=Count("id"))
        .values("total")[:1]
    )

    # Informacion adicionales funeraria
    adicional_funeraria_sum = (
        TarifaAsociado.objects.filter(
            asociado = OuterRef("asociado"),
            estadoRegistro = True,
            primerMesCuotaAdicional__pk__lte = mes_seleccionado
        ).values("asociado")
        .annotate(total=Sum("cuotaAdicionales"))
        .values("total")[:1]
    )

    # Informacion Coohoperativitos
    fecha_mes_seleccionado = MesTarifa.objects.get(pk = mes_seleccionado).fechaInicio
    valor_coohoperativito = Tarifas.objects.filter(pk__in = [5,6]).annotate(total=Sum("valor")).values("total")

    cuota_coohoperativitos_count = (
        Coohoperativitos.objects.filter(
            asociado = OuterRef("asociado"),
            estadoRegistro = True,
            fechaIngreso__lte = fecha_mes_seleccionado
        ).values("asociado")
        .annotate(total=Count("id"))
        .values("total")
    )

    query = (
        ParametroAsociado.objects.filter(
            asociado__tAsociado=empresa_pk,
            asociado__estadoAsociado__in=["ACTIVO", "INACTIVO"],
        )
        .annotate(
            # Pagos realizados
            pagos_realizados=Coalesce(
                Subquery(pagos_vinculacion, output_field=IntegerField()), Value(0)
            ),
            pagos_credito_realizados=Coalesce(
                Subquery(pagos_credito, output_field=IntegerField()), Value(0)
            ),
            pagos_home_realizados=Coalesce(
                Subquery(pagos_home_elements, output_field=IntegerField()), Value(0)
            ),
            # Convenios de gasolina
            cuota_convenio_gasolina=Coalesce(
                Subquery(convenios_gasolina, output_field=IntegerField()), Value(0)
            ),
            # Información adicional para cálculos
            credito_pendiente_pago=Coalesce(
                Subquery(
                    credito_info.values("pendiente_pago_credito"),
                    output_field=IntegerField(),
                ),
                Value(0),
            ),
            credito_cuotas_totales=Coalesce(
                Subquery(
                    credito_info.values("cuotas_totales_credito"),
                    output_field=IntegerField(),
                ),
                Value(0),
            ),
            credito_cuotas_pagas=Coalesce(
                Subquery(
                    credito_info.values("cuotas_pagas_credito"),
                    output_field=IntegerField(),
                ),
                Value(0),
            ),
            credito_valor_cuota_original=Coalesce(
                Subquery(
                    credito_info.values("total_cuotas_credito"),
                    output_field=IntegerField(),
                ),
                Value(0),
            ),
            # Usar la cuota total calculada individualmente para cada home element
            home_cuota_total_calculada=Coalesce(
                Subquery(home_elements_cuota_total, output_field=IntegerField()),
                Value(0),
            ),
            # Cuota de vinculación (ya existente)
            cuota_vinculacion=Case(
                When(Q(vinculacionPendientePago=0), then=Value(0)),
                When(
                    Q(pagos_realizados=F("vinculacionCuotas") - 1)
                    & Q(vinculacionFormaPago__pk=2)
                    & Q(vinculacionPendientePago__gt=0),
                    then=F("vinculacionPendientePago"),
                ),
                default=F("vinculacionValor"),
                output_field=IntegerField(),
            ),
            # Cuota de crédito con manejo completo de pagos parciales
            cuota_credito=Case(
                # Si no hay pendiente de pago, la cuota es 0
                When(Q(credito_pendiente_pago=0), then=Value(0)),
                # Si ya se pagaron todas las cuotas o más (cuotas_pagas >= cuotas_totales)
                # entonces usar solo el pendiente de pago
                When(
                    Q(credito_cuotas_pagas__gte=F("credito_cuotas_totales"))
                    & Q(credito_pendiente_pago__gt=0),
                    then=F("credito_pendiente_pago"),
                ),
                # Si estamos en la última cuota (cuotas_pagas = cuotas_totales - 1)
                # usar el pendiente de pago para manejar pagos parciales
                When(
                    Q(credito_cuotas_pagas=F("credito_cuotas_totales") - 1)
                    & Q(credito_pendiente_pago__gt=0),
                    then=F("credito_pendiente_pago"),
                ),
                # Si el pendiente es menor que la cuota original (pago parcial en cuota intermedia)
                # y aún quedan cuotas por pagar
                When(
                    Q(credito_pendiente_pago__lt=F("credito_valor_cuota_original"))
                    & Q(credito_cuotas_pagas__lt=F("credito_cuotas_totales"))
                    & Q(credito_pendiente_pago__gt=0),
                    then=F("credito_pendiente_pago"),
                ),
                # En cualquier otro caso, usar la cuota original
                default=F("credito_valor_cuota_original"),
                output_field=IntegerField(),
            ),

            # Agregamos al annotate cuota correspondiente a los convenios
            cuota_convenio_final = Coalesce(
                Subquery(convenios_vigentes_sum, output_field=IntegerField()),
                Value(0)
            ),

            # Agregar al annotate cuota de las mascotas
            mascotas_vigentes=Coalesce(
                Subquery(mascotas_vigentes_count, output_field=IntegerField()),
                Value(0)
            ),
            cuota_mascotas=F("mascotas_vigentes") * Value(valor_mascota),

            # Agregar al annotate cuota de las repatriaciones de beneficiarios
            repatriaciones_vigentes=Coalesce(
                Subquery(repatriaciones_vigentes_count, output_field=IntegerField()),
                Value(0)
            ),
            cuota_repatriaciones=F("repatriaciones_vigentes") * Value(valor_repatriacion),

            # Agregar al annotate cuota de seguro vida
            cuota_seguro_vida=Coalesce(
                Subquery(seguro_vida_vigente_sum, output_field=IntegerField()),
                Value(0)
            ),

            # Agregar al annotate cuota de las repatriaciones de titular
            repatriacion_titular_vigente=Coalesce(
                Subquery(repatriacion_titular_count, output_field=IntegerField()),
                Value(0)
            ),
            cuota_repatriacion_titular=F("repatriacion_titular_vigente") * Value(valor_repatriacion),

            # Agregar al annotate cuota de adicionales
            cuota_adicional_funeraria=Coalesce(
                Subquery(adicional_funeraria_sum, output_field=IntegerField()),
                Value(0)
            ),

            # Agregar al annotate cuota de coohoperativitos
            cuota_coohoperativitos_vigentes = Coalesce(
                Subquery(cuota_coohoperativitos_count, output_field=IntegerField()),
                Value(0)
            ),
            cuota_coohoperativitos=F("cuota_coohoperativitos_vigentes") * Value(valor_coohoperativito),

            # Cuota de home elements ya calculada individualmente
            cuota_credito_home_elements=F("home_cuota_total_calculada"),
            total_final=F("tarifaAsociado__cuotaAporte")
            + F("tarifaAsociado__cuotaBSocial")
            + F("cuota_coohoperativitos")
            + Coalesce(F("cuota_vinculacion"), Value(0))
            + F("cuota_credito")
            + F("cuota_credito_home_elements")
            + F("cuota_convenio_gasolina")
            + F("cuota_convenio_final")
            + F("cuota_mascotas")
            + F("cuota_repatriaciones")
            + F("cuota_seguro_vida")
            + F("cuota_repatriacion_titular")
            + F("cuota_adicional_funeraria")

        )
        .select_related("asociado__tAsociado")
    )

    granTotal = query.aggregate(total=Sum("total_final"))["total"] or 0

    return {"query": query, "granTotal": granTotal}


# def obtenerDescuentoNominav2(empresa_pk):
#     pagos_vinculacion = (
#         HistorialPagos.objects.filter(
#             asociado=OuterRef("asociado"), mesPago=9995, estadoRegistro=True
#         )
#         .values("asociado")
#         .annotate(
#             total_pagos=Count(
#                 "id"
#             )  # Cuenta cuántos pagos de vinculación ha hecho el asociado
#         )
#         .values("total_pagos")
#     )  # Devuelve solo el número de pagos realizados

#     credito_pendiente = (
#         HistoricoCredito.objects.filter(
#             asociado=OuterRef("asociado"),
#             estadoRegistro=True,
#             pendientePago__gt=0,
#             estado="OTORGADO",
#         )
#         .values("asociado")
#         .annotate(total_cuotas=Sum("valorCuota"))
#         .values("total_cuotas")
#     )

#     credito_home_elements = (
#         HistoricoVenta.objects.filter(
#             asociado=OuterRef("asociado"),
#             formaPago="DESCUENTO NOMINA",
#             estadoRegistro=True,
#             pendientePago__gt=0,
#         )
#         .values("asociado")
#         .annotate(total_cuota_home_element=Sum("valorCuotas"))
#         .values("total_cuota_home_element")
#     )

#     query = (
#         ParametroAsociado.objects.filter(
#             asociado__tAsociado=empresa_pk,
#             asociado__estadoAsociado__in=["ACTIVO", "INACTIVO"],
#         )
#         .annotate(
#             pagos_realizados=Coalesce(
#                 Subquery(pagos_vinculacion, output_field=IntegerField()), Value(0)
#             ),
#             cuota_vinculacion=Case(
#                 When(
#                     # Si ya pagó todo, no se debe sumar nada
#                     Q(vinculacionPendientePago=0),
#                     then=Value(0),
#                 ),
#                 # Si está en la última cuota, usar vinculaciónPendientePago
#                 When(
#                     Q(pagos_realizados=F("vinculacionCuotas") - 1)
#                     & Q(vinculacionFormaPago__pk=2)
#                     & Q(
#                         vinculacionPendientePago__gt=0
#                     ),  # se obtiene la cantidad de pagos de vinculacion, sino hay pagos el coalse devuelve 0
#                     then=F("vinculacionPendientePago"),
#                 ),
#                 # Si no es la última cuota, usar vinculaciónValor
#                 default=F("vinculacionValor"),
#                 output_field=IntegerField(),
#             ),
#             cuota_credito=Coalesce(
#                 Subquery(credito_pendiente, output_field=IntegerField()), Value(0)
#             ),
#             cuota_credito_home_elements=Coalesce(
#                 Subquery(credito_home_elements, output_field=IntegerField()), Value(0)
#             ),
#             total_final=F("tarifaAsociado__total")
#             + Coalesce(F("cuota_vinculacion"), Value(0))
#             + F("cuota_credito")
#             + F("cuota_credito_home_elements"),
#         )
#         .select_related("asociado__tAsociado")
#     )

#     # Obtener la suma total de 'total_final'
#     granTotal = query.aggregate(total=Sum("total_final"))["total"] or 0

#     return {"query": query, "granTotal": granTotal}
