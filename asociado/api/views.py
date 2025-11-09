from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from datetime import date
from django.db.models import Value
from django.db.models.functions import Concat, Coalesce
from asociado.models import (
    TarifaAsociado,
    Asociado,
    Laboral,
    Financiera,
    ParametroAsociado,
)
from beneficiario.models import Beneficiario, Mascota
from historico.models import HistoricoAuxilio, HistoricoCredito
from credito.models import Codeudor
from asociado.utils.utils import generar_radicado


@api_view(["GET"])
def obtener_total_tarifa(request, pkAsociado):
    try:
        tarifa = TarifaAsociado.objects.get(asociado_id=pkAsociado)
        return Response({"total": tarifa.total})
    except TarifaAsociado.DoesNotExist:
        return Response(
            {"error": "No se encontró la tarifa para el asociado"}, status=404
        )


def obtener_datos_formato_registro(request, asociado_id, tipo_formato):
    try:
        hoy = date.today()
        datos = {
            "id": asociado_id,
            "fechaFormateada": hoy.strftime("%d/%m/%Y"),
            **datos_modelo_asociado(asociado_id),
            **datos_modelo_laboral(asociado_id),
            **datos_modelo_financiera(asociado_id),
            **datos_modelo_parametro_asociado(asociado_id),
        }
        radicado = generar_radicado(asociado_id, tipo_formato)
        datos["numeroRadicado"] = radicado
        print(datos)
        return JsonResponse(datos)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def obtener_datos_servicios_exequiales(request, asociado_id, tipo_formato):
    try:
        hoy = date.today()
        datos = {
            "id": asociado_id,
            "fechaFormateada": hoy.strftime("%d/%m/%Y"),
            **datos_modelo_asociado(asociado_id),
            **datos_modelo_beneficiarios(asociado_id),
            **datos_modelo_mascota(asociado_id),
        }
        radicado = generar_radicado(asociado_id, tipo_formato)
        datos["numeroRadicado"] = radicado
        return JsonResponse(datos)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def obtener_datos_auxilio_economico(request, asociado_id, tipo_formato, auxilio_id):
    try:
        hoy = date.today()
        datos = {
            "id": asociado_id,
            "fechaFormateada": hoy.strftime("%d/%m/%Y"),
            **datos_modelo_asociado(asociado_id),
            **datos_modelo_historicoAuxilio(auxilio_id),
        }
        radicado = generar_radicado(asociado_id, tipo_formato)
        datos["numeroRadicado"] = radicado
        return JsonResponse(datos)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def obtener_datos_solicitud_credito(request, asociado_id, tipo_formato, credito_id):
    try:
        hoy = date.today()
        datos = {
            "id": asociado_id,
            "fechaFormateada": hoy.strftime("%d/%m/%Y"),
            **datos_modelo_asociado(asociado_id),
            **datos_modelo_laboral(asociado_id),
            **datos_modelo_financiera(asociado_id),
            **datos_modelo_parametro_asociado(asociado_id),
            **datos_modelo_historicoCredito(credito_id),
            **datos_modelo_codeudor(credito_id),
        }
        print(datos)
        radicado = generar_radicado(asociado_id, tipo_formato)
        datos["numeroRadicado"] = radicado
        return JsonResponse(datos)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def datos_modelo_asociado(asociado):
    qs_asociado = get_object_or_404(Asociado, id=asociado)
    return {
        "tPersona": (
            "ACTUALIZACION"
            if qs_asociado.fechaIngreso != qs_asociado.fechaActualizacionDatos
            else qs_asociado.tPersona
        ),
        "tAsociado": qs_asociado.tAsociado.concepto,
        "nombre": qs_asociado.nombre,
        "apellido": qs_asociado.apellido,
        "tipoDocumento": qs_asociado.tipoDocumento,
        "numDocumento": qs_asociado.numDocumento,
        "fechaExpedicion": qs_asociado.fechaExpedicion,
        "mpioDoc": qs_asociado.mpioDoc.nombre,
        "nacionalidad": qs_asociado.nacionalidad,
        "genero": qs_asociado.genero,
        "estadoCivil": qs_asociado.estadoCivil,
        "email": qs_asociado.email,
        "fechaNacimiento": qs_asociado.fechaNacimiento,
        "dtoNacimiento": qs_asociado.dtoNacimiento.nombre,
        "mpioNacimiento": qs_asociado.mpioNacimiento.nombre,
        "tipoVivienda": qs_asociado.tipoVivienda,
        "estrato": qs_asociado.estrato,
        "direccion": qs_asociado.direccion,
        "barrio": qs_asociado.barrio,
        "deptoResidencia": qs_asociado.deptoResidencia.nombre,
        "mpioResidencia": qs_asociado.mpioResidencia.nombre,
        "numResidencia": qs_asociado.numResidencia,
        "numCelular": qs_asociado.numCelular,
        "envioInfoCorreo": qs_asociado.envioInfoCorreo,
        "envioInfoMensaje": qs_asociado.envioInfoMensaje,
        "envioInfoWhatsapp": qs_asociado.envioInfoWhatsapp,
        "nivelEducativo": qs_asociado.nivelEducativo,
        "tituloPregrado": qs_asociado.tituloPregrado,
        "tituloPosgrado": qs_asociado.tituloPosgrado,
        "zonaUbicacion": qs_asociado.zonaUbicacion,
        "nPersonasCargo": (
            qs_asociado.nPersonasCargo if qs_asociado.nPersonasCargo is not None else 0
        ),
        "nHijos": qs_asociado.nHijos if qs_asociado.nHijos is not None else 0,
        "cabezaFamilia": qs_asociado.cabezaFamilia,
        "nombreRF": qs_asociado.nombreRF,
        "parentesco": qs_asociado.parentesco,
        "numContacto": qs_asociado.numContacto,
    }


