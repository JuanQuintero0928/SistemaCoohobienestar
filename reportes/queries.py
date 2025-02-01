from django.db.models.functions import TruncSecond
from beneficiario.models import Asociado, Mascota, Beneficiario
from asociado.models import RepatriacionTitular

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
    )
    queryBeneficiario = Beneficiario.objects.filter(
        fechaModificacion__range=[fecha_inicial, fecha_final]
    ).annotate(
        fechaModificacion_truncada=TruncSecond('fechaModificacion'),
        fechaCreacion_truncada=TruncSecond('fechaCreacion'),
    )
    queryRepatriacionTitular = RepatriacionTitular.objects.filter(
        fechaRepatriacion__range=[fecha_inicial, fecha_final]
    )

    return {
        "asociadoRetiro": asociadoRetiro,
        "asociadoIngreso": asociadoIngreso,
        "queryMascota": queryMascota,
        "queryBeneficiario": queryBeneficiario,
        "queryRepatriacionTitular": queryRepatriacionTitular
    }