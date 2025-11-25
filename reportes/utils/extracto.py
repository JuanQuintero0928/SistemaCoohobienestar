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
    RepatriacionTitular,
)
from beneficiario.models import Beneficiario, Mascota
from historico.models import HistorialPagos, HistoricoCredito, HistoricoSeguroVida
from parametro.models import MesTarifa
from ventas.models import HistoricoVenta

# """
# Refactorización del sistema de extractos financieros
# Versión 2.0 - Con soporte para primerMes en mascotas, repatriaciones y convenio gasolina
# """
# from django.db.models import Sum, Count, Q, Max
# from datetime import timedelta
# from typing import Dict, List, Tuple, Optional


# # ============================================================================
# # CONSTANTES
# # ============================================================================
# CODIGOS_ESPECIALES = [9999, 9998, 9997, 9996, 9995, 9994, 9993, 9992, 9991, 9990, 9989]

# CODIGO_ABONO = 9999
# CODIGO_CREDITO_HOME = 9998
# CODIGO_CREDITO_LIBRE = 9993

# CONVENIO_GASOLINA_ID = 4  # ID del convenio de gasolina


# # ============================================================================
# # 1. SERVICIOS DE CONSULTA (Queries reutilizables)
# # ============================================================================

# class ConsultaPagosService:
#     """Servicio para consultas relacionadas con pagos"""
    
#     @staticmethod
#     def obtener_meses_pagados(id_asociado: int) -> List[int]:
#         """Obtiene los IDs de los meses que ya fueron pagados"""
#         return list(
#             HistorialPagos.objects.filter(asociado=id_asociado, estadoRegistro=True)
#             .exclude(mesPago__in=CODIGOS_ESPECIALES)
#             .values_list("mesPago", flat=True)
#         )
    
#     @staticmethod
#     def obtener_meses_pendientes(id_asociado: int, mes_inicio_pk: int, mes_fin_pk: int, meses_pagados: List[int]):
#         """Obtiene los meses pendientes de pago en un rango"""
#         return MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
#             pk__in=CODIGOS_ESPECIALES
#         ).filter(pk__gte=mes_inicio_pk, pk__lte=mes_fin_pk)
    
#     @staticmethod
#     def calcular_saldo_diferencia(id_asociado: int) -> int:
#         """Calcula el saldo total de diferencias (positivo=favor, negativo=debe, 0=al día)"""
#         resultado = HistorialPagos.objects.filter(
#             asociado=id_asociado, estadoRegistro=True
#         ).aggregate(total=Sum("diferencia"))
#         return resultado["total"] or 0
    
#     @staticmethod
#     def obtener_saldo_adelantado(id_asociado: int, mes_pk: int) -> int:
#         """Calcula el saldo de pagos adelantados desde un mes específico"""
#         resultado = (
#             HistorialPagos.objects.exclude(mesPago__in=CODIGOS_ESPECIALES)
#             .filter(mesPago__gte=mes_pk, asociado=id_asociado, estadoRegistro=True)
#             .aggregate(total=Sum("valorPago"))
#         )
#         return resultado["total"] or 0
    
#     @staticmethod
#     def obtener_ultimo_mes_pagado(id_asociado: int):
#         """Obtiene el último mes pagado por el asociado"""
#         max_mes_pk = (
#             HistorialPagos.objects.exclude(mesPago__in=CODIGOS_ESPECIALES)
#             .filter(asociado=id_asociado, estadoRegistro=True)
#             .aggregate(max_mes=Max("mesPago"))["max_mes"]
#         )
        
#         if max_mes_pk:
#             return HistorialPagos.objects.filter(
#                 mesPago=max_mes_pk, asociado=id_asociado, estadoRegistro=True
#             ).first()
#         return None


# class ConsultaCreditosService:
#     """Servicio para consultas relacionadas con créditos"""
    
#     @staticmethod
#     def obtener_creditos_activos(id_asociado: int) -> List[Dict]:
#         """Obtiene todos los créditos activos con saldo pendiente"""
#         creditos = HistoricoCredito.objects.filter(
#             asociado=id_asociado,
#             estadoRegistro=True,
#             estado="OTORGADO",
#             pendientePago__gt=0
#         ).select_related('tasaInteres', 'primerMes')
        
#         return [
#             {
#                 'id': credito.id,
#                 'tipo': 'CREDITO LIBRE INVERSION',
#                 'linea': credito.lineaCredito,
#                 'valor_cuota': credito.valorCuota,
#                 'cuotas_totales': credito.cuotas,
#                 'cuotas_pagas': credito.cuotasPagas or 0,
#                 'pendiente_pago': credito.pendientePago,
#                 'total_credito': credito.totalCredito,
#                 'primer_mes': credito.primerMes,  # ← NUEVO
#             }
#             for credito in creditos
#         ]
    
#     @staticmethod
#     def obtener_ventas_home_elements_activas(id_asociado: int) -> List[Dict]:
#         """Obtiene todas las ventas de home elements con saldo pendiente"""
#         ventas = HistoricoVenta.objects.filter(
#             asociado=id_asociado,
#             estadoRegistro=True,
#             formaPago__in=['CREDITO', 'DESCUENTO NOMINA'],
#             pendientePago__gt=0
#         ).select_related('tasaInteres', 'descuento', 'primerMes')
        
#         return [
#             {
#                 'id': venta.id,
#                 'tipo': 'CREDITO HOME ELEMENTS',
#                 'valor_cuota': venta.valorCuotas,
#                 'cuotas_totales': venta.cuotas,
#                 'cuotas_pagas': venta.cuotasPagas or 0,
#                 'pendiente_pago': venta.pendientePago,
#                 'total_venta': venta.valorNeto,
#                 'primer_mes': venta.primerMes,  # ← NUEVO
#             }
#             for venta in ventas
#         ]


# class ConsultaConveniosService:
#     """Servicio para consultas relacionadas con convenios"""
    
#     @staticmethod
#     def obtener_convenios_activos_separados(id_asociado: int, mes_pk: int) -> Tuple[List, bool]:
#         """
#         Obtiene convenios activos separando gasolina de los demás
        
#         Returns:
#             Tuple[convenios_normales, tiene_gasolina]
#         """
#         convenios_todos = ConveniosAsociado.objects.select_related("convenio").filter(
#             asociado=id_asociado,
#             estadoRegistro=True,
#             primerMes__lte=mes_pk
#         )
        
#         convenios_normales = []
#         tiene_gasolina = False
        
#         for conv in convenios_todos:
#             if conv.convenio.id == CONVENIO_GASOLINA_ID:
#                 tiene_gasolina = True
#             else:
#                 convenios_normales.append(conv)
        
#         return convenios_normales, tiene_gasolina
    
#     @staticmethod
#     def calcular_meses_pendientes_convenio(convenio, mes_fin_pk: int, meses_pagados: List[int]) -> int:
#         """Calcula cuántos meses debe un convenio específico"""
#         meses_faltantes = (
#             MesTarifa.objects.exclude(pk__in=meses_pagados)
#             .exclude(pk__in=CODIGOS_ESPECIALES)
#             .filter(pk__gte=convenio.primerMes.pk, pk__lte=mes_fin_pk)
#         )
#         return meses_faltantes.count()
    
#     @staticmethod
#     def obtener_total_gasolina(id_asociado: int) -> int:
#         """Obtiene el total pendiente de pago del convenio de gasolina"""
#         total = ConvenioHistoricoGasolina.objects.filter(
#             asociado=id_asociado,
#             estado_registro=True
#         ).aggregate(total=Sum('pendiente_pago'))
#         return total['total'] or 0


# class ConsultaBeneficiariosService:
#     """Servicio para consultas de beneficiarios y servicios asociados"""
    
#     @staticmethod
#     def obtener_beneficiarios_activos(id_asociado: int):
#         """Obtiene beneficiarios activos con información de repatriación"""
#         return Beneficiario.objects.filter(
#             asociado=id_asociado, 
#             estadoRegistro=True
#         ).select_related("parentesco", "paisRepatriacion", "primerMesRepatriacion")
    
#     @staticmethod
#     def obtener_mascotas_activas(id_asociado: int):
#         """Obtiene mascotas activas"""
#         return Mascota.objects.filter(
#             asociado=id_asociado, 
#             estadoRegistro=True
#         ).select_related("primerMes")
    
#     @staticmethod
#     def obtener_repatriacion_titular(id_asociado: int):
#         """Obtiene la repatriación del titular si existe"""
#         return RepatriacionTitular.objects.filter(
#             asociado=id_asociado,
#             estadoRegistro=True
#         ).select_related("primerMes", "paisRepatriacion").first()
    
#     @staticmethod
#     def obtener_seguro_vida_activo(id_asociado: int):
#         """Obtiene el seguro de vida activo del asociado si existe"""
#         return HistoricoSeguroVida.objects.filter(
#             asociado=id_asociado,
#             estadoRegistro=True
#         ).select_related("primerMesSeguroVida").first()


# # ============================================================================
# # 2. SERVICIOS DE CÁLCULO (Funciones puras)
# # ============================================================================

# class CalculadoraCuotasService:
#     """Servicio para calcular cuotas y valores"""
    
#     @staticmethod
#     def calcular_cuota_periodica(tarifa_asociado) -> int:
#         """Calcula la cuota periódica base (aporte + bienestar social)"""
#         return tarifa_asociado.cuotaAporte + tarifa_asociado.cuotaBSocial
    
#     @staticmethod
#     def calcular_cuota_coohop(tarifa_asociado) -> int:
#         """Calcula la cuota de Coohoperativitos"""
#         return (
#             (tarifa_asociado.cuotaCoohopAporte or 0) + 
#             (tarifa_asociado.cuotaCoohopBsocial or 0)
#         )
    
#     @staticmethod
#     def calcular_cuotas_vencidas_y_total(meses_faltantes, incluir_saldos: bool) -> Tuple[int, int]:
#         """
#         Calcula cantidad de cuotas vencidas y el total adeudado
        
#         Returns:
#             Tuple[cuotas_vencidas, cuota_periodica_total]
#         """
#         if not incluir_saldos:
#             # Sin saldos: solo el mes seleccionado
#             if meses_faltantes.exists():
#                 mes = meses_faltantes.first()
#                 return 1, mes.aporte + mes.bSocial
#             return 0, 0
        
#         # Con saldos: sumar todos los meses pendientes
#         cuotas_vencidas = meses_faltantes.count()
#         cuota_total = sum(mes.aporte + mes.bSocial for mes in meses_faltantes)
#         return cuotas_vencidas, cuota_total
    
#     @staticmethod
#     def calcular_cuotas_adelantadas(meses_pagados: List[int], mes_actual_pk: int) -> int:
#         """Cuenta cuántas cuotas están adelantadas respecto al mes actual"""
#         return sum(1 for mes_pk in meses_pagados if mes_pk > mes_actual_pk)
    
