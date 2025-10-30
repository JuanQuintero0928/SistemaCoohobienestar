from datetime import timedelta
from django.db.models import Subquery, Sum, Max, Count, Q
from typing import Dict, List, Tuple, Optional
from beneficiario.models import Mascota, Beneficiario
from historico.models import HistorialPagos
from asociado.models import (
    ConveniosAsociado,
    ParametroAsociado,
    TarifaAsociado,
    ConvenioHistoricoGasolina,
    RepatriacionTitular
)
from beneficiario.models import Beneficiario, Mascota
from historico.models import HistorialPagos, HistoricoCredito, HistoricoSeguroVida
from parametro.models import MesTarifa
from ventas.models import HistoricoVenta
"""
Refactorización del sistema de extractos financieros
Versión 2.0 - Con soporte para primerMes en mascotas, repatriaciones y convenio gasolina
"""

# ============================================================================
# CONSTANTES
# ============================================================================
CODIGOS_ESPECIALES = [9999, 9998, 9997, 9996, 9995, 9994, 9993, 9992, 9991, 9990, 9989]

CODIGO_ABONO = 9999
CODIGO_CREDITO_HOME = 9998
CODIGO_CREDITO_LIBRE = 9993

CONVENIO_GASOLINA_ID = 4  # ID del convenio de gasolina


# ============================================================================
# 1. SERVICIOS DE CONSULTA (Queries reutilizables)
# ============================================================================

class ConsultaPagosService:
    """Servicio para consultas relacionadas con pagos"""
    
    @staticmethod
    def obtener_meses_pagados(id_asociado: int) -> List[int]:
        """Obtiene los IDs de los meses que ya fueron pagados"""
        return list(
            HistorialPagos.objects.filter(asociado=id_asociado, estadoRegistro=True)
            .exclude(mesPago__in=CODIGOS_ESPECIALES)
            .values_list("mesPago", flat=True)
        )
    
    @staticmethod
    def obtener_meses_pendientes(id_asociado: int, mes_inicio_pk: int, mes_fin_pk: int, meses_pagados: List[int]):
        """Obtiene los meses pendientes de pago en un rango"""
        return MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
            pk__in=CODIGOS_ESPECIALES
        ).filter(pk__gte=mes_inicio_pk, pk__lte=mes_fin_pk)
    
    @staticmethod
    def calcular_saldo_diferencia(id_asociado: int) -> int:
        """Calcula el saldo total de diferencias (positivo=favor, negativo=debe, 0=al día)"""
        resultado = HistorialPagos.objects.filter(
            asociado=id_asociado, estadoRegistro=True
        ).aggregate(total=Sum("diferencia"))
        return resultado["total"] or 0
    
    @staticmethod
    def obtener_saldo_adelantado(id_asociado: int, mes_pk: int) -> int:
        """Calcula el saldo de pagos adelantados desde un mes específico"""
        resultado = (
            HistorialPagos.objects.exclude(mesPago__in=CODIGOS_ESPECIALES)
            .filter(mesPago__gte=mes_pk, asociado=id_asociado, estadoRegistro=True)
            .aggregate(total=Sum("valorPago"))
        )
        return resultado["total"] or 0
    
    @staticmethod
    def obtener_ultimo_mes_pagado(id_asociado: int):
        """Obtiene el último mes pagado por el asociado"""
        max_mes_pk = (
            HistorialPagos.objects.exclude(mesPago__in=CODIGOS_ESPECIALES)
            .filter(asociado=id_asociado, estadoRegistro=True)
            .aggregate(max_mes=Max("mesPago"))["max_mes"]
        )
        
        if max_mes_pk:
            return HistorialPagos.objects.filter(
                mesPago=max_mes_pk, asociado=id_asociado, estadoRegistro=True
            ).first()
        return None


