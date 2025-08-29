from datetime import timedelta
from django.db.models import Subquery, Sum, Max
from beneficiario.models import Mascota, Beneficiario
from historico.models import HistorialPagos
from asociado.models import (
    ConveniosAsociado,
    ParametroAsociado,
    TarifaAsociado,
)
from beneficiario.models import Beneficiario, Mascota
from historico.models import HistorialPagos
from parametro.models import MesTarifa


def obtenerValorExtracto(id_asociado, saldos, mes, formato):
    parametro = ParametroAsociado.objects.select_related("primerMes").get(
        asociado=id_asociado
    )

    if saldos is False:
        print("entra")
        parametro.primerMes = mes

    # Entra al except cuando un asociado no ha realizado ningun pago y no existe informacion en la query
    try:
        # se valida si el primer mes de pago es igual o mayor a la seleccion del form
        if mes.pk >= parametro.primerMes.pk:
            print("if 1: Mes seleccionado es mayor o igual al mes de vinculacion")
            # Formato 4
            fechaCorte = timedelta(15) + mes.fechaInicio
            objTarifaAsociado = TarifaAsociado.objects.get(asociado=id_asociado)

            cuotaPeriodica = (
                objTarifaAsociado.cuotaAporte + objTarifaAsociado.cuotaBSocial
            )
            cuotaCoohop = (
                objTarifaAsociado.cuotaCoohopAporte
                + objTarifaAsociado.cuotaCoohopBsocial
            )

            # Inicializar contadores
            cuotaVencida = 0
            cuotaAdelantada = 0
            cuotaPeriodicaTotal = 0
            
            # Si se marca el check en saldos
            if saldos is True:
                # Obtener los meses pagados por el asociado, excluyendo los registros 9999 al 9990
                mesesPagados = (
                    HistorialPagos.objects.filter(asociado=id_asociado)
                    .exclude(
                        mesPago__in=[9999, 9998, 9997, 9996, 9995, 9994, 9993, 9992, 9991, 9990]
                    )
                    .values_list("mesPago", flat=True)
                )
                # Salida mesesPagados["ENERO 2025", "FEBRERO 2025", "MARZO 2025"]
                print(f"mesesPagados{mesesPagados}")

                # Obtener del modelo MesTarifa los meses pendientes por pagar
                mesesFaltantes = (
                    MesTarifa.objects.exclude(pk__in=Subquery(mesesPagados))
                    .exclude(
                        pk__in=[9999, 9998, 9997, 9996, 9995, 9994, 9993, 9992, 9991, 9990]
                    )
                    .filter(pk__gte=parametro.primerMes.pk, pk__lte=mes.pk)
                )
                # Salida queryMes, si no a pagado octubre sale ["OCTUBRE 2025"]
                print(f"meses pendientes por pagar {mesesFaltantes}")

                # Calcular cuotas vencidas y sumar las cuotas de meses pendientes
                for mesFaltante in mesesFaltantes:
                    cuotaPeriodicaTotal += mesFaltante.aporte + mesFaltante.bSocial
                    cuotaVencida += 1

                # Calcular cuotas adelantadas
                for mesPagado in mesesPagados:
                    if (
                        mesPagado > mes.pk
                    ):  # Si el mes pagado está fuera del rango actual, es adelantado
                        cuotaAdelantada += 1
            
            # sin saldos en el check
            else:
                cuota_mes = MesTarifa.objects.get(id = mes.pk)
                cuotaPeriodicaTotal = cuota_mes.aporte + cuota_mes.bSocial
                saldoDiferencia = 0
                cuotaVencida = 1

            pagoTotal = cuotaPeriodicaTotal

            # variables iniciacion
            saldo = 0
            valorVencido = 0
            valorVencidoMasc = 0
            valorVencidoRep = 0
            valorVencidoSeg = 0
            valorVencidoAdic = 0
            valorVencidoCoohop = 0
            valorVencidoConvenio = 0
            mensaje = ""

            # query mostrar beneficiarios y mascotas
            objBeneficiario = Beneficiario.objects.filter(
                asociado=id_asociado, estadoRegistro=True
            ).select_related("parentesco", "paisRepatriacion")

            cuentaBeneficiario = len(objBeneficiario)

            objMascota = Mascota.objects.filter(
                asociado=id_asociado, estadoRegistro=True
            )
            cuentaMascota = len(objMascota)


            print(f"mes seleccionado {mes.pk} - {mes}")
            # query convenios
            objConvenio = (
                ConveniosAsociado.objects.select_related("convenio")
                .filter(asociado=id_asociado, estadoRegistro=True, primerMes__lte=mes.pk)
            )
            print(objConvenio)

            if objConvenio:
                for convenio in objConvenio:

                    # Obtener del modelo MesTarifa los meses pendientes por pagar
                    meses_faltantes_convenios = (
                        MesTarifa.objects.exclude(pk__in=Subquery(mesesPagados))
                        .exclude(
                            pk__in=[9999, 9998, 9997, 9996, 9995, 9994, 9993, 9992, 9991, 9990]
                        )
                        .filter(pk__gte=convenio.primerMes.pk, pk__lte=mes.pk)
                    )
                    
                    convenio.cantidad_meses = meses_faltantes_convenios.count()
                    convenio.valor_vencido_convenio = convenio.convenio.valor * convenio.cantidad_meses
                    valorVencidoConvenio += convenio.valor_vencido_convenio
                    print(f"valorVencidoConvenio {valorVencidoConvenio}")
                    # Salida: Se obtiene el valor de cada convenio que debe teniendo en cuenta el primer mes de pago del convenio


            if saldos is True:
                # query que suma la diferencia de pagos
                querySaldoTotal = HistorialPagos.objects.filter(
                    asociado=id_asociado
                ).aggregate(total=Sum("diferencia"))

                # variable que guarda la diferencia en los saldos(0=esta al dia, > a 0, saldo favor, < a 0, saldo pendiente)
                saldoDiferencia = querySaldoTotal["total"] or 0

            # condicional si esta atrasado, si en ¿Traer saldos en pagos? se marca False entra aca
            if cuotaVencida > 0:
                print(f"cuota vencida {cuotaVencida}")
                if objTarifaAsociado.cuotaMascota > 0:
                    valorVencidoMasc = cuotaVencida * objTarifaAsociado.cuotaMascota
                if objTarifaAsociado.cuotaRepatriacion > 0:
                    valorVencidoRep = cuotaVencida * objTarifaAsociado.cuotaRepatriacion
                if objTarifaAsociado.cuotaSeguroVida > 0:
                    valorVencidoSeg = cuotaVencida * objTarifaAsociado.cuotaSeguroVida
                if objTarifaAsociado.cuotaAdicionales > 0:
                    valorVencidoAdic = cuotaVencida * objTarifaAsociado.cuotaAdicionales
                if objTarifaAsociado.cuotaCoohopAporte > 0:
                    valorVencidoCoohop = cuotaVencida * (
                        objTarifaAsociado.cuotaCoohopAporte
                        + objTarifaAsociado.cuotaCoohopBsocial
                    )

                if saldoDiferencia > 0:
                    # saldo a favor
                    valorVencido = cuotaPeriodicaTotal - saldoDiferencia
                    pagoTotal = (
                        valorVencido
                        + valorVencidoMasc
                        + valorVencidoRep
                        + valorVencidoSeg
                        + valorVencidoAdic
                        + valorVencidoCoohop
                        + valorVencidoConvenio
                    )
                    mensaje = "Tiene un saldo a favor de $" + str(saldoDiferencia)
                elif saldoDiferencia < 0:
                    # saldo a pagar
                    valorVencido = cuotaPeriodicaTotal - saldoDiferencia
                    pagoTotal = (
                        valorVencido
                        + valorVencidoMasc
                        + valorVencidoRep
                        + valorVencidoSeg
                        + valorVencidoAdic
                        + valorVencidoCoohop
                        + valorVencidoConvenio
                    )
                    mensaje = "Tiene un saldo pendiente por pagar de $" + str(
                        (saldoDiferencia * -1)
                    )
                else:
                    print("sin saldos")
                    # saldo en 0
                    valorVencido = cuotaPeriodicaTotal
                    print(f"valorVencido {valorVencido}")
                    pagoTotal = (
                        valorVencido
                        + valorVencidoMasc
                        + valorVencidoRep
                        + valorVencidoSeg
                        + valorVencidoAdic
                        + valorVencidoCoohop
                        + valorVencidoConvenio
                    )

                context = {
                    "pkAsociado": id_asociado,
                    "fechaCorte": fechaCorte,
                    "objTarifaAsociado": objTarifaAsociado,
                    "cuotaPeriodica": cuotaPeriodica,
                    "cuotaCoohop": cuotaCoohop,
                    "cuotaVencida": cuotaVencida,
                    "valorVencido": valorVencido,
                    "valorVencidoMasc": valorVencidoMasc,
                    "valorVencidoRep": valorVencidoRep,
                    "valorVencidoSeg": valorVencidoSeg,
                    "valorVencidoAdic": valorVencidoAdic,
                    "valorVencidoCoohop": valorVencidoCoohop,
                    "valorVencidoConvenio": valorVencidoConvenio,
                    "pagoTotal": pagoTotal,
                    "mes": mes,
                    "objBeneficiario": objBeneficiario,
                    "cuentaBeneficiario": cuentaBeneficiario,
                    "objMascota": objMascota,
                    "cuentaMascota": cuentaMascota,
                    "formato": formato,
                    "vista": 0,
                    "saldo": saldo,
                    "mensaje": mensaje,
                    "objConvenio": objConvenio,
                }

                return context

            # condicional si esta al dia y no tiene meses pendientes en los pagos
            elif cuotaAdelantada == 0 and cuotaVencida == 0:

                valorMensual = (
                    objTarifaAsociado.cuotaAporte
                    + objTarifaAsociado.cuotaBSocial
                    + objTarifaAsociado.cuotaMascota
                    + objTarifaAsociado.cuotaRepatriacion
                    + objTarifaAsociado.cuotaSeguroVida
                    + objTarifaAsociado.cuotaAdicionales
                    + objTarifaAsociado.cuotaCoohopAporte
                    + objTarifaAsociado.cuotaCoohopBsocial
                    + objTarifaAsociado.cuotaConvenio
                )

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
                    mensaje = "Tiene un saldo a favor de " + str(dif) + "."
                else:
                    # si saldo es menor, es porque tiene un saldo pendiente x pagar, se muestra el valor y se envia mensaje
                    valorVencido = valorMensual - saldo
                    pagoTotal = valorMensual - saldo
                    dif = valorMensual - saldo
                    mensaje = "Tiene un saldo pendiente por pagar de " + str(dif) + "."

                context = {
                    "pkAsociado": id_asociado,
                    "fechaCorte": fechaCorte,
                    "objTarifaAsociado": objTarifaAsociado,
                    "cuotaPeriodica": cuotaPeriodica,
                    "cuotaCoohop": cuotaCoohop,
                    "cuotaVencida": cuotaVencida,
                    "valorVencido": valorVencido,
                    "valorVencidoMasc": valorVencidoMasc,
                    "valorVencidoRep": valorVencidoRep,
                    "valorVencidoSeg": valorVencidoSeg,
                    "valorVencidoAdic": valorVencidoAdic,
                    "valorVencidoCoohop": valorVencidoCoohop,
                    "valorVencidoConvenio": valorVencidoConvenio,
                    "pagoTotal": pagoTotal,
                    "mes": mes,
                    "objBeneficiario": objBeneficiario,
                    "cuentaBeneficiario": cuentaBeneficiario,
                    "objMascota": objMascota,
                    "cuentaMascota": cuentaMascota,
                    "formato": formato,
                    "saldo": saldo,
                    "mensaje": mensaje,
                    "objConvenio": objConvenio,
                }
                return context

            # condicional si esta adelantado
            else:
                pagoTotal = 0
                # obtenemos el valor total que tiene pago el asociado, desde el mes seleccionado en la query hasta el pago en la bd
                query = (
                    HistorialPagos.objects.exclude(
                        mesPago__in=[
                            9999,
                            9998,
                            9997,
                            9996,
                            9995,
                            9994,
                            9993,
                            9992,
                            9991,
                            9990,
                        ]
                    )
                    .filter(mesPago__gte=mes.pk, asociado=id_asociado)
                    .aggregate(total=Sum("valorPago"))
                )

                # Obtenemos el saldo actual del asociado, del mes seleccionado hasta el ultimo pago
                for valor in query.values():
                    saldoActual = valor

                # si tiene un saldo en diferencia, se calcula el saldo
                if saldoDiferencia > 0:
                    saldo = saldoActual + saldoDiferencia
                elif saldoDiferencia < 0:
                    saldo = saldoActual + saldoDiferencia
                else:
                    saldo = saldoActual

                # Obtenemos el pk de la tabla de pagos con el pk del pago mas alto
                max_mes_pago_pk = (
                    HistorialPagos.objects.exclude(
                        mesPago__in=[
                            9999,
                            9998,
                            9997,
                            9996,
                            9995,
                            9994,
                            9993,
                            9992,
                            9991,
                            9990,
                        ]
                    )
                    .filter(asociado=id_asociado)
                    .aggregate(max_mes_pk=Max("mesPago"))["max_mes_pk"]
                )

                # Obtenemos el nombre del mes con el pk del pago mas alto
                obj_historial_pago = HistorialPagos.objects.filter(
                    mesPago=max_mes_pago_pk, asociado=id_asociado
                ).first()

                mensaje = (
                    "Tiene Pago hasta el mes de "
                    + obj_historial_pago.mesPago.concepto
                    + "."
                )
                context = {
                    "pkAsociado": id_asociado,
                    "fechaCorte": fechaCorte,
                    "objTarifaAsociado": objTarifaAsociado,
                    "cuotaPeriodica": cuotaPeriodica,
                    "cuotaCoohop": cuotaCoohop,
                    "cuotaVencida": cuotaVencida,
                    "valorVencido": valorVencido,
                    "valorVencidoMasc": valorVencidoMasc,
                    "valorVencidoRep": valorVencidoRep,
                    "valorVencidoSeg": valorVencidoSeg,
                    "valorVencidoAdic": valorVencidoAdic,
                    "valorVencidoCoohop": valorVencidoCoohop,
                    "valorVencidoConvenio": valorVencidoConvenio,
                    "pagoTotal": pagoTotal,
                    "mes": mes,
                    "objBeneficiario": objBeneficiario,
                    "cuentaBeneficiario": cuentaBeneficiario,
                    "objMascota": objMascota,
                    "cuentaMascota": cuentaMascota,
                    "formato": formato,
                    "saldo": saldo,
                    "mensaje": mensaje,
                    "objConvenio": objConvenio,
                }
                return context

    # si no hay pagos en la bd
    except Exception as e:
        print(f"excepcion de no pagos en la db {e}")
        # query mostrar beneficiarios y mascotas
        objBeneficiario = Beneficiario.objects.filter(
            asociado=id_asociado, estadoRegistro=True
        ).select_related("parentesco", "paisRepatriacion")
        saldo = 0
        cuentaBeneficiario = len(objBeneficiario)
        objMascota = Mascota.objects.filter(asociado=id_asociado, estadoRegistro=True)
        # query convenios
        objConvenio = (
            ConveniosAsociado.objects.select_related("convenio")
            .filter(asociado=id_asociado, estadoRegistro=True)
            .first()
        )
        cuentaMascota = len(objMascota)
        valorVencidoMasc = objTarifaAsociado.cuotaMascota
        valorVencidoRep = objTarifaAsociado.cuotaRepatriacion
        valorVencidoSeg = objTarifaAsociado.cuotaSeguroVida
        valorVencidoAdic = objTarifaAsociado.cuotaAdicionales
        valorVencidoCoohop = (
            objTarifaAsociado.cuotaCoohopAporte + objTarifaAsociado.cuotaCoohopBsocial
        )
        valorVencidoConvenio = objTarifaAsociado.cuotaConvenio
        # obtenemos el parametro del primer mes q debe pagar
        if cuotaVencida == 0:
            # mes seleccionado igual al parametro.primerMes
            valorVencido = cuotaPeriodicaTotal
            pagoTotal = (
                valorVencido
                + valorVencidoMasc
                + valorVencidoRep
                + valorVencidoSeg
                + valorVencidoAdic
                + valorVencidoCoohop
                + valorVencidoConvenio
            )
        elif cuotaVencida > 0:
            # mes adelantado al parametro.primerMes
            valorVencido = cuotaPeriodicaTotal
            valorVencidoMasc = objTarifaAsociado.cuotaMascota * cuotaVencida
            valorVencidoRep = objTarifaAsociado.cuotaRepatriacion * cuotaVencida
            valorVencidoSeg = objTarifaAsociado.cuotaSeguroVida * cuotaVencida
            valorVencidoAdic = objTarifaAsociado.cuotaAdicionales * cuotaVencida
            valorVencidoCoohop = (
                objTarifaAsociado.cuotaCoohopAporte
                + objTarifaAsociado.cuotaCoohopBsocial
            ) * cuotaVencida
            valorVencidoConvenio = objTarifaAsociado.cuotaConvenio * cuotaVencida
            pagoTotal = (
                valorVencido
                + valorVencidoMasc
                + valorVencidoRep
                + valorVencidoSeg
                + valorVencidoAdic
                + valorVencidoCoohop
                + valorVencidoConvenio
            )
        else:
            pass

        context = {
            "pkAsociado": id_asociado,
            "fechaCorte": fechaCorte,
            "objTarifaAsociado": objTarifaAsociado,
            "cuotaPeriodica": cuotaPeriodica,
            "cuotaCoohop": cuotaCoohop,
            "cuotaVencida": cuotaVencida,
            "valorVencido": valorVencido,
            "valorVencidoMasc": valorVencidoMasc,
            "valorVencidoRep": valorVencidoRep,
            "valorVencidoSeg": valorVencidoSeg,
            "valorVencidoAdic": valorVencidoAdic,
            "valorVencidoCoohop": valorVencidoCoohop,
            "valorVencidoConvenio": valorVencidoConvenio,
            "pagoTotal": pagoTotal,
            "mes": mes,
            "objBeneficiario": objBeneficiario,
            "cuentaBeneficiario": cuentaBeneficiario,
            "objMascota": objMascota,
            "cuentaMascota": cuentaMascota,
            "formato": formato,
            "saldo": saldo,
            "objConvenio": objConvenio,
        }
        return context