#     @staticmethod
#     def calcular_meses_vencidos_servicio(primer_mes_pk: int, mes_actual_pk: int, meses_pagados: List[int]) -> int:
#         """
#         Calcula cuántos meses debe un servicio específico (mascota, repatriación)
#         considerando su primerMes
#         """
#         if not primer_mes_pk:
#             return 0
        
#         meses_pendientes = (
#             MesTarifa.objects.exclude(pk__in=meses_pagados)
#             .exclude(pk__in=CODIGOS_ESPECIALES)
#             .filter(pk__gte=primer_mes_pk, pk__lte=mes_actual_pk)
#         )
#         return meses_pendientes.count()
    
#     @staticmethod
#     def calcular_valores_mascotas(mascotas, mes_actual_pk: int, meses_pagados: List[int], 
#                                   incluir_saldos: bool, valor_unitario: int) -> Tuple[int, int]:
#         """
#         Calcula el valor vencido de mascotas considerando primerMes individual
#         Calcula mes por mes cuántas mascotas estaban activas
        
#         Returns:
#             Tuple[valor_vencido_mascotas, cantidad_cuotas_totales]
#         """
#         if not incluir_saldos:
#             # Sin saldos: solo cuenta las mascotas activas en el mes actual
#             return len(mascotas) * valor_unitario, len(mascotas) if mascotas else 0
        
#         # Obtener todos los meses pendientes
#         meses_pendientes = MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
#             pk__in=CODIGOS_ESPECIALES
#         ).filter(pk__lte=mes_actual_pk).order_by('pk')
        
#         valor_total = 0
#         cuotas_totales = 0
        
#         # DEBUG: Imprimir información
#         print("\n=== DEBUG MASCOTAS ===")
#         print(f"Total mascotas: {len(mascotas)}")
#         print(f"Valor unitario: {valor_unitario}")
#         print(f"Meses pendientes: {[m.concepto for m in meses_pendientes]}")
        
#         # Calcular mes por mes cuántas mascotas estaban activas
#         for mes in meses_pendientes:
#             mascotas_activas_este_mes = 0
            
#             for mascota in mascotas:
#                 # Verificar si la mascota ya estaba activa en este mes
#                 primer_mes_pk = mascota.primerMes.pk if mascota.primerMes else mes_actual_pk
#                 primer_mes_nombre = mascota.primerMes.concepto if mascota.primerMes else "N/A"
                
#                 if mes.pk >= primer_mes_pk:
#                     mascotas_activas_este_mes += 1
#                     print(f"  {mascota.nombre}: activa desde {primer_mes_nombre} (pk={primer_mes_pk})")
            
#             # Sumar el costo de las mascotas activas en este mes
#             valor_mes = mascotas_activas_este_mes * valor_unitario
#             print(f"Mes {mes.concepto}: {mascotas_activas_este_mes} mascotas × {valor_unitario} = {valor_mes}")
            
#             valor_total += valor_mes
#             cuotas_totales += mascotas_activas_este_mes
        
#         print(f"TOTAL MASCOTAS: {valor_total}")
#         print("===================\n")
        
#         return valor_total, cuotas_totales
    
#     @staticmethod
#     def calcular_valores_repatriaciones(beneficiarios, repatriacion_titular, 
#                                        mes_actual_pk: int, meses_pagados: List[int],
#                                        incluir_saldos: bool, valor_unitario: int) -> Tuple[int, int, int]:
#         """
#         Calcula valores de repatriaciones separadas (beneficiarios y titular)
#         Calcula mes por mes cuántas repatriaciones estaban activas
        
#         Returns:
#             Tuple[valor_beneficiarios, valor_titular, cuotas_totales]
#         """
#         if not incluir_saldos:
#             # Sin saldos: contar solo las activas
#             count_benef = sum(1 for b in beneficiarios if b.repatriacion)
#             count_titular = 1 if repatriacion_titular else 0
#             return count_benef * valor_unitario, count_titular * valor_unitario, count_benef + count_titular
        
#         # Obtener todos los meses pendientes
#         meses_pendientes = MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
#             pk__in=CODIGOS_ESPECIALES
#         ).filter(pk__lte=mes_actual_pk).order_by('pk')
        
#         valor_beneficiarios = 0
#         valor_titular = 0
#         cuotas_benef = 0
#         cuotas_titular = 0
        
#         # Calcular mes por mes
#         for mes in meses_pendientes:
#             # Contar beneficiarios con repatriación activa en este mes
#             benef_activos_este_mes = 0
#             for beneficiario in beneficiarios:
#                 if not beneficiario.repatriacion:
#                     continue
                
#                 primer_mes_pk = (beneficiario.primerMesRepatriacion.pk 
#                                if beneficiario.primerMesRepatriacion 
#                                else mes_actual_pk)
                
#                 if mes.pk >= primer_mes_pk:
#                     benef_activos_este_mes += 1
            
#             # Sumar el costo de beneficiarios activos en este mes
#             if benef_activos_este_mes > 0:
#                 valor_beneficiarios += benef_activos_este_mes * valor_unitario
#                 cuotas_benef += benef_activos_este_mes
            
#             # Verificar si repatriación titular estaba activa en este mes
#             if repatriacion_titular:
#                 primer_mes_pk = (repatriacion_titular.primerMes.pk 
#                                if repatriacion_titular.primerMes 
#                                else mes_actual_pk)
                
#                 if mes.pk >= primer_mes_pk:
#                     valor_titular += valor_unitario
#                     cuotas_titular += 1
        
#         return valor_beneficiarios, valor_titular, cuotas_benef + cuotas_titular
    
#     @staticmethod
#     def calcular_valores_adicionales(cuotas_vencidas: int, tarifa_asociado, 
#                                      mes_actual_pk: int, meses_pagados: List[int],
#                                      incluir_saldos: bool, seguro_vida_obj=None) -> Dict[str, int]:
#         """
#         Calcula valores vencidos de seguros, servicios adicionales y coohop
#         - Para cuotaAdicionales considera primerMesCuotaAdicional si existe
#         - Para seguroVida considera primerMesSeguroVida desde HistoricoSeguroVida
#         """
#         if cuotas_vencidas == 0:
#             return {
#                 'seguro_vida': 0,
#                 'adicionales': 0,
#                 'coohop': 0,
#             }
        
#         # Coohop se calcula normal (por cuotas vencidas)
#         valor_coohop = cuotas_vencidas * (
#             (tarifa_asociado.cuotaCoohopAporte or 0) +
#             (tarifa_asociado.cuotaCoohopBsocial or 0)
#         )
        
#         # Seguro de vida: calcular considerando primerMesSeguroVida
#         valor_seguro_vida = 0
        
#         if tarifa_asociado.cuotaSeguroVida and seguro_vida_obj:
#             if not incluir_saldos:
#                 # Sin saldos: solo el mes actual
#                 valor_seguro_vida = tarifa_asociado.cuotaSeguroVida
#             elif seguro_vida_obj.primerMesSeguroVida:
#                 # Con saldos y primerMes definido: calcular meses desde primerMes
#                 meses_seguro = MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
#                     pk__in=CODIGOS_ESPECIALES
#                 ).filter(
#                     pk__gte=seguro_vida_obj.primerMesSeguroVida.pk,
#                     pk__lte=mes_actual_pk
#                 ).count()
#                 valor_seguro_vida = meses_seguro * tarifa_asociado.cuotaSeguroVida
#             else:
#                 # Con saldos pero sin primerMes: usar cuotas vencidas normal
#                 valor_seguro_vida = cuotas_vencidas * tarifa_asociado.cuotaSeguroVida
#         elif tarifa_asociado.cuotaSeguroVida:
#             # Si no hay registro en HistoricoSeguroVida, usar lógica antigua
#             valor_seguro_vida = cuotas_vencidas * tarifa_asociado.cuotaSeguroVida
        
#         # Cuota adicional: calcular considerando primerMesCuotaAdicional
#         valor_adicionales = 0
        
#         if tarifa_asociado.cuotaAdicionales and tarifa_asociado.estadoAdicional:
#             if not incluir_saldos:
#                 # Sin saldos: solo el mes actual
#                 valor_adicionales = tarifa_asociado.cuotaAdicionales
#             elif tarifa_asociado.primerMesCuotaAdicional:
#                 # Con saldos y primerMes definido: calcular meses desde primerMes
#                 meses_adicional = MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
#                     pk__in=CODIGOS_ESPECIALES
#                 ).filter(
#                     pk__gte=tarifa_asociado.primerMesCuotaAdicional.pk,
#                     pk__lte=mes_actual_pk
#                 ).count()
#                 valor_adicionales = meses_adicional * tarifa_asociado.cuotaAdicionales
#             else:
#                 # Con saldos pero sin primerMes: usar cuotas vencidas normal
#                 valor_adicionales = cuotas_vencidas * tarifa_asociado.cuotaAdicionales
        
#         return {
#             'seguro_vida': valor_seguro_vida,
#             'adicionales': valor_adicionales,
#             'coohop': valor_coohop,
#         }
    
#     @staticmethod
#     def calcular_cuota_credito_actual(credito_info: Dict, mes_actual_pk: int) -> int:
#         """
#         Calcula el valor de la cuota actual de un crédito.
#         Maneja casos de última cuota, pagos parciales y primerMes futuro.
#         """
#         pendiente = credito_info['pendiente_pago']
#         cuotas_pagas = credito_info['cuotas_pagas']
#         cuotas_totales = credito_info['cuotas_totales']
#         valor_cuota = credito_info['valor_cuota']
#         primer_mes = credito_info.get('primer_mes')
        
#         # Si tiene primerMes y aún no ha llegado ese mes, retornar 0
#         if primer_mes and primer_mes.pk > mes_actual_pk:
#             return 0
        
#         # Sin deuda
#         if pendiente <= 0:
#             return 0
        
#         # Todas las cuotas pagadas pero aún hay saldo pendiente (ajuste final)
#         if cuotas_pagas >= cuotas_totales:
#             return pendiente
        
#         # Última cuota o pendiente menor que cuota (pago parcial)
#         if cuotas_pagas == cuotas_totales - 1 or pendiente < valor_cuota:
#             return pendiente
        
#         # Cuota normal
#         return valor_cuota


# class CalculadoraSaldosService:
#     """Servicio para cálculos relacionados con saldos"""
    
#     @staticmethod
#     def calcular_pago_con_saldo(cuota_periodica: int, saldo_diferencia: int, 
#                                 valores_vencidos: Dict, valor_convenios: int) -> Tuple[int, int, str]:
#         """
#         Calcula el pago total considerando saldos a favor o en contra
        
#         Returns:
#             Tuple[valor_vencido, pago_total, mensaje]
#         """
#         valor_vencido = cuota_periodica - saldo_diferencia
        
#         suma_adicionales = sum(valores_vencidos.values()) + valor_convenios
#         pago_total = valor_vencido + suma_adicionales
        
