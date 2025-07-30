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
)

from beneficiario.models import Asociado, Mascota, Beneficiario
from asociado.models import RepatriacionTitular, ParametroAsociado
from historico.models import HistorialPagos, HistoricoCredito
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


def obtenerDescuentoNomina(empresa_pk):
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
            estadoRegistro=True
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
            estadoRegistro=True
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
            cuotas_pagas_credito=Sum("cuotasPagas")  # AGREGADO: cuotas ya pagadas
        )
        .values("total_cuotas_credito", "pendiente_pago_credito", "cuotas_totales_credito", "cuotas_pagas_credito")
    )

    # Información de home elements pendientes
    home_elements_info = (
        HistoricoVenta.objects.filter(
            asociado=OuterRef("asociado"),
            formaPago="DESCUENTO NOMINA",
            estadoRegistro=True,
            pendientePago__gt=0,
        )
        .values("asociado")
        .annotate(
            total_cuota_home_element=Sum("valorCuotas"),
            pendiente_pago_home=Sum("pendientePago"),
            cuotas_totales_home=Sum("cuotas"),
            cuotas_pagas_home=Sum("cuotasPagas")  # AGREGADO: cuotas ya pagadas
        )
        .values("total_cuota_home_element", "pendiente_pago_home", "cuotas_totales_home", "cuotas_pagas_home")
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
            
            # Información adicional para cálculos
            credito_pendiente_pago=Coalesce(
                Subquery(credito_info.values("pendiente_pago_credito"), output_field=IntegerField()), 
                Value(0)
            ),
            credito_cuotas_totales=Coalesce(
                Subquery(credito_info.values("cuotas_totales_credito"), output_field=IntegerField()), 
                Value(0)
            ),
            credito_cuotas_pagas=Coalesce(  # AGREGADO
                Subquery(credito_info.values("cuotas_pagas_credito"), output_field=IntegerField()), 
                Value(0)
            ),
            home_pendiente_pago=Coalesce(
                Subquery(home_elements_info.values("pendiente_pago_home"), output_field=IntegerField()), 
                Value(0)
            ),
            home_cuotas_totales=Coalesce(
                Subquery(home_elements_info.values("cuotas_totales_home"), output_field=IntegerField()), 
                Value(0)
            ),
            home_cuotas_pagas=Coalesce(  # AGREGADO
                Subquery(home_elements_info.values("cuotas_pagas_home"), output_field=IntegerField()), 
                Value(0)
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
            
            # Cuota de crédito con lógica corregida
            cuota_credito=Case(
                When(Q(credito_pendiente_pago=0), then=Value(0)),
                # CORREGIDO: Si las cuotas pagadas son mayor o igual a las cuotas totales
                # Y hay pendiente de pago, usar el pendiente (maneja pagos parciales)
                When(
                    Q(credito_cuotas_pagas__gte=F("credito_cuotas_totales"))
                    & Q(credito_pendiente_pago__gt=0),
                    then=F("credito_pendiente_pago"),
                ),
                # CORREGIDO: También verificar con los pagos realizados (lógica anterior)
                When(
                    Q(pagos_credito_realizados=F("credito_cuotas_totales") - 1)
                    & Q(credito_pendiente_pago__gt=0),
                    then=F("credito_pendiente_pago"),
                ),
                default=Coalesce(
                    Subquery(credito_info.values("total_cuotas_credito"), output_field=IntegerField()), 
                    Value(0)
                ),
                output_field=IntegerField(),
            ),
            
            # Cuota de home elements con lógica corregida
            cuota_credito_home_elements=Case(
                When(Q(home_pendiente_pago=0), then=Value(0)),
                # CORREGIDO: Si las cuotas pagadas son mayor o igual a las cuotas totales
                # Y hay pendiente de pago, usar el pendiente (maneja pagos parciales)
                When(
                    Q(home_cuotas_pagas__gte=F("home_cuotas_totales"))
                    & Q(home_pendiente_pago__gt=0),
                    then=F("home_pendiente_pago"),
                ),
                # CORREGIDO: También verificar con los pagos realizados (lógica anterior)
                When(
                    Q(pagos_home_realizados=F("home_cuotas_totales") - 1)
                    & Q(home_pendiente_pago__gt=0),
                    then=F("home_pendiente_pago"),
                ),
                default=Coalesce(
                    Subquery(home_elements_info.values("total_cuota_home_element"), output_field=IntegerField()), 
                    Value(0)
                ),
                output_field=IntegerField(),
            ),
            
            total_final=F("tarifaAsociado__total")
            + Coalesce(F("cuota_vinculacion"), Value(0))
            + F("cuota_credito")
            + F("cuota_credito_home_elements"),
        )
        .select_related("asociado__tAsociado")
    )

    granTotal = query.aggregate(total=Sum("total_final"))["total"] or 0

    return {"query": query, "granTotal": granTotal}

