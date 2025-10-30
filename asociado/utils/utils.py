from django.utils import timezone
from parametro.models import ConsecutivoRadicado
from asociado.models import RadicadoAsociado, Asociado


def generar_radicado(asociado_id, tipo):
    anio = timezone.now().year
    consecutivo, _ = ConsecutivoRadicado.objects.get_or_create(anio=anio, tipo=tipo)
    consecutivo.ultimo_numero += 1
    consecutivo.save()
    print("llega a la funcion generar_radicado")
    numero_radicado = f"{tipo}-{anio}-{consecutivo.ultimo_numero:04d}"

    # Obtener instancia de Asociado
    asociado = Asociado.objects.get(pk=asociado_id)
    proceso = "VINCULACION" if asociado.fechaIngreso == asociado.fechaActualizacionDatos else "ACTUALIZACION" 

    # Crear registro de radicado
    RadicadoAsociado.objects.create(
        asociado=asociado, tipo=tipo, radicado=numero_radicado, proceso=proceso
    )

    return numero_radicado
