import datetime
from zoneinfo import ZoneInfo

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