class ConsultaCreditosService:
    """Servicio para consultas relacionadas con créditos"""
    
    @staticmethod
    def obtener_creditos_activos(id_asociado: int) -> List[Dict]:
        """Obtiene todos los créditos activos con saldo pendiente"""
        creditos = HistoricoCredito.objects.filter(
            asociado=id_asociado,
            estadoRegistro=True,
            estado="OTORGADO",
            pendientePago__gt=0
        ).select_related('tasaInteres')
        
        return [
            {
                'id': credito.id,
                'tipo': 'CREDITO LIBRE INVERSION',
                'linea': credito.lineaCredito,
                'valor_cuota': credito.valorCuota,
                'cuotas_totales': credito.cuotas,
                'cuotas_pagas': credito.cuotasPagas or 0,
                'pendiente_pago': credito.pendientePago,
                'total_credito': credito.totalCredito,
            }
            for credito in creditos
        ]
    
    @staticmethod
    def obtener_ventas_home_elements_activas(id_asociado: int) -> List[Dict]:
        """Obtiene todas las ventas de home elements con saldo pendiente"""
        ventas = HistoricoVenta.objects.filter(
            asociado=id_asociado,
            estadoRegistro=True,
            formaPago__in=['CREDITO', 'DESCUENTO NOMINA'],
            pendientePago__gt=0
        ).select_related('tasaInteres', 'descuento')
        
        return [
            {
                'id': venta.id,
                'tipo': 'CREDITO HOME ELEMENTS',
                'valor_cuota': venta.valorCuotas,
                'cuotas_totales': venta.cuotas,
                'cuotas_pagas': venta.cuotasPagas or 0,
                'pendiente_pago': venta.pendientePago,
                'total_venta': venta.valorNeto,
            }
            for venta in ventas
        ]


class ConsultaConveniosService:
    """Servicio para consultas relacionadas con convenios"""
    
    @staticmethod
    def obtener_convenios_activos_separados(id_asociado: int, mes_pk: int) -> Tuple[List, bool]:
        """
        Obtiene convenios activos separando gasolina de los demás
        
        Returns:
            Tuple[convenios_normales, tiene_gasolina]
        """
        convenios_todos = ConveniosAsociado.objects.select_related("convenio").filter(
            asociado=id_asociado,
            estadoRegistro=True,
            primerMes__lte=mes_pk
        )
        
        convenios_normales = []
        tiene_gasolina = False
        
        for conv in convenios_todos:
            if conv.convenio.id == CONVENIO_GASOLINA_ID:
                tiene_gasolina = True
            else:
                convenios_normales.append(conv)
        
        return convenios_normales, tiene_gasolina
    
    @staticmethod
    def calcular_meses_pendientes_convenio(convenio, mes_fin_pk: int, meses_pagados: List[int]) -> int:
        """Calcula cuántos meses debe un convenio específico"""
        meses_faltantes = (
            MesTarifa.objects.exclude(pk__in=meses_pagados)
            .exclude(pk__in=CODIGOS_ESPECIALES)
            .filter(pk__gte=convenio.primerMes.pk, pk__lte=mes_fin_pk)
        )
        return meses_faltantes.count()
    
    @staticmethod
    def obtener_total_gasolina(id_asociado: int) -> int:
        """Obtiene el total pendiente de pago del convenio de gasolina"""
        total = ConvenioHistoricoGasolina.objects.filter(
            asociado=id_asociado,
            estado_registro=True
        ).aggregate(total=Sum('pendiente_pago'))
        return total['total'] or 0


class ConsultaBeneficiariosService:
    """Servicio para consultas de beneficiarios y servicios asociados"""
    
    @staticmethod
    def obtener_beneficiarios_activos(id_asociado: int):
        """Obtiene beneficiarios activos con información de repatriación"""
        return Beneficiario.objects.filter(
            asociado=id_asociado, 
            estadoRegistro=True
        ).select_related("parentesco", "paisRepatriacion", "primerMesRepatriacion")
    
    @staticmethod
    def obtener_mascotas_activas(id_asociado: int):
        """Obtiene mascotas activas"""
        return Mascota.objects.filter(
            asociado=id_asociado, 
            estadoRegistro=True
        ).select_related("primerMes")
    
    @staticmethod
    def obtener_repatriacion_titular(id_asociado: int):
        """Obtiene la repatriación del titular si existe"""
        return RepatriacionTitular.objects.filter(
            asociado=id_asociado,
            estadoRegistro=True
        ).select_related("primerMes", "paisRepatriacion").first()
    
    @staticmethod
    def obtener_seguro_vida_activo(id_asociado: int):
        """Obtiene el seguro de vida activo del asociado si existe"""
        return HistoricoSeguroVida.objects.filter(
            asociado=id_asociado,
            estadoRegistro=True
        ).select_related("primerMesSeguroVida").first()


# ============================================================================
# 2. SERVICIOS DE CÁLCULO (Funciones puras)
# ============================================================================

