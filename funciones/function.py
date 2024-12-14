import datetime, csv
from urllib import request
from zoneinfo import ZoneInfo
from historico.models import HistorialPagos

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

            # print("Fila leída:", row)
            registros.append(
                HistorialPagos(
                    asociado_id=int(row['asociado_id']),  # Relación con el modelo `Asociado`
                    mesPago_id=int(row['mesPago_id']),  # Relación con el modelo `MesTarifa`
                    fechaPago=row['fechaPago'] or None,
                    valorPago=int(row['valorPago']),
                    aportePago=int(row['aportePago']),
                    bSocialPago=int(row['bSocialPago']),
                    mascotaPago=int(row['mascotaPago']) if row['mascotaPago'] else None,
                    repatriacionPago=int(row['repatriacionPago']) if row['repatriacionPago'] else None,
                    seguroVidaPago=int(row['seguroVidaPago']) if row['seguroVidaPago'] else None,
                    adicionalesPago=int(row['adicionalesPago']) if row['adicionalesPago'] else None,
                    coohopAporte=int(row['coohopAporte']) if row['coohopAporte'] else None,
                    coohopBsocial=int(row['coohopBsocial']) if row['coohopBsocial'] else None,
                    convenioPago=int(row['convenioPago']) if row['convenioPago'] else None,
                    diferencia=int(row['diferencia']) if row['diferencia'] else None,
                    formaPago_id=int(row['formaPago_id']),  # Relación con el modelo `FormaPago`
                    userCreacion_id=user_creacion_id,  # Relación con `User`
                    estadoRegistro=True,  # Convertir a booleano
                )
            )
    except Exception as e:
        raise ValueError(f"Error procesando el archivo CSV: {e}")
    return registros
