from rest_framework.response import Response
from rest_framework.decorators import api_view
from asociado.models import TarifaAsociado

@api_view(['GET'])
def obtener_total_tarifa(request, pkAsociado):
    try:
        tarifa = TarifaAsociado.objects.get(asociado_id=pkAsociado)
        return Response({'total': tarifa.total})
    except TarifaAsociado.DoesNotExist:
        return Response({"error": "No se encontró la tarifa para el asociado"}, status=404)