class CalculadoraCuotasService:
    """Servicio para calcular cuotas y valores"""
    
    @staticmethod
    def calcular_cuota_periodica(tarifa_asociado) -> int:
        """Calcula la cuota periódica base (aporte + bienestar social)"""
        return tarifa_asociado.cuotaAporte + tarifa_asociado.cuotaBSocial
    
    @staticmethod
    def calcular_cuota_coohop(tarifa_asociado) -> int:
        """Calcula la cuota de Coohoperativitos"""
        return (
            (tarifa_asociado.cuotaCoohopAporte or 0) + 
            (tarifa_asociado.cuotaCoohopBsocial or 0)
        )
    
    @staticmethod
    def calcular_cuotas_vencidas_y_total(meses_faltantes, incluir_saldos: bool) -> Tuple[int, int]:
        """
        Calcula cantidad de cuotas vencidas y el total adeudado
        
        Returns:
            Tuple[cuotas_vencidas, cuota_periodica_total]
        """
        if not incluir_saldos:
            # Sin saldos: solo el mes seleccionado
            if meses_faltantes.exists():
                mes = meses_faltantes.first()
                return 1, mes.aporte + mes.bSocial
            return 0, 0
        
        # Con saldos: sumar todos los meses pendientes
        cuotas_vencidas = meses_faltantes.count()
        cuota_total = sum(mes.aporte + mes.bSocial for mes in meses_faltantes)
        return cuotas_vencidas, cuota_total
    
    @staticmethod
    def calcular_cuotas_adelantadas(meses_pagados: List[int], mes_actual_pk: int) -> int:
        """Cuenta cuántas cuotas están adelantadas respecto al mes actual"""
        return sum(1 for mes_pk in meses_pagados if mes_pk > mes_actual_pk)
    
    @staticmethod
    def calcular_meses_vencidos_servicio(primer_mes_pk: int, mes_actual_pk: int, meses_pagados: List[int]) -> int:
        """
        Calcula cuántos meses debe un servicio específico (mascota, repatriación)
        considerando su primerMes
        """
        if not primer_mes_pk:
            return 0
        
        meses_pendientes = (
            MesTarifa.objects.exclude(pk__in=meses_pagados)
            .exclude(pk__in=CODIGOS_ESPECIALES)
            .filter(pk__gte=primer_mes_pk, pk__lte=mes_actual_pk)
        )
        return meses_pendientes.count()
    
    @staticmethod
    def calcular_valores_mascotas(mascotas, mes_actual_pk: int, meses_pagados: List[int], 
                                  incluir_saldos: bool, valor_unitario: int) -> Tuple[int, int]:
        """
        Calcula el valor vencido de mascotas considerando primerMes individual
        Calcula mes por mes cuántas mascotas estaban activas
        
        Returns:
            Tuple[valor_vencido_mascotas, cantidad_cuotas_totales]
        """
        if not incluir_saldos:
            # Sin saldos: solo cuenta las mascotas activas en el mes actual
            return len(mascotas) * valor_unitario, len(mascotas) if mascotas else 0
        
        # Obtener todos los meses pendientes
        meses_pendientes = MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
            pk__in=CODIGOS_ESPECIALES
        ).filter(pk__lte=mes_actual_pk).order_by('pk')
        
        valor_total = 0
        cuotas_totales = 0
        
        # DEBUG: Imprimir información
        print("\n=== DEBUG MASCOTAS ===")
        print(f"Total mascotas: {len(mascotas)}")
        print(f"Valor unitario: {valor_unitario}")
        print(f"Meses pendientes: {[m.concepto for m in meses_pendientes]}")
        
        # Calcular mes por mes cuántas mascotas estaban activas
        for mes in meses_pendientes:
            mascotas_activas_este_mes = 0
            
            for mascota in mascotas:
                # Verificar si la mascota ya estaba activa en este mes
                primer_mes_pk = mascota.primerMes.pk if mascota.primerMes else mes_actual_pk
                primer_mes_nombre = mascota.primerMes.concepto if mascota.primerMes else "N/A"
                
                if mes.pk >= primer_mes_pk:
                    mascotas_activas_este_mes += 1
                    print(f"  {mascota.nombre}: activa desde {primer_mes_nombre} (pk={primer_mes_pk})")
            
            # Sumar el costo de las mascotas activas en este mes
            valor_mes = mascotas_activas_este_mes * valor_unitario
            print(f"Mes {mes.concepto}: {mascotas_activas_este_mes} mascotas × {valor_unitario} = {valor_mes}")
            
            valor_total += valor_mes
            cuotas_totales += mascotas_activas_este_mes
        
        print(f"TOTAL MASCOTAS: {valor_total}")
        print("===================\n")
        
        return valor_total, cuotas_totales
    
    @staticmethod
    def calcular_valores_repatriaciones(beneficiarios, repatriacion_titular, 
                                       mes_actual_pk: int, meses_pagados: List[int],
                                       incluir_saldos: bool, valor_unitario: int) -> Tuple[int, int, int]:
        """
        Calcula valores de repatriaciones separadas (beneficiarios y titular)
        Calcula mes por mes cuántas repatriaciones estaban activas
        
        Returns:
            Tuple[valor_beneficiarios, valor_titular, cuotas_totales]
        """
        if not incluir_saldos:
            # Sin saldos: contar solo las activas
            count_benef = sum(1 for b in beneficiarios if b.repatriacion)
            count_titular = 1 if repatriacion_titular else 0
            return count_benef * valor_unitario, count_titular * valor_unitario, count_benef + count_titular
        
        # Obtener todos los meses pendientes
        meses_pendientes = MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
            pk__in=CODIGOS_ESPECIALES
        ).filter(pk__lte=mes_actual_pk).order_by('pk')
        
        valor_beneficiarios = 0
        valor_titular = 0
        cuotas_benef = 0
        cuotas_titular = 0
        
        # Calcular mes por mes
        for mes in meses_pendientes:
            # Contar beneficiarios con repatriación activa en este mes
            benef_activos_este_mes = 0
            for beneficiario in beneficiarios:
                if not beneficiario.repatriacion:
                    continue
                
                primer_mes_pk = (beneficiario.primerMesRepatriacion.pk 
                               if beneficiario.primerMesRepatriacion 
                               else mes_actual_pk)
                
                if mes.pk >= primer_mes_pk:
                    benef_activos_este_mes += 1
            
            # Sumar el costo de beneficiarios activos en este mes
            if benef_activos_este_mes > 0:
                valor_beneficiarios += benef_activos_este_mes * valor_unitario
                cuotas_benef += benef_activos_este_mes
            
            # Verificar si repatriación titular estaba activa en este mes
            if repatriacion_titular:
                primer_mes_pk = (repatriacion_titular.primerMes.pk 
                               if repatriacion_titular.primerMes 
                               else mes_actual_pk)
                
                if mes.pk >= primer_mes_pk:
                    valor_titular += valor_unitario
                    cuotas_titular += 1
        
        return valor_beneficiarios, valor_titular, cuotas_benef + cuotas_titular
    
    @staticmethod
    def calcular_valores_adicionales(cuotas_vencidas: int, tarifa_asociado, 
                                     mes_actual_pk: int, meses_pagados: List[int],
                                     incluir_saldos: bool, seguro_vida_obj=None) -> Dict[str, int]:
        """
        Calcula valores vencidos de seguros, servicios adicionales y coohop
        - Para cuotaAdicionales considera primerMesCuotaAdicional si existe
        - Para seguroVida considera primerMesSeguroVida desde HistoricoSeguroVida
        """
        if cuotas_vencidas == 0:
            return {
                'seguro_vida': 0,
                'adicionales': 0,
                'coohop': 0,
            }
        
        # Coohop se calcula normal (por cuotas vencidas)
        valor_coohop = cuotas_vencidas * (
            (tarifa_asociado.cuotaCoohopAporte or 0) +
            (tarifa_asociado.cuotaCoohopBsocial or 0)
        )
        
        # Seguro de vida: calcular considerando primerMesSeguroVida
        valor_seguro_vida = 0
        
        if tarifa_asociado.cuotaSeguroVida and seguro_vida_obj:
            if not incluir_saldos:
                # Sin saldos: solo el mes actual
                valor_seguro_vida = tarifa_asociado.cuotaSeguroVida
            elif seguro_vida_obj.primerMesSeguroVida:
                # Con saldos y primerMes definido: calcular meses desde primerMes
                meses_seguro = MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
                    pk__in=CODIGOS_ESPECIALES
                ).filter(
                    pk__gte=seguro_vida_obj.primerMesSeguroVida.pk,
                    pk__lte=mes_actual_pk
                ).count()
                valor_seguro_vida = meses_seguro * tarifa_asociado.cuotaSeguroVida
            else:
                # Con saldos pero sin primerMes: usar cuotas vencidas normal
                valor_seguro_vida = cuotas_vencidas * tarifa_asociado.cuotaSeguroVida
        elif tarifa_asociado.cuotaSeguroVida:
            # Si no hay registro en HistoricoSeguroVida, usar lógica antigua
            valor_seguro_vida = cuotas_vencidas * tarifa_asociado.cuotaSeguroVida
        
        # Cuota adicional: calcular considerando primerMesCuotaAdicional
        valor_adicionales = 0
        
        if tarifa_asociado.cuotaAdicionales and tarifa_asociado.estadoAdicional:
            if not incluir_saldos:
                # Sin saldos: solo el mes actual
                valor_adicionales = tarifa_asociado.cuotaAdicionales
            elif tarifa_asociado.primerMesCuotaAdicional:
                # Con saldos y primerMes definido: calcular meses desde primerMes
                meses_adicional = MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
                    pk__in=CODIGOS_ESPECIALES
                ).filter(
                    pk__gte=tarifa_asociado.primerMesCuotaAdicional.pk,
                    pk__lte=mes_actual_pk
                ).count()
                valor_adicionales = meses_adicional * tarifa_asociado.cuotaAdicionales
            else:
                # Con saldos pero sin primerMes: usar cuotas vencidas normal
                valor_adicionales = cuotas_vencidas * tarifa_asociado.cuotaAdicionales
        
        return {
            'seguro_vida': valor_seguro_vida,
            'adicionales': valor_adicionales,
            'coohop': valor_coohop,
        }
    
    @staticmethod
    def calcular_cuota_credito_actual(credito_info: Dict) -> int:
        """
        Calcula el valor de la cuota actual de un crédito.
        Maneja casos de última cuota y pagos parciales.
        """
        pendiente = credito_info['pendiente_pago']
        cuotas_pagas = credito_info['cuotas_pagas']
        cuotas_totales = credito_info['cuotas_totales']
        valor_cuota = credito_info['valor_cuota']
        
        # Sin deuda
        if pendiente <= 0:
            return 0
        
        # Todas las cuotas pagadas pero aún hay saldo pendiente (ajuste final)
        if cuotas_pagas >= cuotas_totales:
            return pendiente
        
        # Última cuota o pendiente menor que cuota (pago parcial)
        if cuotas_pagas == cuotas_totales - 1 or pendiente < valor_cuota:
            return pendiente
        
        # Cuota normal
        return valor_cuota


