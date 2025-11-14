from django.utils import timezone
from django.db import transaction
from parametro.models import ConsecutivoRadicado
from asociado.models import (
    RadicadoAsociado,
    Asociado,
    ConveniosAsociado,
    RepatriacionTitular,
    TarifaAsociado
)
from beneficiario.models import Beneficiario, Mascota, Coohoperativitos
from historico.models import HistoricoSeguroVida


def generar_radicado(asociado_id, tipo):
    anio = timezone.now().year
    consecutivo, _ = ConsecutivoRadicado.objects.get_or_create(anio=anio, tipo=tipo)
    consecutivo.ultimo_numero += 1
    consecutivo.save()
    numero_radicado = f"{tipo}-{anio}-{consecutivo.ultimo_numero:03d}"

    # Obtener instancia de Asociado
    asociado = Asociado.objects.get(pk=asociado_id)
    proceso = (
        "VINCULACION"
        if asociado.fechaIngreso == asociado.fechaActualizacionDatos
        else "ACTUALIZACION"
    )

    # Crear registro de radicado
    RadicadoAsociado.objects.create(
        asociado=asociado, tipo=tipo, radicado=numero_radicado, proceso=proceso
    )

    return numero_radicado


def inactivar_asociado(asociado_id):
    """
    Desactiva (estadoRegistro=False) todas las entidades relacionadas
    con el asociado: Mascota, Beneficiario, Coohoperativitos, Seguro de Vida
    """
    with transaction.atomic():
        print("llega  ala funcino")
        qs_mascota = Mascota.objects.filter(
            asociado=asociado_id, estadoRegistro=True
        ).update(estadoRegistro=False)

        qs_beneficiario = Beneficiario.objects.filter(
            asociado=asociado_id, estadoRegistro=True
        ).update(estadoRegistro=False)

        qs_coohoperativitos = Coohoperativitos.objects.filter(
            asociado=asociado_id, estadoRegistro=True
        ).update(estadoRegistro=False)

        qs_seguro_vida = HistoricoSeguroVida.objects.filter(
            asociado=asociado_id, estadoRegistro=True
        ).update(estadoRegistro=False)

        qs_convenios = ConveniosAsociado.objects.filter(
            asociado=asociado_id, estadoRegistro=True
        ).update(estadoRegistro=False)

        qs_repatriacion_titular = RepatriacionTitular.objects.filter(
            asociado=asociado_id, estadoRegistro=True
        ).update(estadoRegistro=False)

        TarifaAsociado.objects.filter(asociado=asociado_id).update(
            cuotaAporte=0,
            cuotaBSocial=0,
            cuotaMascota=0,
            cuotaAdicionales=0,
            cuotaRepatriacionBeneficiarios=0,
            cuotaRepatriacionTitular=0,
            cuotaSeguroVida=0,
            cuotaCoohopAporte=0,
            cuotaCoohopBsocial=0,
            cuotaConvenio=0,
            total=0,
            estadoAdicional=False
        )

        return {
            "mascotas": qs_mascota,
            "beneficiarios": qs_beneficiario,
            "coohoperativitos": qs_coohoperativitos,
            "seguro_vida": qs_seguro_vida,
            "convenios": qs_convenios,
            "repatriacion_titular": qs_repatriacion_titular,
        }