#         # Generar mensaje según el saldo
#         if saldo_diferencia > 0:
#             mensaje = f"Tiene un saldo a favor de ${saldo_diferencia:,}"
#         elif saldo_diferencia < 0:
#             mensaje = f"Tiene un saldo pendiente por pagar de ${abs(saldo_diferencia):,}"
#         else:
#             mensaje = ""
        
#         return valor_vencido, pago_total, mensaje
    
#     @staticmethod
#     def calcular_estado_al_dia(tarifa_asociado, saldo_diferencia: int) -> Tuple[int, int, int, str]:
#         """
#         Calcula el estado cuando el asociado está al día
        
#         Returns:
#             Tuple[saldo, valor_vencido, pago_total, mensaje]
#         """
#         valor_mensual = (
#             tarifa_asociado.cuotaAporte +
#             tarifa_asociado.cuotaBSocial +
#             (tarifa_asociado.cuotaMascota or 0) +
#             (tarifa_asociado.cuotaRepatriacionBeneficiarios or 0) +
#             (tarifa_asociado.cuotaRepatriacionTitular or 0) +
#             (tarifa_asociado.cuotaSeguroVida or 0) +
#             (tarifa_asociado.cuotaAdicionales or 0) +
#             (tarifa_asociado.cuotaCoohopAporte or 0) +
#             (tarifa_asociado.cuotaCoohopBsocial or 0) +
#             (tarifa_asociado.cuotaConvenio or 0)
#         )
        
#         # El saldo siempre incluye la diferencia
#         saldo = valor_mensual + saldo_diferencia
        
#         # Determinar pago y mensaje
#         if saldo == valor_mensual:
#             # Sin diferencias
#             return saldo, 0, 0, ""
#         elif saldo > valor_mensual:
#             # Saldo a favor
#             dif = saldo - valor_mensual
#             return saldo, 0, 0, f"Tiene un saldo a favor de ${dif:,}"
#         else:
#             # Saldo pendiente
#             dif = valor_mensual - saldo
#             return saldo, dif, dif, f"Tiene un saldo pendiente por pagar de ${dif:,}"


# # ============================================================================
# # 3. ORQUESTADOR PRINCIPAL
# # ============================================================================

# def obtenerValorExtracto(id_asociado: int, saldos: bool, mes):
#     """
#     Genera el extracto financiero de un asociado
    
#     Args:
#         id_asociado: ID del asociado
#         saldos: Si True, incluye historial completo. Si False, solo mes actual
#         mes: Objeto MesTarifa del mes seleccionado
    
#     Returns:
#         Dict con toda la información del extracto
#     """
    
#     # ========================================================================
#     # VALIDACIONES Y DATOS BÁSICOS
#     # ========================================================================
    
#     try:
#         parametro = ParametroAsociado.objects.select_related("primerMes").get(
#             asociado=id_asociado
#         )
#         tarifa_asociado = TarifaAsociado.objects.select_related(
#             "asociado", "asociado__mpioResidencia"
#         ).get(asociado=id_asociado)
#     except (ParametroAsociado.DoesNotExist, TarifaAsociado.DoesNotExist):
#         raise ValueError(f"No se encontró información para el asociado {id_asociado}")
    
#     # Validar que el mes seleccionado sea válido
#     if mes.pk < parametro.primerMes.pk:
#         raise ValueError(
#             f"El mes seleccionado ({mes.concepto}) es anterior al primer mes "
#             f"de vinculación ({parametro.primerMes.concepto})"
#         )
    
#     # Calcular fecha de corte
#     fecha_corte = mes.fechaInicio + timedelta(days=15)
    
#     # Cuotas básicas
#     cuota_periodica = CalculadoraCuotasService.calcular_cuota_periodica(tarifa_asociado)
#     cuota_coohop = CalculadoraCuotasService.calcular_cuota_coohop(tarifa_asociado)
    
#     # ========================================================================
#     # CONSULTAR INFORMACIÓN DE PAGOS
#     # ========================================================================
    
#     meses_pagados = ConsultaPagosService.obtener_meses_pagados(id_asociado)
#     meses_pendientes = ConsultaPagosService.obtener_meses_pendientes(
#         id_asociado, parametro.primerMes.pk, mes.pk, meses_pagados
#     )
    
#     # ========================================================================
#     # CALCULAR CUOTAS VENCIDAS Y ADELANTADAS
#     # ========================================================================
    
#     cuotas_vencidas, cuota_periodica_total = CalculadoraCuotasService.calcular_cuotas_vencidas_y_total(
#         meses_pendientes, saldos
#     )
#     cuotas_adelantadas = CalculadoraCuotasService.calcular_cuotas_adelantadas(
#         meses_pagados, mes.pk
#     )
    
#     # ========================================================================
#     # CALCULAR SALDO DE DIFERENCIAS
#     # ========================================================================
    
#     saldo_diferencia = 0
#     if saldos:
#         saldo_diferencia = ConsultaPagosService.calcular_saldo_diferencia(id_asociado)
    
#     # ========================================================================
#     # OBTENER BENEFICIARIOS, MASCOTAS, REPATRIACIONES Y SEGURO DE VIDA
#     # ========================================================================
    
#     beneficiarios = ConsultaBeneficiariosService.obtener_beneficiarios_activos(id_asociado)
#     mascotas = ConsultaBeneficiariosService.obtener_mascotas_activas(id_asociado)
#     repatriacion_titular = ConsultaBeneficiariosService.obtener_repatriacion_titular(id_asociado)
#     seguro_vida = ConsultaBeneficiariosService.obtener_seguro_vida_activo(id_asociado)
    
#     # ========================================================================
#     # CALCULAR VALORES DE MASCOTAS Y REPATRIACIONES (CON PRIMER MES)
#     # ========================================================================
    
#     # Valor unitario de mascota (dividir entre cantidad actual)
#     cantidad_mascotas_actuales = mascotas.count()
#     valor_unitario_mascota = (
#         (tarifa_asociado.cuotaMascota or 0) // cantidad_mascotas_actuales 
#         if cantidad_mascotas_actuales > 0 
#         else 5500  # Valor por defecto si no hay mascotas
#     )
    
#     print(f"\n=== CÁLCULO VALOR UNITARIO MASCOTA ===")
#     print(f"Total en tarifa: {tarifa_asociado.cuotaMascota}")
#     print(f"Cantidad mascotas actuales: {cantidad_mascotas_actuales}")
#     print(f"Valor unitario calculado: {valor_unitario_mascota}")
#     print("=====================================\n")
    
#     valor_mascotas, cuotas_mascotas = CalculadoraCuotasService.calcular_valores_mascotas(
#         mascotas, mes.pk, meses_pagados, saldos, valor_unitario_mascota
#     )
    
#     # Valor unitario de repatriación (calculado dividiendo entre cantidad actual)
#     # Primero contar cuántas repatriaciones hay activas ACTUALMENTE
#     cantidad_repatriaciones_benef_actuales = sum(1 for b in beneficiarios if b.repatriacion)
#     cantidad_rep_titular_actual = 1 if repatriacion_titular else 0
#     cantidad_total_repatriaciones = cantidad_repatriaciones_benef_actuales + cantidad_rep_titular_actual
    
#     # Obtener el total en tarifa (usando campos separados)
#     total_repatriaciones_tarifa = (
#         (tarifa_asociado.cuotaRepatriacionBeneficiarios or 0) +
#         (tarifa_asociado.cuotaRepatriacionTitular or 0)
#     )
    
#     # Calcular valor unitario
#     valor_unitario_repatriacion = (
#         total_repatriaciones_tarifa // cantidad_total_repatriaciones 
#         if cantidad_total_repatriaciones > 0 
#         else 10500  # Valor por defecto
#     )
    
#     print(f"\n=== CÁLCULO VALOR UNITARIO REPATRIACIÓN ===")
#     print(f"Total en tarifa: {total_repatriaciones_tarifa}")
#     print(f"Beneficiarios con repatriación: {cantidad_repatriaciones_benef_actuales}")
#     print(f"Titular con repatriación: {cantidad_rep_titular_actual}")
#     print(f"Total repatriaciones: {cantidad_total_repatriaciones}")
#     print(f"Valor unitario calculado: {valor_unitario_repatriacion}")
#     print("==========================================\n")
    
#     valor_rep_benef, valor_rep_titular, cuotas_repatriaciones = (
#         CalculadoraCuotasService.calcular_valores_repatriaciones(
#             beneficiarios, repatriacion_titular, mes.pk, meses_pagados, 
#             saldos, valor_unitario_repatriacion
#         )
#     )
    
#     # Total de repatriaciones
#     valor_repatriaciones_total = valor_rep_benef + valor_rep_titular
    
#     # ========================================================================
#     # CALCULAR VALORES ADICIONALES
#     # ========================================================================
    
#     valores_adicionales = CalculadoraCuotasService.calcular_valores_adicionales(
#         cuotas_vencidas, tarifa_asociado, mes.pk, meses_pagados, saldos, seguro_vida
#     )
    
#     # ========================================================================
#     # PROCESAR CONVENIOS (SEPARANDO GASOLINA)
#     # ========================================================================
    
#     convenios_normales, tiene_gasolina = ConsultaConveniosService.obtener_convenios_activos_separados(
#         id_asociado, mes.pk
#     )
    
#     valor_convenios_normales = 0
    
#     for convenio in convenios_normales:
#         if saldos:
#             meses_pendientes_convenio = ConsultaConveniosService.calcular_meses_pendientes_convenio(
#                 convenio, mes.pk, meses_pagados
#             )
#         else:
#             meses_pendientes_convenio = 1 if cuotas_vencidas > 0 else 0
        
#         convenio.cantidad_meses = meses_pendientes_convenio
#         convenio.valor_vencido_convenio = convenio.convenio.valor * meses_pendientes_convenio
#         valor_convenios_normales += convenio.valor_vencido_convenio
    
#     # Convenio de gasolina (total acumulado)
#     valor_gasolina = 0
#     convenio_gasolina_info = None
    
#     if tiene_gasolina:
#         valor_gasolina = ConsultaConveniosService.obtener_total_gasolina(id_asociado)
#         convenio_gasolina_info = {
#             'activo': True,
#             'concepto': 'CHIP GASOLINA',
#             'pendiente_total': valor_gasolina,
#         }
    
#     valor_total_convenios = valor_convenios_normales + valor_gasolina
    
#     # ========================================================================
#     # PROCESAR CRÉDITOS
#     # ========================================================================
    
#     creditos_info = ConsultaCreditosService.obtener_creditos_activos(id_asociado)
#     ventas_home_info = ConsultaCreditosService.obtener_ventas_home_elements_activas(id_asociado)
    