class CalculadoraSaldosService:
    """Servicio para cálculos relacionados con saldos"""
    
    @staticmethod
    def calcular_pago_con_saldo(cuota_periodica: int, saldo_diferencia: int, 
                                valores_vencidos: Dict, valor_convenios: int) -> Tuple[int, int, str]:
        """
        Calcula el pago total considerando saldos a favor o en contra
        
        Returns:
            Tuple[valor_vencido, pago_total, mensaje]
        """
        valor_vencido = cuota_periodica - saldo_diferencia
        
        suma_adicionales = sum(valores_vencidos.values()) + valor_convenios
        pago_total = valor_vencido + suma_adicionales
        
        # Generar mensaje según el saldo
        if saldo_diferencia > 0:
            mensaje = f"Tiene un saldo a favor de ${saldo_diferencia:,}"
        elif saldo_diferencia < 0:
            mensaje = f"Tiene un saldo pendiente por pagar de ${abs(saldo_diferencia):,}"
        else:
            mensaje = ""
        
        return valor_vencido, pago_total, mensaje
    
    @staticmethod
    def calcular_estado_al_dia(tarifa_asociado, saldo_diferencia: int) -> Tuple[int, int, int, str]:
        """
        Calcula el estado cuando el asociado está al día
        
        Returns:
            Tuple[saldo, valor_vencido, pago_total, mensaje]
        """
        valor_mensual = (
            tarifa_asociado.cuotaAporte +
            tarifa_asociado.cuotaBSocial +
            (tarifa_asociado.cuotaMascota or 0) +
            (tarifa_asociado.cuotaRepatriacionBeneficiarios or 0) +
            (tarifa_asociado.cuotaRepatriacionTitular or 0) +
            (tarifa_asociado.cuotaSeguroVida or 0) +
            (tarifa_asociado.cuotaAdicionales or 0) +
            (tarifa_asociado.cuotaCoohopAporte or 0) +
            (tarifa_asociado.cuotaCoohopBsocial or 0) +
            (tarifa_asociado.cuotaConvenio or 0)
        )
        
        # El saldo siempre incluye la diferencia
        saldo = valor_mensual + saldo_diferencia
        
        # Determinar pago y mensaje
        if saldo == valor_mensual:
            # Sin diferencias
            return saldo, 0, 0, ""
        elif saldo > valor_mensual:
            # Saldo a favor
            dif = saldo - valor_mensual
            return saldo, 0, 0, f"Tiene un saldo a favor de ${dif:,}"
        else:
            # Saldo pendiente
            dif = valor_mensual - saldo
            return saldo, dif, dif, f"Tiene un saldo pendiente por pagar de ${dif:,}"


