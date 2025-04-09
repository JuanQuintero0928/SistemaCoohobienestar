import datetime, csv
from zoneinfo import ZoneInfo
from historico.models import HistorialPagos
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "No tiene permisos para acceder a esta sección.")
        return redirect('perfil:inicio')

def separarFecha(fecha, parametro):
    from datetime import datetime 
    fechaString = datetime.strptime(fecha, "%Y-%m-%d")
    dia = fechaString.day
    mes = fechaString.month
    año = fechaString.year
    fecha = [año, mes, dia]
    fechaFormato = fechaUtc(año, mes, dia, parametro)
    return fechaFormato

# funcion que pone en formato utc la fecha par evitar advertencias en la consulta
def fechaUtc(año, mes, dia, parametro):
    if parametro == 'inicial':
        fecha = datetime.datetime(año, mes, dia, 00, 00, 00, 000000,  tzinfo=ZoneInfo("America/Guayaquil"))
        return fecha
    elif parametro == 'final':
        fecha = datetime.datetime(año, mes, dia, 23, 59, 59, 999999,  tzinfo=ZoneInfo("America/Guayaquil"))
        # fecha = datetime.datetime(año, mes, dia, 23, 59, 59, 999999,  tzinfo=datetime.timezone.utc)
    else:
        fecha = '00-00-0000'
    return fecha

def procesar_csv(archivo_csv, user_creacion_id):
    registros = []

    # Leer el archivo CSV
    try:
        decoded_file = archivo_csv.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        # Limpia el encabezado para eliminar el carácter BOM
        if reader.fieldnames[0].startswith('\ufeff'):
            reader.fieldnames[0] = reader.fieldnames[0].replace('\ufeff', '')
        # print("encabezado encontrado", reader.fieldnames)

        for row in reader:
            asociado_id = int(row['asociado_id'])
            mesPago_id = int(row['mesPago_id'])

            # Verificar si ya existe un registro con ese asociado_id y mesPago_id
            if HistorialPagos.objects.filter(asociado_id=asociado_id, mesPago_id=mesPago_id).exists():
                raise ValueError(f"El asociado con ID {asociado_id} ya tiene un registro para el mes con ID {mesPago_id}.")

            # Extraer y convertir los campos numéricos
            aporte = int(row['aportePago'])
            bsocial = int(row['bSocialPago'])
            mascota = int(row['mascotaPago']) if row['mascotaPago'] else 0
            repatriacion = int(row['repatriacionPago']) if row['repatriacionPago'] else 0
            seguro = int(row['seguroVidaPago']) if row['seguroVidaPago'] else 0
            adicionales = int(row['adicionalesPago']) if row['adicionalesPago'] else 0
            coohop_aporte = int(row['coohopAporte']) if row['coohopAporte'] else 0
            coohop_bsocial = int(row['coohopBsocial']) if row['coohopBsocial'] else 0
            convenio = int(row['convenioPago']) if row['convenioPago'] else 0
            # credito_home = int(row['creditoHomeElements']) if row.get('creditoHomeElements') else 0
            diferencia = int(row['diferencia']) if row['diferencia'] else 0

            valor_pago = int(row['valorPago'])

            suma_total = (
                aporte + bsocial + mascota + repatriacion + seguro + adicionales +
                coohop_aporte + coohop_bsocial + convenio + diferencia
            )

            if suma_total != valor_pago:
                raise ValueError(f"La suma de los campos no coincide con valorPago ({valor_pago}) "
                                 f"para el asociado ID {asociado_id}, mes ID {mesPago_id}. Suma calculada: {suma_total}")

            registros.append(
                HistorialPagos(
                    asociado_id=asociado_id,
                    mesPago_id=mesPago_id,
                    fechaPago=row['fechaPago'],
                    valorPago=valor_pago,
                    aportePago=aporte,
                    bSocialPago=bsocial,
                    mascotaPago=mascota,
                    repatriacionPago=repatriacion,
                    seguroVidaPago=seguro,
                    adicionalesPago=adicionales,
                    coohopAporte=coohop_aporte,
                    coohopBsocial=coohop_bsocial,
                    convenioPago=convenio,
                    diferencia=diferencia,
                    formaPago_id=int(row['formaPago_id']),
                    userCreacion_id=user_creacion_id,
                    estadoRegistro=True,
                )
            )
    except Exception as e:
        raise ValueError(f"Error procesando el archivo CSV: {e}")
    return registros

def convertirFecha(fecha):
    fecha_objeto = datetime.datetime.strptime(fecha, "%Y-%m-%d")
    return fecha_objeto.strftime("%d-%m-%Y")