#     # Calcular cuotas actuales de créditos
#     valor_total_creditos = 0
#     for credito in creditos_info:
#         credito['cuota_actual'] = CalculadoraCuotasService.calcular_cuota_credito_actual(credito, mes.pk)
#         credito['progreso'] = f"{credito['cuotas_pagas']}/{credito['cuotas_totales']}"
#         valor_total_creditos += credito['cuota_actual']
    
#     for venta in ventas_home_info:
#         venta['cuota_actual'] = CalculadoraCuotasService.calcular_cuota_credito_actual(venta, mes.pk)
#         venta['progreso'] = f"{venta['cuotas_pagas']}/{venta['cuotas_totales']}"
#         valor_total_creditos += venta['cuota_actual']
    
#     # ========================================================================
#     # CALCULAR VINCULACIÓN
#     # ========================================================================
    
#     valor_vinculacion = 0
    
#     # Solo si es descuento de nómina (FormaPago.pk = 2) y tiene saldo pendiente
#     if (parametro.vinculacionFormaPago and 
#         parametro.vinculacionFormaPago.pk == 2 and 
#         parametro.vinculacionPendientePago and 
#         parametro.vinculacionPendientePago > 0):
        
#         # Contar cuotas ya pagadas (código 9995)
#         cuotas_pagas_vinculacion = HistorialPagos.objects.filter(
#             asociado=id_asociado,
#             mesPago=9995,
#             estadoRegistro=True
#         ).count()
        
#         # Calcular cuota actual de vinculación
#         if cuotas_pagas_vinculacion >= parametro.vinculacionCuotas:
#             # Ya pagó todas las cuotas pero aún hay saldo (ajuste)
#             valor_vinculacion = parametro.vinculacionPendientePago
#         elif cuotas_pagas_vinculacion == parametro.vinculacionCuotas - 1:
#             # Última cuota (puede tener ajuste)
#             valor_vinculacion = parametro.vinculacionPendientePago
#         elif parametro.vinculacionPendientePago < parametro.vinculacionValor:
#             # Pago parcial en cuota intermedia
#             valor_vinculacion = parametro.vinculacionPendientePago
#         else:
#             # Cuota normal
#             valor_vinculacion = parametro.vinculacionValor
    
#     # ========================================================================
#     # CALCULAR TOTALES SEGÚN ESTADO
#     # ========================================================================
    
#     # Consolidar todos los valores vencidos
#     valores_vencidos_consolidados = {
#         'mascota': valor_mascotas,
#         'repatriacion': valor_repatriaciones_total,
#         'seguro_vida': valores_adicionales['seguro_vida'],
#         'adicionales': valores_adicionales['adicionales'],
#         'coohop': valores_adicionales['coohop'],
#     }
    
#     # Inicializar variables del context
#     saldo = 0
#     valor_vencido = 0
#     pago_total = 0
#     mensaje = ""
    
#     # CASO 1: Tiene cuotas vencidas
#     if cuotas_vencidas > 0:
#         valor_vencido, pago_total, mensaje = CalculadoraSaldosService.calcular_pago_con_saldo(
#             cuota_periodica_total,
#             saldo_diferencia,
#             valores_vencidos_consolidados,
#             valor_total_convenios
#         )
#         # Agregar créditos y vinculación al pago total
#         pago_total += valor_total_creditos + valor_vinculacion
    
#     # CASO 2: Está al día (sin cuotas vencidas ni adelantadas)
#     elif cuotas_adelantadas == 0:
#         saldo, valor_vencido, pago_total, mensaje = CalculadoraSaldosService.calcular_estado_al_dia(
#             tarifa_asociado, saldo_diferencia
#         )
#         # Agregar créditos y vinculación al pago total
#         pago_total += valor_total_creditos + valor_vinculacion
    
#     # CASO 3: Tiene pagos adelantados
#     else:
#         saldo_actual = ConsultaPagosService.obtener_saldo_adelantado(id_asociado, mes.pk)
#         saldo = saldo_actual + saldo_diferencia
#         pago_total = 0  # No debe nada este mes
        
#         ultimo_pago = ConsultaPagosService.obtener_ultimo_mes_pagado(id_asociado)
#         if ultimo_pago:
#             mensaje = f"Tiene pago hasta el mes de {ultimo_pago.mesPago.concepto}"
    
#     # ========================================================================
#     # CONSTRUIR CONCEPTOS DETALLADOS PARA PDF
#     # ========================================================================
    
#     conceptos_detallados = []
    
#     # 1. CUOTA PERIÓDICA
#     if cuotas_vencidas > 0:
#         conceptos_detallados.append({
#             'concepto': f'CUOTA {mes.concepto}',
#             'cuotas_vencidas': cuotas_vencidas,
#             'cuota_mes': cuota_periodica,
#             'total': cuota_periodica_total
#         })
    
#     # 2. MASCOTAS (Detalladas individualmente)
#     for mascota in mascotas:
#         primer_mes_pk = mascota.primerMes.pk if mascota.primerMes else mes.pk
        
#         # Calcular cuotas vencidas individuales
#         if saldos:
#             meses_vencidos_mascota = MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
#                 pk__in=CODIGOS_ESPECIALES
#             ).filter(pk__gte=primer_mes_pk, pk__lte=mes.pk).count()
#         else:
#             meses_vencidos_mascota = 1 if cuotas_vencidas > 0 else 0
        
#         if meses_vencidos_mascota > 0:
#             conceptos_detallados.append({
#                 'concepto': f'MASCOTA - {mascota.nombre}',
#                 'cuotas_vencidas': meses_vencidos_mascota,
#                 'cuota_mes': valor_unitario_mascota,
#                 'total': meses_vencidos_mascota * valor_unitario_mascota
#             })
    
#     # 3. REPATRIACIONES BENEFICIARIOS (Detalladas individualmente)
#     for beneficiario in beneficiarios:
#         if not beneficiario.repatriacion:
#             continue
        
#         primer_mes_pk = (beneficiario.primerMesRepatriacion.pk 
#                         if beneficiario.primerMesRepatriacion 
#                         else mes.pk)
        
#         # Calcular cuotas vencidas individuales
#         if saldos:
#             meses_vencidos_benef = MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
#                 pk__in=CODIGOS_ESPECIALES
#             ).filter(pk__gte=primer_mes_pk, pk__lte=mes.pk).count()
#         else:
#             meses_vencidos_benef = 1 if cuotas_vencidas > 0 else 0
        
#         if meses_vencidos_benef > 0:
#             conceptos_detallados.append({
#                 'concepto': f'REPATRIACION - {beneficiario.nombre} {beneficiario.apellido}',
#                 'cuotas_vencidas': meses_vencidos_benef,
#                 'cuota_mes': valor_unitario_repatriacion,
#                 'total': meses_vencidos_benef * valor_unitario_repatriacion
#             })
    
#     # 4. REPATRIACIÓN TITULAR
#     if repatriacion_titular:
#         primer_mes_pk = (repatriacion_titular.primerMes.pk 
#                         if repatriacion_titular.primerMes 
#                         else mes.pk)
        
#         # Calcular cuotas vencidas titular
#         if saldos:
#             meses_vencidos_titular = MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
#                 pk__in=CODIGOS_ESPECIALES
#             ).filter(pk__gte=primer_mes_pk, pk__lte=mes.pk).count()
#         else:
#             meses_vencidos_titular = 1 if cuotas_vencidas > 0 else 0
        
#         if meses_vencidos_titular > 0:
#             conceptos_detallados.append({
#                 'concepto': 'REPATRIACION - TITULAR',
#                 'cuotas_vencidas': meses_vencidos_titular,
#                 'cuota_mes': valor_unitario_repatriacion,
#                 'total': meses_vencidos_titular * valor_unitario_repatriacion
#             })
    
#     # 5. CONVENIOS NORMALES (Cada uno por separado)
#     for convenio in convenios_normales:
#         if convenio.cantidad_meses > 0:
#             conceptos_detallados.append({
#                 'concepto': f'CONVENIO - {convenio.convenio.concepto}',
#                 'cuotas_vencidas': convenio.cantidad_meses,
#                 'cuota_mes': convenio.convenio.valor,
#                 'total': convenio.valor_vencido_convenio
#             })
    
#     # 6. CONVENIO GASOLINA (Total acumulado)
#     if tiene_gasolina and valor_gasolina > 0:
#         conceptos_detallados.append({
#             'concepto': 'CONVENIO - CHIP GASOLINA',
#             'cuotas_vencidas': 'N/A',
#             'cuota_mes': 'N/A',
#             'total': valor_gasolina
#         })
    
#     # 7. CRÉDITOS LIBRE INVERSIÓN
#     for credito in creditos_info:
#         # Siempre agregar, pero con valores en 0 si primerMes es futuro
#         conceptos_detallados.append({
#             'concepto': credito['tipo'],
#             'cuotas_vencidas': credito['progreso'],  # "0/4" o "1/4"
#             'cuota_mes': credito['valor_cuota'],
#             'total': credito['cuota_actual']  # 0 si primerMes futuro
#         })
    
#     # 8. CRÉDITOS HOME ELEMENTS
#     for venta in ventas_home_info:
#         # Siempre agregar, pero con valores en 0 si primerMes es futuro
#         conceptos_detallados.append({
#             'concepto': venta['tipo'],
#             'cuotas_vencidas': venta['progreso'],  # "0/3" o "1/3"
#             'cuota_mes': venta['valor_cuota'],
#             'total': venta['cuota_actual']  # 0 si primerMes futuro
#         })
    
#     # 9. CUOTA DE VINCULACIÓN
#     # Solo si es descuento de nómina (FormaPago.pk = 2) y tiene saldo pendiente
#     if valor_vinculacion > 0:
#         # Contar cuotas ya pagadas (código 9995)
#         cuotas_pagas_vinculacion = HistorialPagos.objects.filter(
#             asociado=id_asociado,
#             mesPago=9995,
#             estadoRegistro=True
#         ).count()
        
#         # Progreso
#         progreso_vinculacion = f"{cuotas_pagas_vinculacion}/{parametro.vinculacionCuotas or 0}"
        
#         conceptos_detallados.append({
#             'concepto': 'CUOTA VINCULACION',
#             'cuotas_vencidas': progreso_vinculacion,  # "0/3"
#             'cuota_mes': parametro.vinculacionValor or 0,  # Valor original de la cuota
#             'total': valor_vinculacion  # Valor calculado (puede ser una cuota o pendiente ajustado)
#         })
    
#     # 10. SEGURO DE VIDA
#     if valores_adicionales['seguro_vida'] > 0 and seguro_vida:
#         # Calcular cuotas vencidas de seguro
#         if saldos and seguro_vida.primerMesSeguroVida:
#             meses_vencidos_seguro = MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
#                 pk__in=CODIGOS_ESPECIALES
#             ).filter(
#                 pk__gte=seguro_vida.primerMesSeguroVida.pk,
#                 pk__lte=mes.pk
#             ).count()
#         else:
#             meses_vencidos_seguro = cuotas_vencidas
        
