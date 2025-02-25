from django.db.models.functions import TruncSecond, Coalesce
from django.db.models import OuterRef, Subquery, Count, IntegerField, Value, Case, When, F, Q, Sum

from beneficiario.models import Asociado, Mascota, Beneficiario
from asociado.models import RepatriacionTitular, ParametroAsociado
from historico.models import HistorialPagos, HistoricoCredito

def obtenerNovedades(fecha_inicial, fecha_final):
    asociadoRetiro = Asociado.objects.filter(
        fechaRetiro__range=[fecha_inicial, fecha_final]
    )
    asociadoIngreso = Asociado.objects.filter(
        fechaIngreso__range=[fecha_inicial, fecha_final]
    )
    queryMascota = Mascota.objects.filter(
        fechaModificacion__range=[fecha_inicial, fecha_final]
    ).annotate(
        fechaModificacion_truncada=TruncSecond('fechaModificacion'),
        fechaCreacion_truncada=TruncSecond('fechaCreacion'),
    )
    queryBeneficiario = Beneficiario.objects.filter(
        fechaModificacion__range=[fecha_inicial, fecha_final]
    ).annotate(
        fechaModificacion_truncada=TruncSecond('fechaModificacion'),
        fechaCreacion_truncada=TruncSecond('fechaCreacion'),
    )
    queryRepatriacionTitular = RepatriacionTitular.objects.filter(
        fechaRepatriacion__range=[fecha_inicial, fecha_final]
    )

    return {
        "asociadoRetiro": asociadoRetiro,
        "asociadoIngreso": asociadoIngreso,
        "queryMascota": queryMascota,
        "queryBeneficiario": queryBeneficiario,
        "queryRepatriacionTitular": queryRepatriacionTitular
    }

def obtenerDescuentoNomina(empresa_pk):
    pagos_vinculacion = HistorialPagos.objects.filter(
                            asociado=OuterRef('asociado'),
                            mesPago=9995,
                            estadoRegistro=True
                        ).values('asociado').annotate(
                            total_pagos=Count('id')
                        ).values('total_pagos')

    credito_pendiente = HistoricoCredito.objects.filter(
                                asociado=OuterRef('asociado'),
                                estadoRegistro=True,
                                pendientePago__gt=0
                            ).values('asociado').annotate(
                                total_cuotas=Sum('valorCuota')
                            ).values('total_cuotas')

    query = ParametroAsociado.objects.filter(
                            empresa=empresa_pk,
                            asociado__estadoAsociado='ACTIVO'
                        ).annotate(
                            pagos_realizados=Coalesce(Subquery(pagos_vinculacion, output_field=IntegerField()), Value(0)),
                            cuota_vinculacion=Case(
                                # Si está en la última cuota, usar vinculaciónPendientePago
                                When(
                                    Q(pagos_realizados=F('vinculacionCuotas') - 1) & Q(vinculacionFormaPago__pk=2) & Q(vinculacionPendientePago__gt=0),
                                    then=F('vinculacionPendientePago')
                                ),
                                # Si no es la última cuota, usar vinculaciónValor
                                default=F('vinculacionValor'),
                                output_field=IntegerField()
                            ),
                            cuota_credito=Coalesce(Subquery(credito_pendiente, output_field=IntegerField()), Value(0)),
                            total_final=F('tarifaAsociado__total') + Coalesce(F('cuota_vinculacion'), Value(0)) + F('cuota_credito')
                        )

    # Obtener la suma total de 'total_final'
    granTotal = query.aggregate(total=Sum('total_final'))['total'] or 0

    return {
        'query': query,
        'granTotal': granTotal
    }