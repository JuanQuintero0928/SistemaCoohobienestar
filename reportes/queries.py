from django.db.models.functions import TruncSecond, Coalesce
from django.db.models import OuterRef, Subquery, Count, IntegerField, Value, Case, When, F, Q, Sum

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

    queryMascota = Mascota.objects.filter(
        fechaModificacion__range=[fecha_inicial, fecha_final]
        ).annotate(
            fechaModificacion_truncada=TruncSecond('fechaModificacion'),
            fechaCreacion_truncada=TruncSecond('fechaCreacion'),
        ).select_related('asociado')

    queryBeneficiario = Beneficiario.objects.filter(
        fechaModificacion__range=[fecha_inicial, fecha_final]
        ).annotate(
            fechaModificacion_truncada=TruncSecond('fechaModificacion'),
            fechaCreacion_truncada=TruncSecond('fechaCreacion'),
        ).select_related('asociado','paisRepatriacion','parentesco')

    queryRepatriacionTitular = RepatriacionTitular.objects.filter(
        fechaRepatriacion__range=[fecha_inicial, fecha_final]
        ).select_related('asociado','paisRepatriacion')

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
                            total_pagos=Count('id')     # Cuenta cuántos pagos de vinculación ha hecho el asociado
                        ).values('total_pagos')         # Devuelve solo el número de pagos realizados

    credito_pendiente = HistoricoCredito.objects.filter(
                                asociado=OuterRef('asociado'),
                                estadoRegistro=True,
                                pendientePago__gt=0,
                                estado = 'OTORGADO'
                            ).values('asociado').annotate(
                                total_cuotas=Sum('valorCuota')
                            ).values('total_cuotas')
    
    credito_home_elements = HistoricoVenta.objects.filter(
                                asociado=OuterRef('asociado'),
                                formaPago='DESCUENTO NOMINA',
                                estadoRegistro=True,
                                pendientePago__gt=0,
                            ).values('asociado').annotate(
                                total_cuota_home_element=Sum('valorCuotas')
                            ).values('total_cuota_home_element')

    query = ParametroAsociado.objects.filter(
                            asociado__tAsociado=empresa_pk,
                            asociado__estadoAsociado__in=['ACTIVO', 'INACTIVO']
                        ).annotate(
                            pagos_realizados=Coalesce(Subquery(pagos_vinculacion, output_field=IntegerField()), Value(0)),
                            cuota_vinculacion=Case(
                                When(
                                    # Si ya pagó todo, no se debe sumar nada
                                    Q(vinculacionPendientePago=0),
                                    then=Value(0)
                                ),
                                # Si está en la última cuota, usar vinculaciónPendientePago
                                When(
                                    Q(pagos_realizados=F('vinculacionCuotas') - 1) & Q(vinculacionFormaPago__pk=2) & Q(vinculacionPendientePago__gt=0), # se obtiene la cantidad de pagos de vinculacion, sino hay pagos el coalse devuelve 0
                                    then=F('vinculacionPendientePago')
                                ),
                                # Si no es la última cuota, usar vinculaciónValor
                                default=F('vinculacionValor'),
                                output_field=IntegerField()
                            ),
                            cuota_credito=Coalesce(Subquery(credito_pendiente, output_field=IntegerField()), Value(0)),
                            cuota_credito_home_elements=Coalesce(Subquery(credito_home_elements, output_field=IntegerField()), Value(0)),
                            total_final=F('tarifaAsociado__total') + Coalesce(F('cuota_vinculacion'), Value(0)) + F('cuota_credito') + F('cuota_credito_home_elements')
                        ).select_related('asociado__tAsociado')

    # Obtener la suma total de 'total_final'
    granTotal = query.aggregate(total=Sum('total_final'))['total'] or 0

    return {
        'query': query,
        'granTotal': granTotal
    }