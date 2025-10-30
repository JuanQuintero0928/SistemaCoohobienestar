from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.dateparse import parse_date
from asociado.models import Asociado

def asignar_campos(obj, data, campos, upper=False, enteros=False, fechas=False, relaciones=None):
    """
    Asigna dinámicamente los valores de un diccionario (ej: request.POST) a los campos de un modelo.
    
    :param obj: instancia del modelo a modificar
    :param data: diccionario con los datos (ej. request.POST)
    :param campos: lista de nombres de campos a asignar
    :param upper: convierte a mayúsculas si es True
    :param enteros: convierte a int si es True
    :param fechas: convierte a date si es True
    :param relaciones: dict con {'nombre_campo': ModeloRelacionado}
    """
    for campo in campos:
        valor = data.get(campo)

        # Si el valor viene vacío o "0", lo tratamos como None
        if not valor or valor == "0":
            setattr(obj, campo, None)
            continue

        # Conversión por tipo
        if upper:
            setattr(obj, campo, valor.upper())
        elif enteros:
            try:
                setattr(obj, campo, int(valor.replace(".", "")))
            except ValueError:
                setattr(obj, campo, None)
        elif fechas:
            try:
                setattr(obj, campo, datetime.strptime(valor, "%Y-%m-%d").date())
            except ValueError:
                setattr(obj, campo, None)
        else:
            setattr(obj, campo, valor)

    # Manejo de relaciones (ForeignKey)
    if relaciones:
        for campo, modelo in relaciones.items():
            valor = data.get(campo)
            if valor and valor != "0":
                setattr(obj, campo, modelo.objects.get(pk=valor))
            else:
                setattr(obj, campo, None)


@require_POST
def actualizar_fecha_actualizacion(request, asociado_id):
    try:
        nueva_fecha = request.POST.get("fechaActualizacionDatos")
        if not nueva_fecha:
            return JsonResponse({"error": "Fecha no proporcionada"}, status=400)

        fecha_parseada = parse_date(nueva_fecha)
        if not fecha_parseada:
            return JsonResponse({"error": "Formato de fecha inválido"}, status=400)

        asociado = Asociado.objects.get(id=asociado_id)
        asociado.fechaActualizacionDatos = fecha_parseada
        asociado.save()

        return JsonResponse({"success": True, "fecha": fecha_parseada.strftime("%Y-%m-%d")})

    except Asociado.DoesNotExist:
        return JsonResponse({"error": "Asociado no encontrado"}, status=404)