def datos_modelo_laboral(asociado_id):
    qs_laboral = get_object_or_404(Laboral, asociado_id=asociado_id)
    return {
        "ocupacion": qs_laboral.ocupacion,
        "ocupacionEspecifica": qs_laboral.ocupacionOtro,
        "tipoEmpresa": qs_laboral.tipoEmpresa,
        "tipoEmpresaEspecifica": qs_laboral.tipoEmpresaOtro,
        "nombreEmpresa": qs_laboral.nombreEmpresa,
        "cargo": qs_laboral.cargo,
        "tipoContrato": qs_laboral.tipoContrato,
        "fechaInicio": qs_laboral.fechaInicio,
        "fechaTerminacion": qs_laboral.fechaTerminacion,
        "nomRepresenLegal": qs_laboral.nomRepresenLegal,
        "numDocRL": qs_laboral.numDocRL,
        "nomJefeInmediato": qs_laboral.nomJefeInmediato,
        "telefonoJefeInmediato": qs_laboral.telefonoJefeInmediato,
        "direccionLaboral": qs_laboral.direccion,
        "municipioLaboral": getattr(qs_laboral.mpioTrabajo, "nombre", ""),
        "dptoLaboral": getattr(qs_laboral.dptoTrabajo, "nombre", ""),
        "telefonoLaboral": qs_laboral.telefonoLaboral,
        "correoLaboral": qs_laboral.correoLaboral,
        "admRP": qs_laboral.admRP,
        "pep": qs_laboral.pep,
        "activEcono": qs_laboral.activEcono,
        "ciiu": qs_laboral.ciiu,
        "declaraRenta": qs_laboral.declaraRenta,
        "responsableIVA": qs_laboral.responsableIva,
        "regimenTributario": qs_laboral.regimenTributario,
        "banco": qs_laboral.banco,
        "tipoCuenta": qs_laboral.tipoCuenta,
        "numCuenta": qs_laboral.numCuenta,
    }


