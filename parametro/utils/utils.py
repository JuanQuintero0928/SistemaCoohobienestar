from django.http import JsonResponse
from datetime import timedelta
from ..models import MesTarifa


def mes_tarifa_info(request, pk):
    """
    Funcion utilizada obtener mediante por medio del id del modelo mesTarifa la fecha final
    Utilizada para la adecuada vista de la tabla de amortizacion
    """
    mes = MesTarifa.objects.get(pk=pk)
    fecha_modificada = mes.fechaFinal

    if fecha_modificada.day > 30:
        fecha_modificada = mes.fechaFinal - timedelta(days=1)

    return JsonResponse({"fechaInicio": fecha_modificada.strftime("%Y-%m-%d")})


def funcion_mes_tarifa_info(pk):
    """
    Funcion para generar pdf de tabla de amortizacion
    """
    mes = MesTarifa.objects.get(pk=pk)
    fecha_modificada = mes.fechaFinal

    if fecha_modificada.day > 30:
        fecha_modificada = mes.fechaFinal - timedelta(days=1)

    return fecha_modificada.strftime("%Y-%m-%d")