def obtenerDescuentoNominav2(empresa_pk):
    pagos_vinculacion = (
        HistorialPagos.objects.filter(
            asociado=OuterRef("asociado"), mesPago=9995, estadoRegistro=True
        )
        .values("asociado")
        .annotate(
            total_pagos=Count(
                "id"
            )  # Cuenta cuántos pagos de vinculación ha hecho el asociado
        )
        .values("total_pagos")
    )  # Devuelve solo el número de pagos realizados

    credito_pendiente = (
        HistoricoCredito.objects.filter(
            asociado=OuterRef("asociado"),
            estadoRegistro=True,
            pendientePago__gt=0,
            estado="OTORGADO",
        )
        .values("asociado")
        .annotate(total_cuotas=Sum("valorCuota"))
        .values("total_cuotas")
    )

    credito_home_elements = (
        HistoricoVenta.objects.filter(
            asociado=OuterRef("asociado"),
            formaPago="DESCUENTO NOMINA",
            estadoRegistro=True,
            pendientePago__gt=0,
        )
        .values("asociado")
        .annotate(total_cuota_home_element=Sum("valorCuotas"))
        .values("total_cuota_home_element")
    )

    query = (
        ParametroAsociado.objects.filter(
            asociado__tAsociado=empresa_pk,
            asociado__estadoAsociado__in=["ACTIVO", "INACTIVO"],
        )
        .annotate(
            pagos_realizados=Coalesce(
                Subquery(pagos_vinculacion, output_field=IntegerField()), Value(0)
            ),
            cuota_vinculacion=Case(
                When(
                    # Si ya pagó todo, no se debe sumar nada
                    Q(vinculacionPendientePago=0),
                    then=Value(0),
                ),
                # Si está en la última cuota, usar vinculaciónPendientePago
                When(
                    Q(pagos_realizados=F("vinculacionCuotas") - 1)
                    & Q(vinculacionFormaPago__pk=2)
                    & Q(
                        vinculacionPendientePago__gt=0
                    ),  # se obtiene la cantidad de pagos de vinculacion, sino hay pagos el coalse devuelve 0
                    then=F("vinculacionPendientePago"),
                ),
                # Si no es la última cuota, usar vinculaciónValor
                default=F("vinculacionValor"),
                output_field=IntegerField(),
            ),
            cuota_credito=Coalesce(
                Subquery(credito_pendiente, output_field=IntegerField()), Value(0)
            ),
            cuota_credito_home_elements=Coalesce(
                Subquery(credito_home_elements, output_field=IntegerField()), Value(0)
            ),
            total_final=F("tarifaAsociado__total")
            + Coalesce(F("cuota_vinculacion"), Value(0))
            + F("cuota_credito")
            + F("cuota_credito_home_elements"),
        )
        .select_related("asociado__tAsociado")
    )

    # Obtener la suma total de 'total_final'
    granTotal = query.aggregate(total=Sum("total_final"))["total"] or 0

    return {"query": query, "granTotal": granTotal}