def datos_modelo_financiera(asociado_id):
    qs_financiera = get_object_or_404(Financiera, asociado_id=asociado_id)
    return {
        "ingrSalario": qs_financiera.ingrSalario,
        "ingrHorasExtras": qs_financiera.ingrHorasExtras,
        "ingrPension": qs_financiera.ingrPension,
        "ingrCompensacion": qs_financiera.ingrCompensacion,
        "ingrHonorarios": qs_financiera.ingrHonorarios,
        "ingrVentas": qs_financiera.ingrVentas,
        "ingrIntereses": qs_financiera.ingrIntereses,
        "ingrGiros": qs_financiera.ingrGiros,
        "ingrArrendamientos": qs_financiera.ingrArrendamientos,
        "ingrOtros": qs_financiera.ingrOtros,
        "ingrDescripcionOtros": qs_financiera.ingrDescripcionOtros,
        "egrArrendamiento": qs_financiera.egrArrendamiento,
        "egrServiciosPublicos": qs_financiera.egrServiciosPublicos,
        "egrAportesSalud": qs_financiera.egrAportesSalud,
        "egrTransporte": qs_financiera.egrTransporte,
        "egrAlimentacion": qs_financiera.egrAlimentacion,
        "egrObligaciones": qs_financiera.egrObligaciones,
        "egrTarjetas": qs_financiera.egrTarjetas,
        "egrCostos": qs_financiera.egrCostos,
        "egrEmbargos": qs_financiera.egrEmbargos,
        "egrOtros": qs_financiera.egrOtros,
        "egrDescripcionOtros": qs_financiera.egrDescripcionOtros,
        "total_ingresos": qs_financiera.total_ingresos,
        "total_egresos": qs_financiera.total_egresos,
        "total_patrimonio": qs_financiera.total_patrimonio,
        "operacionesMonedaExtranjera": qs_financiera.operacionesMonedaExtranjera,
        "operacionesMonedaCuales": qs_financiera.operacionesMonedaCuales,
        "operacionesMonedaTipo": qs_financiera.operacionesMonedaTipo,
        "operacionesMonedaMonto": qs_financiera.operacionesMonedaMonto,
        "operacionesMoneda": qs_financiera.operacionesMoneda,
        "poseeCuentasMonedaExtranjera": qs_financiera.poseeCuentasMonedaExtranjera,
        "poseeCuentasBanco": qs_financiera.poseeCuentasBanco,
        "poseeCuentasCuenta": qs_financiera.poseeCuentasCuenta,
        "poseeCuentasMoneda": qs_financiera.poseeCuentasMoneda,
        "poseeCuentasCiudad": qs_financiera.poseeCuentasCiudad,
        "poseeCuentasPais": qs_financiera.poseeCuentasPais,
    }


def datos_modelo_parametro_asociado(asociado_id):
    qs_parametro = get_object_or_404(ParametroAsociado, asociado_id=asociado_id)
    return {
        "autorizaciondcto": qs_parametro.autorizaciondcto,
    }


def datos_modelo_beneficiarios(asociado_id):
    qs_beneficiario = Beneficiario.objects.filter(
        asociado_id=asociado_id, estadoRegistro=True
    ).values(
        "nombre",
        "apellido",
        "tipoDocumento",
        "numDocumento",
        "parentesco__nombre",
        "fechaNacimiento",
        "repatriacion",
        "ciudadRepatriacion",
        "paisRepatriacion__nombre",
    )
    return {"beneficiarios": list(qs_beneficiario)}


def datos_modelo_mascota(asociado_id):
    qs_mascotas = Mascota.objects.filter(
        asociado_id=asociado_id, estadoRegistro=True
    ).values("nombre", "tipo", "raza", "fechaNacimiento", "vacunasCompletas")
    return {"mascotas": list(qs_mascotas)}


def datos_modelo_historicoAuxilio(auxilio_id):
    qs_historicoAuxilio = HistoricoAuxilio.objects.filter(
        id=auxilio_id, estadoRegistro=True
    ).values(
        "tipoAuxilio__nombre",
        "entidadBancaria",
        "numCuenta",
        "nombre",
        "numDoc",
        "parentesco__nombre",
        "nivelEducativo",
        "anexoOne",
        "anexoTwo",
        "anexoThree",
        "anexoFour",
        "anexoFive",
        "anexoSix",
        "anexoSeven",
        "anexoEight",
    ).first()

    if not qs_historicoAuxilio:
        return {"auxilio": None}
    
    anexos = [
        qs_historicoAuxilio.get(f"anexo{i}")
        for i in ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight"]
        if qs_historicoAuxilio.get(f"anexo{i}")
    ]
    qs_historicoAuxilio["anexos_concat"] = ", ".join(anexos)
    
    return {"auxilio": qs_historicoAuxilio}


def datos_modelo_historicoCredito(credito_id):
    qs_historicoCredito = HistoricoCredito.objects.filter(
        id = credito_id
    ).values(
        "fechaSolicitud",
        "valor",
        "lineaCredito",
        "amortizacion",
        "tasaInteres__porcentaje",
        "medioPago",
        "cuotas",
        "valorCuota",
        "totalCredito",
        "formaDesembolso",
        "banco",
        "numCuenta",
        "tipoCuenta"
    ).first() or {}
    return {"credito": qs_historicoCredito}


def datos_modelo_codeudor(credito_id):
    qs_codeudor = Codeudor.objects.filter(
        historicoCredito_id=credito_id
    ).values(
        "nombre",
        "apellido",
        "tipoDocumento",
        "numDocumento",
        "mpioDoc__nombre",
    ).first() or {}
    return {"codeudor": qs_codeudor}