# ============================================================================
# 3. ORQUESTADOR PRINCIPAL
# ============================================================================

def obtenerValorExtracto(id_asociado: int, saldos: bool, mes):
    """
    Genera el extracto financiero de un asociado
    
    Args:
        id_asociado: ID del asociado
        saldos: Si True, incluye historial completo. Si False, solo mes actual
        mes: Objeto MesTarifa del mes seleccionado
    
    Returns:
        Dict con toda la información del extracto
    """
    
    # ========================================================================
    # VALIDACIONES Y DATOS BÁSICOS
    # ========================================================================
    
    try:
        parametro = ParametroAsociado.objects.select_related("primerMes").get(
            asociado=id_asociado
        )
        tarifa_asociado = TarifaAsociado.objects.select_related(
            "asociado", "asociado__mpioResidencia"
        ).get(asociado=id_asociado)
    except (ParametroAsociado.DoesNotExist, TarifaAsociado.DoesNotExist):
        raise ValueError(f"No se encontró información para el asociado {id_asociado}")
    
    # Validar que el mes seleccionado sea válido
    if mes.pk < parametro.primerMes.pk:
        raise ValueError(
            f"El mes seleccionado ({mes.concepto}) es anterior al primer mes "
            f"de vinculación ({parametro.primerMes.concepto})"
        )
    
    # Calcular fecha de corte
    fecha_corte = mes.fechaInicio + timedelta(days=15)
    
    # Cuotas básicas
    cuota_periodica = CalculadoraCuotasService.calcular_cuota_periodica(tarifa_asociado)
    cuota_coohop = CalculadoraCuotasService.calcular_cuota_coohop(tarifa_asociado)
    
    # ========================================================================
    # CONSULTAR INFORMACIÓN DE PAGOS
    # ========================================================================
    
    meses_pagados = ConsultaPagosService.obtener_meses_pagados(id_asociado)
    meses_pendientes = ConsultaPagosService.obtener_meses_pendientes(
        id_asociado, parametro.primerMes.pk, mes.pk, meses_pagados
    )
    
    # ========================================================================
    # CALCULAR CUOTAS VENCIDAS Y ADELANTADAS
    # ========================================================================
    
    cuotas_vencidas, cuota_periodica_total = CalculadoraCuotasService.calcular_cuotas_vencidas_y_total(
        meses_pendientes, saldos
    )
    cuotas_adelantadas = CalculadoraCuotasService.calcular_cuotas_adelantadas(
        meses_pagados, mes.pk
    )
    
    # ========================================================================
    # CALCULAR SALDO DE DIFERENCIAS
    # ========================================================================
    
    saldo_diferencia = 0
    if saldos:
        saldo_diferencia = ConsultaPagosService.calcular_saldo_diferencia(id_asociado)
    
    # ========================================================================
    # OBTENER BENEFICIARIOS, MASCOTAS, REPATRIACIONES Y SEGURO DE VIDA
    # ========================================================================
    
    beneficiarios = ConsultaBeneficiariosService.obtener_beneficiarios_activos(id_asociado)
    mascotas = ConsultaBeneficiariosService.obtener_mascotas_activas(id_asociado)
    repatriacion_titular = ConsultaBeneficiariosService.obtener_repatriacion_titular(id_asociado)
    seguro_vida = ConsultaBeneficiariosService.obtener_seguro_vida_activo(id_asociado)
    
    # ========================================================================
    # CALCULAR VALORES DE MASCOTAS Y REPATRIACIONES (CON PRIMER MES)
    # ========================================================================
    
    # Valor unitario de mascota (dividir entre cantidad actual)
    cantidad_mascotas_actuales = mascotas.count()
    valor_unitario_mascota = (
        (tarifa_asociado.cuotaMascota or 0) // cantidad_mascotas_actuales 
        if cantidad_mascotas_actuales > 0 
        else 5500  # Valor por defecto si no hay mascotas
    )
    
    print(f"\n=== CÁLCULO VALOR UNITARIO MASCOTA ===")
    print(f"Total en tarifa: {tarifa_asociado.cuotaMascota}")
    print(f"Cantidad mascotas actuales: {cantidad_mascotas_actuales}")
    print(f"Valor unitario calculado: {valor_unitario_mascota}")
    print("=====================================\n")
    
    valor_mascotas, cuotas_mascotas = CalculadoraCuotasService.calcular_valores_mascotas(
        mascotas, mes.pk, meses_pagados, saldos, valor_unitario_mascota
    )
    
    # Valor unitario de repatriación (calculado dividiendo entre cantidad actual)
    # Para compatibilidad, usamos el valor total en tarifa si existe
    total_repatriaciones_tarifa = (
        (tarifa_asociado.cuotaRepatriacionBeneficiarios or 0) +
        (tarifa_asociado.cuotaRepatriacionTitular or 0)
    )
    
    # Si no hay separación, usar el campo antiguo
    if total_repatriaciones_tarifa == 0 and tarifa_asociado.cuotaRepatriacion:
        total_repatriaciones_tarifa = tarifa_asociado.cuotaRepatriacion
    
    # Calcular valor unitario
    cantidad_repatriaciones_activas = (
        sum(1 for b in beneficiarios if b.repatriacion) +
        (1 if repatriacion_titular else 0)
    )
    
    valor_unitario_repatriacion = (
        total_repatriaciones_tarifa // cantidad_repatriaciones_activas 
        if cantidad_repatriaciones_activas > 0 
        else 10500  # Valor por defecto
    )
    
    valor_rep_benef, valor_rep_titular, cuotas_repatriaciones = (
        CalculadoraCuotasService.calcular_valores_repatriaciones(
            beneficiarios, repatriacion_titular, mes.pk, meses_pagados, 
            saldos, valor_unitario_repatriacion
        )
    )
    
    # Total de repatriaciones
    valor_repatriaciones_total = valor_rep_benef + valor_rep_titular
    
    # ========================================================================
    # CALCULAR VALORES ADICIONALES
    # ========================================================================
    
    valores_adicionales = CalculadoraCuotasService.calcular_valores_adicionales(
        cuotas_vencidas, tarifa_asociado, mes.pk, meses_pagados, saldos, seguro_vida
    )
    
    # ========================================================================
    # PROCESAR CONVENIOS (SEPARANDO GASOLINA)
    # ========================================================================
    
    convenios_normales, tiene_gasolina = ConsultaConveniosService.obtener_convenios_activos_separados(
        id_asociado, mes.pk
    )
    
    valor_convenios_normales = 0
    
    for convenio in convenios_normales:
        if saldos:
            meses_pendientes_convenio = ConsultaConveniosService.calcular_meses_pendientes_convenio(
                convenio, mes.pk, meses_pagados
            )
        else:
            meses_pendientes_convenio = 1 if cuotas_vencidas > 0 else 0
        
        convenio.cantidad_meses = meses_pendientes_convenio
        convenio.valor_vencido_convenio = convenio.convenio.valor * meses_pendientes_convenio
        valor_convenios_normales += convenio.valor_vencido_convenio
    
    # Convenio de gasolina (total acumulado)
    valor_gasolina = 0
    convenio_gasolina_info = None
    
    if tiene_gasolina:
        valor_gasolina = ConsultaConveniosService.obtener_total_gasolina(id_asociado)
        convenio_gasolina_info = {
            'activo': True,
            'concepto': 'CHIP GASOLINA',
            'pendiente_total': valor_gasolina,
        }
    
    valor_total_convenios = valor_convenios_normales + valor_gasolina
    
    # ========================================================================
    # PROCESAR CRÉDITOS
    # ========================================================================
    
    creditos_info = ConsultaCreditosService.obtener_creditos_activos(id_asociado)
    ventas_home_info = ConsultaCreditosService.obtener_ventas_home_elements_activas(id_asociado)
    
    # Calcular cuotas actuales de créditos
    valor_total_creditos = 0
    for credito in creditos_info:
        credito['cuota_actual'] = CalculadoraCuotasService.calcular_cuota_credito_actual(credito)
        credito['progreso'] = f"{credito['cuotas_pagas']}/{credito['cuotas_totales']}"
        valor_total_creditos += credito['cuota_actual']
    
    for venta in ventas_home_info:
        venta['cuota_actual'] = CalculadoraCuotasService.calcular_cuota_credito_actual(venta)
        venta['progreso'] = f"{venta['cuotas_pagas']}/{venta['cuotas_totales']}"
        valor_total_creditos += venta['cuota_actual']
    
    # ========================================================================
    # CALCULAR TOTALES SEGÚN ESTADO
    # ========================================================================
    
    # Consolidar todos los valores vencidos
    valores_vencidos_consolidados = {
        'mascota': valor_mascotas,
        'repatriacion': valor_repatriaciones_total,
        'seguro_vida': valores_adicionales['seguro_vida'],
        'adicionales': valores_adicionales['adicionales'],
        'coohop': valores_adicionales['coohop'],
    }
    
    # Inicializar variables del context
    saldo = 0
    valor_vencido = 0
    pago_total = 0
    mensaje = ""
    
    # CASO 1: Tiene cuotas vencidas
    if cuotas_vencidas > 0:
        valor_vencido, pago_total, mensaje = CalculadoraSaldosService.calcular_pago_con_saldo(
            cuota_periodica_total,
            saldo_diferencia,
            valores_vencidos_consolidados,
            valor_total_convenios
        )
        # Agregar créditos al pago total
        pago_total += valor_total_creditos
    
    # CASO 2: Está al día (sin cuotas vencidas ni adelantadas)
    elif cuotas_adelantadas == 0:
        saldo, valor_vencido, pago_total, mensaje = CalculadoraSaldosService.calcular_estado_al_dia(
            tarifa_asociado, saldo_diferencia
        )
        # Agregar créditos al pago total
        pago_total += valor_total_creditos
    
    # CASO 3: Tiene pagos adelantados
    else:
        saldo_actual = ConsultaPagosService.obtener_saldo_adelantado(id_asociado, mes.pk)
        saldo = saldo_actual + saldo_diferencia
        pago_total = 0  # No debe nada este mes
        
        ultimo_pago = ConsultaPagosService.obtener_ultimo_mes_pagado(id_asociado)
        if ultimo_pago:
            mensaje = f"Tiene pago hasta el mes de {ultimo_pago.mesPago.concepto}"
    
    # ========================================================================
    # CONSTRUIR Y RETORNAR CONTEXT
    # ========================================================================
    
    context = {
        # Información básica
        "pkAsociado": id_asociado,
        "fechaCorte": fecha_corte,
        "mes": mes,
        
        # Tarifa del asociado
        "objTarifaAsociado": tarifa_asociado,
        "cuotaPeriodica": cuota_periodica,
        "cuotaCoohop": cuota_coohop,
        
        # Cuotas y valores vencidos
        "cuotaVencida": cuotas_vencidas,
        "valorVencido": valor_vencido,
        "valorVencidoMasc": valor_mascotas,
        "valorVencidoRep": valor_repatriaciones_total,
        "valorVencidoRepBeneficiarios": valor_rep_benef,
        "valorVencidoRepTitular": valor_rep_titular,
        "valorVencidoSeg": valores_adicionales['seguro_vida'],
        "valorVencidoAdic": valores_adicionales['adicionales'],
        "valorVencidoCoohop": valores_adicionales['coohop'],
        "valorVencidoConvenio": valor_total_convenios,
        "valorVencidoConveniosNormales": valor_convenios_normales,
        "valorVencidoGasolina": valor_gasolina,
        
        # Créditos (NUEVA FUNCIONALIDAD)
        "creditos": creditos_info,
        "ventasHomeElements": ventas_home_info,
        "valorTotalCreditos": valor_total_creditos,
        
        # Totales
        "pagoTotal": pago_total,
        "saldo": saldo,
        "mensaje": mensaje,
        
        # Beneficiarios y mascotas (con información extendida)
        "objBeneficiario": beneficiarios,
        "cuentaBeneficiario": beneficiarios.count(),
        "cuentaBeneficiarioConRepatriacion": sum(1 for b in beneficiarios if b.repatriacion),
        "objMascota": mascotas,
        "cuentaMascota": mascotas.count(),
        "objRepatriacionTitular": repatriacion_titular,
        "objSeguroVida": seguro_vida,
        
        # Convenios (separados)
        "objConvenio": convenios_normales,
        "convenioGasolina": convenio_gasolina_info,
        
        # Vista (mantener compatibilidad)
        "vista": 0,
    }
    
    return context