#         conceptos_detallados.append({
#             'concepto': 'SEGURO VIDA',
#             'cuotas_vencidas': meses_vencidos_seguro,
#             'cuota_mes': tarifa_asociado.cuotaSeguroVida or 0,
#             'total': valores_adicionales['seguro_vida']
#         })
    
#     # 11. ADICIONALES
#     if valores_adicionales['adicionales'] > 0 and tarifa_asociado.estadoAdicional:
#         # Calcular cuotas vencidas adicionales
#         if saldos and tarifa_asociado.primerMesCuotaAdicional:
#             meses_vencidos_adicional = MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
#                 pk__in=CODIGOS_ESPECIALES
#             ).filter(
#                 pk__gte=tarifa_asociado.primerMesCuotaAdicional.pk,
#                 pk__lte=mes.pk
#             ).count()
#         else:
#             meses_vencidos_adicional = cuotas_vencidas
        
#         conceptos_detallados.append({
#             'concepto': f'ADICIONALES - {tarifa_asociado.conceptoAdicional or ""}',
#             'cuotas_vencidas': meses_vencidos_adicional,
#             'cuota_mes': tarifa_asociado.cuotaAdicionales or 0,
#             'total': valores_adicionales['adicionales']
#         })
    
#     # 12. COOHOPERATIVITOS
#     if valores_adicionales['coohop'] > 0:
#         conceptos_detallados.append({
#             'concepto': 'COOHOPERATIVITOS',
#             'cuotas_vencidas': cuotas_vencidas,
#             'cuota_mes': cuota_coohop,
#             'total': valores_adicionales['coohop']
#         })
    
#     # ========================================================================
#     # CONSTRUIR Y RETORNAR CONTEXT
#     # ========================================================================
    
#     context = {
#         # Información básica
#         "pkAsociado": id_asociado,
#         "fechaCorte": fecha_corte,
#         "mes": mes,
        
#         # Tarifa del asociado
#         "objTarifaAsociado": tarifa_asociado,
#         "cuotaPeriodica": cuota_periodica,
#         "cuotaCoohop": cuota_coohop,
        
#         # Cuotas y valores vencidos
#         "cuotaVencida": cuotas_vencidas,
#         "valorVencido": valor_vencido,
#         "valorVencidoMasc": valor_mascotas,
#         "valorVencidoRep": valor_repatriaciones_total,
#         "valorVencidoRepBeneficiarios": valor_rep_benef,
#         "valorVencidoRepTitular": valor_rep_titular,
#         "valorVencidoSeg": valores_adicionales['seguro_vida'],
#         "valorVencidoAdic": valores_adicionales['adicionales'],
#         "valorVencidoCoohop": valores_adicionales['coohop'],
#         "valorVencidoConvenio": valor_total_convenios,
#         "valorVencidoConveniosNormales": valor_convenios_normales,
#         "valorVencidoGasolina": valor_gasolina,
        
#         # Créditos (NUEVA FUNCIONALIDAD)
#         "creditos": creditos_info,
#         "ventasHomeElements": ventas_home_info,
#         "valorTotalCreditos": valor_total_creditos,
        
#         # Vinculación (NUEVA FUNCIONALIDAD)
#         "vinculacion": {
#             "activa": (parametro.vinculacionFormaPago and 
#                       parametro.vinculacionFormaPago.pk == 2 and 
#                       parametro.vinculacionPendientePago and 
#                       parametro.vinculacionPendientePago > 0),
#             "cuotas_totales": parametro.vinculacionCuotas or 0,
#             "valor_cuota": parametro.vinculacionValor or 0,
#             "pendiente_pago": parametro.vinculacionPendientePago or 0,
#         },
        
#         # Totales y saldos
#         "pagoTotal": pago_total,
#         "saldo": saldo,
#         "saldoDiferencia": saldo_diferencia,  # ← NUEVO: Valor numérico puro
#         "mensaje": mensaje,
        
#         # Beneficiarios y mascotas (con información extendida)
#         "objBeneficiario": beneficiarios,
#         "cuentaBeneficiario": beneficiarios.count(),
#         "cuentaBeneficiarioConRepatriacion": sum(1 for b in beneficiarios if b.repatriacion),
#         "objMascota": mascotas,
#         "cuentaMascota": mascotas.count(),
#         "objRepatriacionTitular": repatriacion_titular,
#         "objSeguroVida": seguro_vida,
        
#         # Convenios (separados)
#         "objConvenio": convenios_normales,
#         "convenioGasolina": convenio_gasolina_info,
        
#         # Conceptos Detallados para PDF (NUEVA FUNCIONALIDAD)
#         "conceptos_detallados": conceptos_detallados,
        
#         # Vista (mantener compatibilidad)
#         "vista": 0,
#     }
    
#     return context

"""
Refactorización del sistema de extractos financieros
Versión 2.0 - Con soporte para primerMes en mascotas, repatriaciones y convenio gasolina
"""
from django.db.models import Sum, Count, Q, Max
from datetime import timedelta
from typing import Dict, List, Tuple, Optional


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
        ).select_related('tasaInteres', 'primerMes')
        
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
                'primer_mes': credito.primerMes,  # ← NUEVO
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
        ).select_related('tasaInteres', 'descuento', 'primerMes')
        
        return [
            {
                'id': venta.id,
                'tipo': 'CREDITO PRODUCTOS',
                'valor_cuota': venta.valorCuotas,
                'cuotas_totales': venta.cuotas,
                'cuotas_pagas': venta.cuotasPagas or 0,
                'pendiente_pago': venta.pendientePago,
                'total_venta': venta.valorNeto,
                'primer_mes': venta.primerMes,  # ← NUEVO
            }
            for venta in ventas
        ]


# ============================================================================
# SERVICIO DE CONSULTA DE SALDOS DETALLADOS
# ============================================================================

class ConsultaSaldosDetalladosService:
    """
    Servicio para obtener saldos (diferencias) desglosados por concepto.
    
    Los saldos se obtienen del campo 'diferencia' de HistorialPagos:
    - Positivo: Asociado pagó de más (a su favor)
    - Negativo: Asociado pagó de menos (debe)
    - Cero: Pagó exacto
    """
    
    @staticmethod
    def obtener_saldo_cuota_periodica(id_asociado: int) -> int:
        """
        Obtiene el saldo neto de la cuota periódica (meses normales + abonos).
        
        Incluye:
        - Pagos de meses normales (excluye códigos especiales)
        - Abonos (mesPago = 9999)
        """
        from django.db.models import Sum, Q
        
        resultado = HistorialPagos.objects.filter(
            asociado=id_asociado,
            estadoRegistro=True
        ).filter(
            # Meses normales (excluir códigos especiales)
            Q(mesPago__pk__lt=min(CODIGOS_ESPECIALES)) |
            # O abonos (9999)
            Q(mesPago__pk=CODIGO_ABONO)
        ).aggregate(total=Sum("diferencia"))
        
        return resultado["total"] or 0
    
    @staticmethod
    def obtener_saldo_por_credito(id_asociado: int, credito_id: int) -> int:
        """
        Obtiene el saldo específico de un crédito libre inversión.
        
        Args:
            id_asociado: ID del asociado
            credito_id: ID del crédito (FK creditoId)
        
        Returns:
            Saldo acumulado del crédito (puede ser positivo o negativo)
        """
        resultado = HistorialPagos.objects.filter(
            asociado=id_asociado,
            estadoRegistro=True,
            creditoId=credito_id
        ).aggregate(total=Sum("diferencia"))
        
        return resultado["total"] or 0
    
    @staticmethod
    def obtener_saldo_por_venta_home(id_asociado: int, venta_id: int) -> int:
        """
        Obtiene el saldo específico de una venta de Home Elements.
        
        Args:
            id_asociado: ID del asociado
            venta_id: ID de la venta (FK ventaHE)
        
        Returns:
            Saldo acumulado de la venta (puede ser positivo o negativo)
        """
        resultado = HistorialPagos.objects.filter(
            asociado=id_asociado,
            estadoRegistro=True,
            ventaHE=venta_id
        ).aggregate(total=Sum("diferencia"))
        
        return resultado["total"] or 0
    
    @staticmethod
    def obtener_saldo_gasolina(id_asociado: int) -> int:
        """
        Obtiene el saldo del convenio de gasolina.
        
        Returns:
            Saldo acumulado de pagos de gasolina (puede ser positivo o negativo)
        """
        resultado = HistorialPagos.objects.filter(
            asociado=id_asociado,
            estadoRegistro=True,
            mesPago__pk=9990,  # Código de gasolina
            convenio_gasolina_id__isnull=False
        ).aggregate(total=Sum("diferencia"))
        
        return resultado["total"] or 0
    
    @staticmethod
    def obtener_saldos_creditos_finalizados(id_asociado: int, creditos_activos_ids: list) -> int:
        """
        Obtiene el saldo total de créditos que ya fueron finalizados.
        
        Esto captura diferencias de créditos que ya no aparecen en la lista
        de créditos activos pero que tienen saldo a favor o en contra.
        
        Args:
            id_asociado: ID del asociado
            creditos_activos_ids: Lista de IDs de créditos actualmente activos
        
        Returns:
            Saldo acumulado de créditos finalizados
        """
        query = HistorialPagos.objects.filter(
            asociado=id_asociado,
            estadoRegistro=True,
            mesPago__pk=CODIGO_CREDITO_LIBRE,  # 9993
            creditoId__isnull=False
        )
        
        # Excluir créditos activos
        if creditos_activos_ids:
            query = query.exclude(creditoId__in=creditos_activos_ids)
        
        resultado = query.aggregate(total=Sum("diferencia"))
        return resultado["total"] or 0
    
    @staticmethod
    def obtener_saldos_ventas_finalizadas(id_asociado: int, ventas_activas_ids: list) -> int:
        """
        Obtiene el saldo total de ventas de Home Elements que ya fueron finalizadas.
        
        Args:
            id_asociado: ID del asociado
            ventas_activas_ids: Lista de IDs de ventas actualmente activas
        
        Returns:
            Saldo acumulado de ventas finalizadas
        """
        query = HistorialPagos.objects.filter(
            asociado=id_asociado,
            estadoRegistro=True,
            mesPago__pk=CODIGO_CREDITO_HOME,  # 9998
            ventaHE__isnull=False
        )
        
        # Excluir ventas activas
        if ventas_activas_ids:
            query = query.exclude(ventaHE__in=ventas_activas_ids)
        
        resultado = query.aggregate(total=Sum("diferencia"))
        return resultado["total"] or 0
    
    @staticmethod
    def obtener_desglose_completo_saldos(id_asociado: int, creditos_activos: list, 
                                         ventas_activas: list) -> dict:
        """
        Obtiene un desglose completo de todos los saldos del asociado.
        
        Args:
            id_asociado: ID del asociado
            creditos_activos: Lista de dicts con información de créditos activos (debe incluir 'id')
            ventas_activas: Lista de dicts con información de ventas activas (debe incluir 'id')
        
        Returns:
            Dict con todos los saldos desglosados:
            {
                'cuota_periodica': int,
                'creditos': {credito_id: saldo, ...},
                'ventas_home': {venta_id: saldo, ...},
                'gasolina': int,
                'creditos_finalizados': int,
                'ventas_finalizadas': int,
                'total': int
            }
        """
        desglose = {
            'cuota_periodica': 0,
            'creditos': {},
            'ventas_home': {},
            'gasolina': 0,
            'creditos_finalizados': 0,
            'ventas_finalizadas': 0,
            'total': 0
        }
        
        # 1. Saldo de cuota periódica (incluye abonos)
        desglose['cuota_periodica'] = ConsultaSaldosDetalladosService.obtener_saldo_cuota_periodica(id_asociado)
        
        # 2. Saldos de créditos activos
        for credito in creditos_activos:
            saldo = ConsultaSaldosDetalladosService.obtener_saldo_por_credito(
                id_asociado, credito['id']
            )
            desglose['creditos'][credito['id']] = saldo
        
        # 3. Saldos de ventas activas
        for venta in ventas_activas:
            saldo = ConsultaSaldosDetalladosService.obtener_saldo_por_venta_home(
                id_asociado, venta['id']
            )
            desglose['ventas_home'][venta['id']] = saldo
        
        # 4. Saldo de gasolina
        desglose['gasolina'] = ConsultaSaldosDetalladosService.obtener_saldo_gasolina(id_asociado)
        
        # 5. Saldos de créditos finalizados
        creditos_activos_ids = [c['id'] for c in creditos_activos]
        desglose['creditos_finalizados'] = ConsultaSaldosDetalladosService.obtener_saldos_creditos_finalizados(
            id_asociado, creditos_activos_ids
        )
        
        # 6. Saldos de ventas finalizadas
        ventas_activas_ids = [v['id'] for v in ventas_activas]
        desglose['ventas_finalizadas'] = ConsultaSaldosDetalladosService.obtener_saldos_ventas_finalizadas(
            id_asociado, ventas_activas_ids
        )
        
        # 7. Total
        desglose['total'] = (
            desglose['cuota_periodica'] +
            sum(desglose['creditos'].values()) +
            sum(desglose['ventas_home'].values()) +
            desglose['gasolina'] +
            desglose['creditos_finalizados'] +
            desglose['ventas_finalizadas']
        )
        
        return desglose


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
    def calcular_cuota_credito_actual(credito_info: Dict, mes_actual_pk: int) -> int:
        """
        Calcula el valor de la cuota actual de un crédito.
        Maneja casos de última cuota, pagos parciales y primerMes futuro.
        """
        pendiente = credito_info['pendiente_pago']
        cuotas_pagas = credito_info['cuotas_pagas']
        cuotas_totales = credito_info['cuotas_totales']
        valor_cuota = credito_info['valor_cuota']
        primer_mes = credito_info.get('primer_mes')
        
        # Si tiene primerMes y aún no ha llegado ese mes, retornar 0
        if primer_mes and primer_mes.pk > mes_actual_pk:
            return 0
        
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
        
        # Si el saldo a favor supera lo que debe, el valor vencido es 0
        if valor_vencido < 0:
            valor_vencido = 0
        
        suma_adicionales = sum(valores_vencidos.values()) + valor_convenios
        pago_total = valor_vencido + suma_adicionales
        
        # Evitar pago total negativo (doble validación)
        if pago_total < 0:
            pago_total = 0
        
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
# SERVICIO DE CONSTRUCCIÓN DE CONCEPTOS DETALLADOS
# ============================================================================

