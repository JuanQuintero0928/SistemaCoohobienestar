from django.http import JsonResponse
from datetime import date
from ..models import (
    Empleados,
    HistorialLaboral,
)

def obtener_datos_certificado_laboral(request, empleado_id, tipo_formato):
    try:
        hoy = date.today()
        print(f"Obteniendo datos para certificado laboral: empleado_id={empleado_id}, tipo_formato={tipo_formato}")

        mapa_historial = {
            "CL": datos_modelo_historial_laboral_actual,
            "CLH": datos_modelo_historial_laboral_todos,
        }

        funcion_historial = mapa_historial.get(tipo_formato, datos_modelo_historial_laboral_actual)

        datos = {
            "id": empleado_id,
            "fechaFormateada": hoy.strftime("%d/%m/%Y"),
            **datos_modelo_empleado(empleado_id),
            **funcion_historial(empleado_id),
            }

        return JsonResponse(datos)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def datos_modelo_empleado(empleado_id):
    empleado = Empleados.objects.get(pk=empleado_id)

    return {
        "empleado": {
            "id": empleado.id,
            "nombre": empleado.nombre,
            "apellido": empleado.apellido,
            "tipo_documento": empleado.tipo_documento,
            "documento": empleado.numero_documento,
            "genero": empleado.genero,
        }
    }


def datos_modelo_historial_laboral_actual(empleado_id):
    historial = (
        HistorialLaboral.objects
        .filter(empleado_id=empleado_id, estado_registro=True)
        .values(
            "contrato__nombre",
            "cargo__nombre",
            "modalidad__nombre",
            "tipo_contrato__nombre",
            "salario",
            "fecha_inicio",
            "fecha_fin",
        )
        .last()
    )

    if historial:
        if historial["fecha_inicio"]:
            historial["fecha_inicio"] = historial["fecha_inicio"].strftime("%d/%m/%Y")

        if historial["fecha_fin"]:
            historial["fecha_fin"] = historial["fecha_fin"].strftime("%d/%m/%Y")

    return {
        "historial_laboral": historial if historial else {}
    }


def datos_modelo_historial_laboral_todos(empleado_id):
    historial = (
        HistorialLaboral.objects
        .filter(empleado_id=empleado_id, estado_registro=True)
        .values(
            "contrato__nombre",
            "cargo__nombre",
            "modalidad__nombre",
            "tipo_contrato__nombre",
            "salario",
            "fecha_inicio",
            "fecha_fin",
        ).order_by("fecha_inicio")
    )

    for registro in historial:
        if registro["fecha_inicio"]:
            registro["fecha_inicio"] = registro["fecha_inicio"].strftime("%d/%m/%Y")

        if registro["fecha_fin"]:
            registro["fecha_fin"] = registro["fecha_fin"].strftime("%d/%m/%Y")

    return {
        "historial_laboral": list(historial)
    }