class ConstructorConceptosDetalladosService:
    """
    Servicio para construir la lista de conceptos detallados del extracto.
    
    Cada concepto incluye:
    - concepto: Nombre del concepto
    - cuotas_vencidas: Cantidad de cuotas (o progreso en créditos)
    - cuota_mes: Valor de la cuota mensual
    - total: Total adeudado
    - saldo: Saldo a favor/contra del asociado
    - total_a_pagar: Total final (total - saldo, nunca negativo)
    """
    
    @staticmethod
    def agregar_cuota_periodica(conceptos: list, mes, cuota_periodica: int, 
                                cuota_periodica_total: int, cuotas_vencidas: int,
                                saldo_cuota_periodica: int):
        """Agrega el concepto de cuota periódica"""
        total_a_pagar = max(0, cuota_periodica_total - saldo_cuota_periodica)
        
        conceptos.append({
            'concepto': f'CUOTA {mes.concepto}',
            'cuotas_vencidas': cuotas_vencidas if cuotas_vencidas > 0 else 0,
            'cuota_mes': cuota_periodica,
            'total': cuota_periodica_total if cuotas_vencidas > 0 else 0,
            'saldo': saldo_cuota_periodica,
            'total_a_pagar': total_a_pagar if cuotas_vencidas > 0 else 0
        })
    
    @staticmethod
    def agregar_mascotas(conceptos: list, mascotas, mes_pk: int, meses_pagados: list,
                        saldos: bool, valor_unitario: int):
        """Agrega conceptos de mascotas (individuales)"""
        for mascota in mascotas:
            primer_mes_pk = mascota.primerMes.pk if mascota.primerMes else mes_pk
            
            # Calcular cuotas vencidas individuales
            if saldos:
                meses_vencidos_mascota = MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
                    pk__in=CODIGOS_ESPECIALES
                ).filter(pk__gte=primer_mes_pk, pk__lte=mes_pk).count()
            else:
                meses_vencidos_mascota = 0
            
            total = meses_vencidos_mascota * valor_unitario if meses_vencidos_mascota > 0 else 0
            
            # Las mascotas no tienen saldo individual, se incluyen en cuota periódica
            conceptos.append({
                'concepto': f'MASCOTA - {mascota.nombre}',
                'cuotas_vencidas': meses_vencidos_mascota,
                'cuota_mes': valor_unitario,
                'total': total,
                'saldo': 0,
                'total_a_pagar': total
            })
    
    @staticmethod
    def agregar_repatriaciones_beneficiarios(conceptos: list, beneficiarios, mes_pk: int,
                                             meses_pagados: list, saldos: bool,
                                             valor_unitario: int):
        """Agrega conceptos de repatriaciones de beneficiarios (individuales)"""
        for beneficiario in beneficiarios:
            if not beneficiario.repatriacion:
                continue
            
            primer_mes_pk = (beneficiario.primerMesRepatriacion.pk 
                            if beneficiario.primerMesRepatriacion 
                            else mes_pk)
            
            # Calcular cuotas vencidas individuales
            if saldos:
                meses_vencidos_benef = MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
                    pk__in=CODIGOS_ESPECIALES
                ).filter(pk__gte=primer_mes_pk, pk__lte=mes_pk).count()
            else:
                meses_vencidos_benef = 0
            
            total = meses_vencidos_benef * valor_unitario if meses_vencidos_benef > 0 else 0
            
            # Las repatriaciones no tienen saldo individual, se incluyen en cuota periódica
            conceptos.append({
                'concepto': f'REPATRIACION - {beneficiario.nombre} {beneficiario.apellido}',
                'cuotas_vencidas': meses_vencidos_benef,
                'cuota_mes': valor_unitario,
                'total': total,
                'saldo': 0,
                'total_a_pagar': total
            })
    
    @staticmethod
    def agregar_repatriacion_titular(conceptos: list, repatriacion_titular, mes_pk: int,
                                     meses_pagados: list, saldos: bool, valor_unitario: int):
        """Agrega concepto de repatriación del titular"""
        if not repatriacion_titular:
            return
        
        primer_mes_pk = (repatriacion_titular.primerMes.pk 
                        if repatriacion_titular.primerMes 
                        else mes_pk)
        
        # Calcular cuotas vencidas titular
        if saldos:
            meses_vencidos_titular = MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
                pk__in=CODIGOS_ESPECIALES
            ).filter(pk__gte=primer_mes_pk, pk__lte=mes_pk).count()
        else:
            meses_vencidos_titular = 0
        
        total = meses_vencidos_titular * valor_unitario if meses_vencidos_titular > 0 else 0
        
        # La repatriación titular no tiene saldo individual
        conceptos.append({
            'concepto': 'REPATRIACION - TITULAR',
            'cuotas_vencidas': meses_vencidos_titular,
            'cuota_mes': valor_unitario,
            'total': total,
            'saldo': 0,
            'total_a_pagar': total
        })
    
    @staticmethod
    def agregar_convenios_normales(conceptos: list, convenios_normales):
        """Agrega conceptos de convenios normales (cada uno por separado)"""
        for convenio in convenios_normales:
            if convenio.cantidad_meses > 0:
                # Los convenios normales no tienen saldo individual
                conceptos.append({
                    'concepto': f'CONVENIO - {convenio.convenio.concepto}',
                    'cuotas_vencidas': convenio.cantidad_meses,
                    'cuota_mes': convenio.convenio.valor,
                    'total': convenio.valor_vencido_convenio,
                    'saldo': 0,
                    'total_a_pagar': convenio.valor_vencido_convenio
                })
    
    @staticmethod
    def agregar_convenio_gasolina(conceptos: list, valor_gasolina: int, saldo_gasolina: int):
        """Agrega concepto de convenio de gasolina con su saldo"""
        if valor_gasolina > 0 or saldo_gasolina != 0:
            total_a_pagar = max(0, valor_gasolina - saldo_gasolina)
            
            conceptos.append({
                'concepto': 'CONVENIO - CHIP GASOLINA',
                'cuotas_vencidas': '1',
                'cuota_mes': total_a_pagar,
                'total': valor_gasolina,
                'saldo': saldo_gasolina,
                'total_a_pagar': total_a_pagar
            })
    
    @staticmethod
    def agregar_creditos(conceptos: list, creditos_info: list, desglose_saldos: dict):
        """Agrega conceptos de créditos libre inversión con sus saldos individuales"""
        for credito in creditos_info:
            saldo_credito = desglose_saldos['creditos'].get(credito['id'], 0)
            total_a_pagar = max(0, credito['cuota_actual'] - saldo_credito)
            
            conceptos.append({
                'concepto': credito['tipo'],
                'cuotas_vencidas': credito['progreso'],
                'cuota_mes': credito['valor_cuota'],
                'total': credito['cuota_actual'],
                'saldo': saldo_credito,
                'total_a_pagar': total_a_pagar
            })
    
    @staticmethod
    def agregar_ventas_home(conceptos: list, ventas_home_info: list, desglose_saldos: dict):
        """Agrega conceptos de ventas Home Elements con sus saldos individuales"""
        for venta in ventas_home_info:
            saldo_venta = desglose_saldos['ventas_home'].get(venta['id'], 0)
            total_a_pagar = max(0, venta['cuota_actual'] - saldo_venta)
            
            conceptos.append({
                'concepto': venta['tipo'],
                'cuotas_vencidas': venta['progreso'],
                'cuota_mes': venta['valor_cuota'],
                'total': venta['cuota_actual'],
                'saldo': saldo_venta,
                'total_a_pagar': total_a_pagar
            })
    
    @staticmethod
    def agregar_vinculacion(conceptos: list, parametro, id_asociado: int):
        """Agrega concepto de vinculación si está activo"""
        # Solo si es descuento de nómina (FormaPago.pk = 2) y tiene saldo pendiente
        if not (parametro.vinculacionFormaPago and 
                parametro.vinculacionFormaPago.pk == 2 and 
                parametro.vinculacionPendientePago and 
                parametro.vinculacionPendientePago > 0):
            return
        
        # Contar cuotas ya pagadas (código 9995)
        cuotas_pagas_vinculacion = HistorialPagos.objects.filter(
            asociado=id_asociado,
            mesPago=9995,
            estadoRegistro=True
        ).count()
        
        # Calcular cuota actual
        if cuotas_pagas_vinculacion >= parametro.vinculacionCuotas:
            valor_vinculacion = parametro.vinculacionPendientePago
        elif cuotas_pagas_vinculacion == parametro.vinculacionCuotas - 1:
            valor_vinculacion = parametro.vinculacionPendientePago
        elif parametro.vinculacionPendientePago < parametro.vinculacionValor:
            valor_vinculacion = parametro.vinculacionPendientePago
        else:
            valor_vinculacion = parametro.vinculacionValor
        
        progreso = f"{cuotas_pagas_vinculacion}/{parametro.vinculacionCuotas or 0}"
        
        # La vinculación no tiene saldo individual
        conceptos.append({
            'concepto': 'CUOTA VINCULACION',
            'cuotas_vencidas': progreso,
            'cuota_mes': parametro.vinculacionValor or 0,
            'total': valor_vinculacion,
            'saldo': 0,
            'total_a_pagar': valor_vinculacion
        })
    
    @staticmethod
    def agregar_seguro_vida(conceptos: list, seguro_vida, tarifa_asociado, mes_pk: int,
                           meses_pagados: list, saldos: bool, cuotas_vencidas: int,
                           valor_seguro_vida: int):
        """Agrega concepto de seguro de vida si está activo"""
        if not seguro_vida:
            return
        
        # Calcular cuotas vencidas de seguro
        if saldos and seguro_vida.primerMesSeguroVida and cuotas_vencidas > 0:
            meses_vencidos_seguro = MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
                pk__in=CODIGOS_ESPECIALES
            ).filter(
                pk__gte=seguro_vida.primerMesSeguroVida.pk,
                pk__lte=mes_pk
            ).count()
        else:
            meses_vencidos_seguro = 0
        
        total = valor_seguro_vida if cuotas_vencidas > 0 else 0
        
        # El seguro no tiene saldo individual
        conceptos.append({
            'concepto': 'SEGURO VIDA',
            'cuotas_vencidas': meses_vencidos_seguro,
            'cuota_mes': tarifa_asociado.cuotaSeguroVida or 0,
            'total': total,
            'saldo': 0,
            'total_a_pagar': total
        })
    
    @staticmethod
    def agregar_adicionales(conceptos: list, tarifa_asociado, mes_pk: int,
                           meses_pagados: list, saldos: bool, cuotas_vencidas: int,
                           valor_adicionales: int):
        """Agrega concepto de adicionales si está activo"""
        if not (tarifa_asociado.estadoAdicional and tarifa_asociado.cuotaAdicionales):
            return
        
        # Calcular cuotas vencidas adicionales
        if saldos and tarifa_asociado.primerMesCuotaAdicional and cuotas_vencidas > 0:
            meses_vencidos_adicional = MesTarifa.objects.exclude(pk__in=meses_pagados).exclude(
                pk__in=CODIGOS_ESPECIALES
            ).filter(
                pk__gte=tarifa_asociado.primerMesCuotaAdicional.pk,
                pk__lte=mes_pk
            ).count()
        else:
            meses_vencidos_adicional = 0
        
        total = valor_adicionales if cuotas_vencidas > 0 else 0
        
        # Los adicionales no tienen saldo individual
        conceptos.append({
            'concepto': f'ADICIONALES - {tarifa_asociado.conceptoAdicional or ""}',
            'cuotas_vencidas': meses_vencidos_adicional,
            'cuota_mes': tarifa_asociado.cuotaAdicionales or 0,
            'total': total,
            'saldo': 0,
            'total_a_pagar': total
        })
    
    @staticmethod
    def agregar_coohop(conceptos: list, cuota_coohop: int, cuotas_vencidas: int,
                      valor_coohop: int):
        """Agrega concepto de Coohoperativitos si tiene"""
        if cuota_coohop > 0:
            total = valor_coohop if cuotas_vencidas > 0 else 0
            
            # Coohop no tiene saldo individual
            conceptos.append({
                'concepto': 'COOHOPERATIVITOS',
                'cuotas_vencidas': cuotas_vencidas if cuotas_vencidas > 0 else 0,
                'cuota_mes': cuota_coohop,
                'total': total,
                'saldo': 0,
                'total_a_pagar': total
            })
    
    @staticmethod
    def agregar_saldos_finalizados(conceptos: list, desglose_saldos: dict):
        """
        Agrega concepto especial para créditos/ventas finalizados que aún tienen saldo.
        
        Este concepto aparece al final y agrupa todos los saldos de:
        - Créditos finalizados
        - Ventas Home Elements finalizadas
        """
        saldo_total_finalizados = (
            desglose_saldos['creditos_finalizados'] +
            desglose_saldos['ventas_finalizadas']
        )
        
        # Solo agregar si hay saldo (positivo o negativo)
        if saldo_total_finalizados != 0:
            # Si el saldo es negativo, el total_a_pagar es el valor absoluto
            # Si es positivo, total_a_pagar es 0 (porque está a favor)
            total_a_pagar = abs(saldo_total_finalizados) if saldo_total_finalizados < 0 else 0
            
            conceptos.append({
                'concepto': 'SALDO - CREDITOS/VENTAS FINALIZADOS',
                'cuotas_vencidas': 'N/A',
                'cuota_mes': 'N/A',
                'total': abs(saldo_total_finalizados),
                'saldo': saldo_total_finalizados,
                'total_a_pagar': total_a_pagar
            })
    
    @staticmethod
    def construir_conceptos_completos(
        # Datos básicos
        mes, parametro, tarifa_asociado, id_asociado,
        # Cuotas y valores
        cuota_periodica, cuota_coohop, cuotas_vencidas, cuota_periodica_total,
        # Listas de objetos
        mascotas, beneficiarios, repatriacion_titular, convenios_normales,
        creditos_info, ventas_home_info, seguro_vida,
        # Valores calculados
        valor_unitario_mascota, valor_unitario_repatriacion,
        valor_gasolina, valores_adicionales,
        # Estados y configuraciones
        meses_pagados, saldos,
        # Desglose de saldos
        desglose_saldos
    ) -> list:
        """
        Construye la lista completa de conceptos detallados en el orden correcto.
        
        Returns:
            Lista de dicts con todos los conceptos del extracto
        """
        conceptos = []
        
        # 1. CUOTA PERIÓDICA
        ConstructorConceptosDetalladosService.agregar_cuota_periodica(
            conceptos, mes, cuota_periodica, cuota_periodica_total, cuotas_vencidas,
            desglose_saldos['cuota_periodica']
        )
        
        # 2. MASCOTAS (individuales)
        ConstructorConceptosDetalladosService.agregar_mascotas(
            conceptos, mascotas, mes.pk, meses_pagados, saldos, valor_unitario_mascota
        )
        
        # 3. REPATRIACIONES BENEFICIARIOS (individuales)
        ConstructorConceptosDetalladosService.agregar_repatriaciones_beneficiarios(
            conceptos, beneficiarios, mes.pk, meses_pagados, saldos, valor_unitario_repatriacion
        )
        
        # 4. REPATRIACIÓN TITULAR
        ConstructorConceptosDetalladosService.agregar_repatriacion_titular(
            conceptos, repatriacion_titular, mes.pk, meses_pagados, saldos, valor_unitario_repatriacion
        )
        
        # 5. CONVENIOS NORMALES
        ConstructorConceptosDetalladosService.agregar_convenios_normales(
            conceptos, convenios_normales
        )
        
        # 6. GASOLINA
        ConstructorConceptosDetalladosService.agregar_convenio_gasolina(
            conceptos, valor_gasolina, desglose_saldos['gasolina']
        )
        
        # 7. CRÉDITOS LIBRE INVERSIÓN
        ConstructorConceptosDetalladosService.agregar_creditos(
            conceptos, creditos_info, desglose_saldos
        )
        
        # 8. CRÉDITOS HOME ELEMENTS
        ConstructorConceptosDetalladosService.agregar_ventas_home(
            conceptos, ventas_home_info, desglose_saldos
        )
        
        # 9. VINCULACIÓN
        ConstructorConceptosDetalladosService.agregar_vinculacion(
            conceptos, parametro, id_asociado
        )
        
        # 10. SEGURO DE VIDA
        ConstructorConceptosDetalladosService.agregar_seguro_vida(
            conceptos, seguro_vida, tarifa_asociado, mes.pk, meses_pagados,
            saldos, cuotas_vencidas, valores_adicionales['seguro_vida']
        )
        
        # 11. ADICIONALES
        ConstructorConceptosDetalladosService.agregar_adicionales(
            conceptos, tarifa_asociado, mes.pk, meses_pagados, saldos,
            cuotas_vencidas, valores_adicionales['adicionales']
        )
        
        # 12. COOHOPERATIVITOS
        ConstructorConceptosDetalladosService.agregar_coohop(
            conceptos, cuota_coohop, cuotas_vencidas, valores_adicionales['coohop']
        )
        
        # 13. SALDOS DE CRÉDITOS/VENTAS FINALIZADOS (si existen)
        ConstructorConceptosDetalladosService.agregar_saldos_finalizados(
            conceptos, desglose_saldos
        )
        
        return conceptos


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
    # VALIDACIONES Y DATOS BÁSICOS (sin cambios)
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
    
    if mes.pk < parametro.primerMes.pk:
        raise ValueError(
            f"El mes seleccionado ({mes.concepto}) es anterior al primer mes "
            f"de vinculación ({parametro.primerMes.concepto})"
        )
    
    fecha_corte = mes.fechaInicio + timedelta(days=15)
    cuota_periodica = CalculadoraCuotasService.calcular_cuota_periodica(tarifa_asociado)
    cuota_coohop = CalculadoraCuotasService.calcular_cuota_coohop(tarifa_asociado)
    
    # ========================================================================
    # CONSULTAR INFORMACIÓN DE PAGOS (sin cambios)
    # ========================================================================
    
    meses_pagados = ConsultaPagosService.obtener_meses_pagados(id_asociado)
    meses_pendientes = ConsultaPagosService.obtener_meses_pendientes(
        id_asociado, parametro.primerMes.pk, mes.pk, meses_pagados
    )
    
    # ========================================================================
    # CALCULAR CUOTAS VENCIDAS Y ADELANTADAS (sin cambios)
    # ========================================================================
    
    cuotas_vencidas, cuota_periodica_total = CalculadoraCuotasService.calcular_cuotas_vencidas_y_total(
        meses_pendientes, saldos
    )
    cuotas_adelantadas = CalculadoraCuotasService.calcular_cuotas_adelantadas(
        meses_pagados, mes.pk
    )
    
    # ========================================================================
    # CALCULAR SALDO DE DIFERENCIAS (sin cambios)
    # ========================================================================
    
    saldo_diferencia = 0
    if saldos:
        saldo_diferencia = ConsultaPagosService.calcular_saldo_diferencia(id_asociado)
    
    # ========================================================================
    # OBTENER BENEFICIARIOS, MASCOTAS, REPATRIACIONES Y SEGURO DE VIDA (sin cambios)
    # ========================================================================
    
    beneficiarios = ConsultaBeneficiariosService.obtener_beneficiarios_activos(id_asociado)
    mascotas = ConsultaBeneficiariosService.obtener_mascotas_activas(id_asociado)
    repatriacion_titular = ConsultaBeneficiariosService.obtener_repatriacion_titular(id_asociado)
    seguro_vida = ConsultaBeneficiariosService.obtener_seguro_vida_activo(id_asociado)
    
    # ========================================================================
    # CALCULAR VALORES DE MASCOTAS Y REPATRIACIONES (sin cambios)
    # ========================================================================
    
    cantidad_mascotas_actuales = mascotas.count()
    valor_unitario_mascota = (
        (tarifa_asociado.cuotaMascota or 0) // cantidad_mascotas_actuales 
        if cantidad_mascotas_actuales > 0 
        else 5500
    )
    
    valor_mascotas, cuotas_mascotas = CalculadoraCuotasService.calcular_valores_mascotas(
        mascotas, mes.pk, meses_pagados, saldos, valor_unitario_mascota
    )
    
    cantidad_repatriaciones_benef_actuales = sum(1 for b in beneficiarios if b.repatriacion)
    cantidad_rep_titular_actual = 1 if repatriacion_titular else 0
    cantidad_total_repatriaciones = cantidad_repatriaciones_benef_actuales + cantidad_rep_titular_actual
    
    total_repatriaciones_tarifa = (
        (tarifa_asociado.cuotaRepatriacionBeneficiarios or 0) +
        (tarifa_asociado.cuotaRepatriacionTitular or 0)
    )
    
    valor_unitario_repatriacion = (
        total_repatriaciones_tarifa // cantidad_total_repatriaciones 
        if cantidad_total_repatriaciones > 0 
        else 10500
    )
    
    valor_rep_benef, valor_rep_titular, cuotas_repatriaciones = (
        CalculadoraCuotasService.calcular_valores_repatriaciones(
            beneficiarios, repatriacion_titular, mes.pk, meses_pagados, 
            saldos, valor_unitario_repatriacion
        )
    )
    
    valor_repatriaciones_total = valor_rep_benef + valor_rep_titular
    
    # ========================================================================
    # CALCULAR VALORES ADICIONALES (sin cambios)
    # ========================================================================
    
    valores_adicionales = CalculadoraCuotasService.calcular_valores_adicionales(
        cuotas_vencidas, tarifa_asociado, mes.pk, meses_pagados, saldos, seguro_vida
    )
    
    # ========================================================================
    # PROCESAR CONVENIOS (sin cambios)
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
    # PROCESAR CRÉDITOS (sin cambios)
    # ========================================================================
    
    creditos_info = ConsultaCreditosService.obtener_creditos_activos(id_asociado)
    ventas_home_info = ConsultaCreditosService.obtener_ventas_home_elements_activas(id_asociado)
    
    valor_total_creditos = 0
    for credito in creditos_info:
        credito['cuota_actual'] = CalculadoraCuotasService.calcular_cuota_credito_actual(credito, mes.pk)
        credito['progreso'] = f"{credito['cuotas_pagas']}/{credito['cuotas_totales']}"
        valor_total_creditos += credito['cuota_actual']
    
    for venta in ventas_home_info:
        venta['cuota_actual'] = CalculadoraCuotasService.calcular_cuota_credito_actual(venta, mes.pk)
        venta['progreso'] = f"{venta['cuotas_pagas']}/{venta['cuotas_totales']}"
        valor_total_creditos += venta['cuota_actual']
    
    # ========================================================================
    # CALCULAR VINCULACIÓN (sin cambios)
    # ========================================================================
    
    valor_vinculacion = 0
    
    if (parametro.vinculacionFormaPago and 
        parametro.vinculacionFormaPago.pk == 2 and 
        parametro.vinculacionPendientePago and 
        parametro.vinculacionPendientePago > 0):
        
        cuotas_pagas_vinculacion = HistorialPagos.objects.filter(
            asociado=id_asociado,
            mesPago=9995,
            estadoRegistro=True
        ).count()
        
        if cuotas_pagas_vinculacion >= parametro.vinculacionCuotas:
            valor_vinculacion = parametro.vinculacionPendientePago
        elif cuotas_pagas_vinculacion == parametro.vinculacionCuotas - 1:
            valor_vinculacion = parametro.vinculacionPendientePago
        elif parametro.vinculacionPendientePago < parametro.vinculacionValor:
            valor_vinculacion = parametro.vinculacionPendientePago
        else:
            valor_vinculacion = parametro.vinculacionValor
    
    # ========================================================================
    # ← NUEVO: OBTENER DESGLOSE DE SALDOS
    # ========================================================================
    
    desglose_saldos = ConsultaSaldosDetalladosService.obtener_desglose_completo_saldos(
        id_asociado, 
        creditos_info, 
        ventas_home_info
    )
    
    # Validación: el total del desglose debe coincidir con saldoDiferencia
    if abs(desglose_saldos['total'] - saldo_diferencia) > 1:  # Tolerancia de 1 peso por redondeos
        print(f"⚠️ ADVERTENCIA: Discrepancia en saldos")
        print(f"   Desglose total: {desglose_saldos['total']}")
        print(f"   Saldo diferencia: {saldo_diferencia}")
    
    # ========================================================================
    # ← NUEVO: CONSTRUIR CONCEPTOS DETALLADOS CON SALDOS
    # ========================================================================
    
    conceptos_detallados = ConstructorConceptosDetalladosService.construir_conceptos_completos(
        # Datos básicos
        mes=mes,
        parametro=parametro,
        tarifa_asociado=tarifa_asociado,
        id_asociado=id_asociado,
        # Cuotas y valores
        cuota_periodica=cuota_periodica,
        cuota_coohop=cuota_coohop,
        cuotas_vencidas=cuotas_vencidas,
        cuota_periodica_total=cuota_periodica_total,
        # Listas de objetos
        mascotas=mascotas,
        beneficiarios=beneficiarios,
        repatriacion_titular=repatriacion_titular,
        convenios_normales=convenios_normales,
        creditos_info=creditos_info,
        ventas_home_info=ventas_home_info,
        seguro_vida=seguro_vida,
        # Valores calculados
        valor_unitario_mascota=valor_unitario_mascota,
        valor_unitario_repatriacion=valor_unitario_repatriacion,
        valor_gasolina=valor_gasolina,
        valores_adicionales=valores_adicionales,
        # Estados y configuraciones
        meses_pagados=meses_pagados,
        saldos=saldos,
        # ← NUEVO: Desglose de saldos
        desglose_saldos=desglose_saldos
    )
    
    # ========================================================================
    # ← CAMBIO: CALCULAR TOTALES DESDE CONCEPTOS DETALLADOS
    # ========================================================================
    
    # Calcular pago total desde los conceptos (para consistencia)
    pago_total_calculado = sum(concepto['total_a_pagar'] for concepto in conceptos_detallados)
    
    # Consolidar valores vencidos (mantener compatibilidad con código existente)
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
    pago_total = pago_total_calculado  # ← CAMBIO: Usar el calculado desde conceptos
    mensaje = ""
    
    # CASO 1: Tiene cuotas vencidas
    if cuotas_vencidas > 0:
        valor_vencido, _, mensaje = CalculadoraSaldosService.calcular_pago_con_saldo(
            cuota_periodica_total,
            saldo_diferencia,
            valores_vencidos_consolidados,
            valor_total_convenios
        )
        # pago_total ya viene calculado desde conceptos_detallados
    
    # CASO 2: Está al día (sin cuotas vencidas ni adelantadas)
    elif cuotas_adelantadas == 0:
        saldo, valor_vencido, _, mensaje = CalculadoraSaldosService.calcular_estado_al_dia(
            tarifa_asociado, saldo_diferencia
        )
        # pago_total ya viene calculado desde conceptos_detallados
    
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
        
        # Créditos
        "creditos": creditos_info,
        "ventasHomeElements": ventas_home_info,
        "valorTotalCreditos": valor_total_creditos,
        
        # Vinculación
        "vinculacion": {
            "activa": (parametro.vinculacionFormaPago and 
                      parametro.vinculacionFormaPago.pk == 2 and 
                      parametro.vinculacionPendientePago and 
                      parametro.vinculacionPendientePago > 0),
            "cuotas_totales": parametro.vinculacionCuotas or 0,
            "valor_cuota": parametro.vinculacionValor or 0,
            "pendiente_pago": parametro.vinculacionPendientePago or 0,
        },
        
        # Totales y saldos
        "pagoTotal": pago_total,  # ← CAMBIO: Ahora viene desde conceptos_detallados
        "saldo": saldo,
        "saldoDiferencia": saldo_diferencia,
        "mensaje": mensaje,
        
        # ← NUEVO: Desglose de saldos detallado
        "desgloseSaldos": desglose_saldos,
        
        # Beneficiarios y mascotas
        "objBeneficiario": beneficiarios,
        "cuentaBeneficiario": beneficiarios.count(),
        "cuentaBeneficiarioConRepatriacion": sum(1 for b in beneficiarios if b.repatriacion),
        "objMascota": mascotas,
        "cuentaMascota": mascotas.count(),
        "objRepatriacionTitular": repatriacion_titular,
        "objSeguroVida": seguro_vida,
        
        # Convenios
        "objConvenio": convenios_normales,
        "convenioGasolina": convenio_gasolina_info,
        
        # ← CAMBIO: Conceptos detallados ahora incluyen saldos y total_a_pagar
        "conceptos_detallados": conceptos_detallados,
        
        # Vista
        "vista": 0,
    }
    
    return context

