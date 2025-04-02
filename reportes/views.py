from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.http import HttpResponse
from django.db.models import Sum, F, Subquery
from datetime import timedelta
from datetime import datetime

from asociado.models import Asociado, ParametroAsociado, TarifaAsociado
from beneficiario.models import Mascota, Beneficiario
from historico.models import HistorialPagos, HistoricoAuxilio, HistoricoCredito
from parametro.models import FormaPago, MesTarifa, TipoAsociado
from .queries import obtenerNovedades, obtenerDescuentoNomina

#Funciones
from funciones.function import separarFecha, convertirFecha

#Libreria para generar el Excel
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
    
class InformacionReporte(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'reporte/informacion.html'
        return render(request, template_name)

class VerModificacionesFecha(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'reporte/modificacionesPorFecha.html'
        return render(request, template_name)
    
    def post(self, request, *args, **kwargs):
        fechaInicialForm = request.POST['fechaInicial']
        fechaFinalForm = request.POST['fechaFinal']
        # funcion que separa año, mes y dia de la fecha ingresada por el usuario.
        fechaInicial = separarFecha(fechaInicialForm, 'inicial')
        fechaFinal = separarFecha(fechaFinalForm, 'final')
        
        # Obtenemos las queries de las novedades
        queries = obtenerNovedades(fechaInicial, fechaFinal)

        template_name = 'reporte/modificacionesPorFecha.html'
        context = {'queries':queries,
                   'post':'yes',
                   'fechaIncialF':fechaInicialForm,
                   'fechaFinalF':fechaFinalForm,
                   }
        return render(request, template_name, context)

class ReporteExcelFecha(TemplateView):
    def get(self, request, *args, **kwargs):
        fechaInicialForm = request.GET.get('fechaInicial')
        fechaFinalForm = request.GET.get('fechaFinal')
        # funcion que separa año, mes y dia de la fecha ingresada por el usuario.
        fechaInicial = separarFecha(fechaInicialForm, 'inicial')
        fechaFinal = separarFecha(fechaFinalForm, 'final')

        # Funcion para formatear la fecha en el formato d-m-Y
        fecha_formateada1 = convertirFecha(fechaInicialForm)
        fecha_formateada2 = convertirFecha(fechaFinalForm)
       
        # Obtenemos las queries de las novedades
        queries = obtenerNovedades(fechaInicial, fechaFinal)

        # Estilos
        bold_font = Font(bold=True, size=16, color="FFFFFF")  # Fuente en negrita, tamaño 12 y color blanco
        bold_font2 = Font(bold=True, size=12, color="000000")  # Fuente en negrita, tamaño 12 y color negro
        alignment_center = Alignment(horizontal="center", vertical="center")  # Alineación al centro
        fill = PatternFill(start_color="85B84C", end_color="85B84C", fill_type="solid")  # Relleno verde sólido

        wb = Workbook() #Creamos la instancia del Workbook
        ws = wb.active
        ws.title = 'Mascotas'
        titulo1 = f"Reporte de Novedades Mascota Funeraria desde {fecha_formateada1} - {fecha_formateada2}"
        ws['A1'] = titulo1    #Casilla en la que queremos poner la informacion
        ws.merge_cells('A1:I1')
        ws['A1'].font = bold_font
        ws['A1'].alignment = alignment_center
        ws['A1'].fill = fill

        ws['A2'] = 'Número registro'
        ws['B2'] = 'Número Documento Titular'
        ws['C2'] = 'Nombre Titular'
        ws['D2'] = 'Mascota'
        ws['E2'] = 'Tipo'
        ws['F2'] = 'Raza'
        ws['G2'] = 'Fecha Nacimiento'
        ws['H2'] = 'Novedad'
        ws['I2'] = 'Fecha Novedad'
     
        bold_font2 = Font(bold=True)
        center_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

        for col in range(1,10):
            cell = ws.cell(row=2, column=col)
            cell.font = bold_font2
            cell.alignment = center_alignment

        ws.column_dimensions['A'].width = 11
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 40
        ws.column_dimensions['D'].width = 14
        ws.column_dimensions['E'].width = 14
        ws.column_dimensions['F'].width = 14
        ws.column_dimensions['G'].width = 14
        ws.column_dimensions['H'].width = 12
        ws.column_dimensions['I'].width = 14
        
        #Inicia el primer registro en la celda numero 3
        cont = 3
        i = 1
        for mascota in queries["queryMascota"]:
            #Row, son las filas , A,B,C,D osea row es igual al contador, y columnas 1,2,3
            ws.cell(row = cont, column = 1).value = i
            ws.cell(row = cont, column = 2).value = int(mascota.asociado.numDocumento)
            ws.cell(row = cont, column = 3).value = f'{mascota.asociado.nombre}' + ' ' + f'{mascota.asociado.apellido}'
            ws.cell(row = cont, column = 4).value = mascota.nombre
            ws.cell(row = cont, column = 5).value = mascota.tipo
            ws.cell(row = cont, column = 6).value = mascota.raza
            ws.cell(row = cont, column = 7).value = mascota.fechaNacimiento.strftime("%d/%m/%Y")
            if mascota.fechaCreacion_truncada == mascota.fechaModificacion_truncada:
                ws.cell(row = cont, column = 8).value = 'Ingreso'
                ws.cell(row = cont, column = 9).value = mascota.fechaIngreso.strftime("%d/%m/%Y")
            elif mascota.fechaCreacion_truncada != mascota.fechaModificacion_truncada:
                if mascota.estadoRegistro == True:
                    ws.cell(row = cont, column = 8).value = 'Modificación'
                    ws.cell(row = cont, column = 9).value = mascota.fechaModificacion.strftime("%d/%m/%Y")
                else:
                    ws.cell(row = cont, column = 8).value = 'Retiro'
                    ws.cell(row = cont, column = 9).value = mascota.fechaRetiro.strftime("%d/%m/%Y")
            i+=1
            cont+=1
        
        # se crea una nueva hoja
        wb.create_sheet('Beneficiarios')  
        # se selecciona la hoja creada
        ws2 = wb['Beneficiarios']
        titulo2 = f"Reporte de Novedades Beneficiarios Funeraria desde {fecha_formateada1} - {fecha_formateada2}"
        ws2['A1'] = titulo2    #Casilla en la que queremos poner la informacion
        ws2.merge_cells('A1:K1')
        ws2['A1'].font = bold_font
        ws2['A1'].alignment = alignment_center
        ws2['A1'].fill = fill

        ws2['A2'] = 'Número Registro'
        ws2['B2'] = 'Número Documento Titular'
        ws2['C2'] = 'Nombre Titular'
        ws2['D2'] = 'Tipo Documento Beneficiario'
        ws2['E2'] = 'Número Documento Beneficiario'
        ws2['F2'] = 'Nombre Beneficiario'
        ws2['G2'] = 'Parentesco'
        ws2['H2'] = 'Fecha Nacimiento'
        ws2['I2'] = 'Repatriación'
        ws2['J2'] = 'Novedad'
        ws2['K2'] = 'Fecha Novedad'

        bold_font2 = Font(bold=True)
        center_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

        for col in range(1,13):
            cell = ws2.cell(row=2, column=col)
            cell.font = bold_font2
            cell.alignment = center_alignment

        ws2.column_dimensions['A'].width = 11
        ws2.column_dimensions['B'].width = 15
        ws2.column_dimensions['C'].width = 40
        ws2.column_dimensions['D'].width = 18
        ws2.column_dimensions['E'].width = 13
        ws2.column_dimensions['F'].width = 40
        ws2.column_dimensions['G'].width = 16
        ws2.column_dimensions['H'].width = 12
        ws2.column_dimensions['I'].width = 15
        ws2.column_dimensions['J'].width = 13
        ws2.column_dimensions['K'].width = 12


        #Inicia el primer registro en la celda numero 3
        cont = 3
        i = 1
        for beneficiario in queries["queryBeneficiario"]:
            #Row, son las filas , A,B,C,D osea row es igual al contador, y columnas 1,2,3
            ws2.cell(row = cont, column = 1).value = i                    
            ws2.cell(row = cont, column = 2).value = int(beneficiario.asociado.numDocumento)
            ws2.cell(row = cont, column = 3).value = f'{beneficiario.asociado.nombre}' + ' ' + f'{beneficiario.asociado.apellido}'
            ws2.cell(row = cont, column = 4).value = beneficiario.tipoDocumento
            ws2.cell(row = cont, column = 5).value = int(beneficiario.numDocumento)
            ws2.cell(row = cont, column = 6).value = f'{beneficiario.nombre}' + ' ' + f'{beneficiario.apellido}'
            ws2.cell(row = cont, column = 7).value = beneficiario.parentesco.nombre
            ws2.cell(row = cont, column = 8).value = beneficiario.fechaNacimiento.strftime("%d/%m/%Y")
            if beneficiario.repatriacion == True:
                ws2.cell(row = cont, column = 9).value = f'{beneficiario.paisRepatriacion.nombre}' + '-' + f'{beneficiario.ciudadRepatriacion}'
            else:
                ws2.cell(row = cont, column = 9).value = ''
            if beneficiario.fechaCreacion_truncada == beneficiario.fechaModificacion_truncada:
                ws2.cell(row = cont, column = 10).value = 'Ingreso'
            elif beneficiario.fechaCreacion_truncada != beneficiario.fechaModificacion_truncada:
                if beneficiario.estadoRegistro == True:
                    ws2.cell(row = cont, column = 10).value = 'Modificación'
                else:
                    ws2.cell(row = cont, column = 10).value = 'Retiro'
            if beneficiario.fechaRetiro != None:
                ws2.cell(row = cont, column = 11).value = beneficiario.fechaRetiro.strftime("%d/%m/%Y")
            elif beneficiario.fechaCreacion_truncada == beneficiario.fechaModificacion_truncada:
                ws2.cell(row = cont, column = 11).value = beneficiario.fechaIngreso.strftime("%d/%m/%Y")
            else:
                ws2.cell(row = cont, column = 11).value = beneficiario.fechaModificacion.strftime("%d/%m/%Y")
            i+=1
            cont+=1
        
        # se crea una nueva hoja
        wb.create_sheet('Asociados')
        # se selecciona la hoja creada
        ws3 = wb['Asociados']
        titulo2 = f"Reporte de Novedades Asociados Funeraria desde {fecha_formateada1} - {fecha_formateada2}"
        ws3['A1'] = titulo2    #Casilla en la que queremos poner la informacion
        ws3.merge_cells('A1:G1')

        ws3['A1'].font = bold_font
        ws3['A1'].alignment = alignment_center
        ws3['A1'].fill = fill

        ws3['A2'] = 'Número registro'
        ws3['B2'] = 'Nombre'
        ws3['C2'] = 'Tipo Documento'
        ws3['D2'] = 'Número Documento'
        ws3['E2'] = 'Fecha Nacimiento'
        ws3['F2'] = 'Novedad'
        ws3['G2'] = 'Fecha'

        bold_font2 = Font(bold=True)
        center_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

        for col in range(1,8):
            cell = ws3.cell(row=2, column=col)
            cell.font = bold_font2
            cell.alignment = center_alignment

        ws3.column_dimensions['A'].width = 11
        ws3.column_dimensions['B'].width = 30
        ws3.column_dimensions['C'].width = 14
        ws3.column_dimensions['D'].width = 13
        ws3.column_dimensions['E'].width = 12
        ws3.column_dimensions['F'].width = 29
        ws3.column_dimensions['G'].width = 12

        #Inicia el primer registro en la celda numero 3
        cont = 3
        i = 1
        for asociado in queries["asociadoRetiro"]:
            #Row, son las filas , A,B,C,D osea row es igual al contador, y columnas 1,2,3
            ws3.cell(row = cont, column = 1).value = i                    
            ws3.cell(row = cont, column = 2).value = f'{asociado.nombre}' + ' ' + f'{asociado.apellido}'
            ws3.cell(row = cont, column = 3).value = asociado.tipoDocumento
            ws3.cell(row = cont, column = 4).value = int(asociado.numDocumento)
            ws3.cell(row = cont, column = 5).value = asociado.fechaNacimiento.strftime("%d/%m/%Y")
            ws3.cell(row = cont, column = 6).value = 'Retiro'
            ws3.cell(row = cont, column = 7).value = asociado.fechaRetiro.strftime("%d/%m/%Y")
            i+=1
            cont+=1
        
        for asociado in queries["asociadoIngreso"]:
            #Row, son las filas , A,B,C,D osea row es igual al contador, y columnas 1,2,3
            ws3.cell(row = cont, column = 1).value = i                    
            ws3.cell(row = cont, column = 2).value = f'{asociado.nombre}' + ' ' + f'{asociado.apellido}'
            ws3.cell(row = cont, column = 3).value = asociado.tipoDocumento
            ws3.cell(row = cont, column = 4).value = int(asociado.numDocumento)
            ws3.cell(row = cont, column = 5).value = asociado.fechaNacimiento.strftime("%d/%m/%Y")
            ws3.cell(row = cont, column = 6).value = 'Ingreso'
            ws3.cell(row = cont, column = 7).value = asociado.fechaIngreso.strftime("%d/%m/%Y")
            i+=1
            cont+=1

        for asociado in queries["queryRepatriacionTitular"]:
            #Row, son las filas , A,B,C,D osea row es igual al contador, y columnas 1,2,3
            ws3.cell(row = cont, column = 1).value = i                    
            ws3.cell(row = cont, column = 2).value = f'{asociado.asociado.nombre}' + ' ' + f'{asociado.asociado.apellido}'
            ws3.cell(row = cont, column = 3).value = asociado.asociado.tipoDocumento
            ws3.cell(row = cont, column = 4).value = int(asociado.asociado.numDocumento)
            ws3.cell(row = cont, column = 5).value = asociado.asociado.fechaNacimiento.strftime("%d/%m/%Y")
            if asociado.estadoRegistro == True:
                ws3.cell(row = cont, column = 6).value = 'Ingreso Repatriación ' + f'{asociado.paisRepatriacion}'
            else:
                ws3.cell(row = cont, column = 6).value = 'Retiro Repatriación ' + f'{asociado.paisRepatriacion}'
            ws3.cell(row = cont, column = 7).value = asociado.fechaRepatriacion.strftime("%d/%m/%Y")
            i+=1
            cont+=1
        

        nombre_archivo = f"Reporte Modificaciones_{fecha_formateada1}-{fecha_formateada2}.xlsx"
        response = HttpResponse(content_type = "application/ms-excel")
        content = "attachment; filename = {0}".format(nombre_archivo)
        response['Content-Disposition'] = content
        wb.save(response)
        return response

class VerPagosFecha(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'reporte/pagosPorFecha.html'
        return render(request, template_name)
    
    def post(self, request, *args, **kwargs):
        fechaInicialForm = request.POST['fechaInicial']
        fechaFinalForm = request.POST['fechaFinal']
        # funcion que separa año, mes y dia de la fecha ingresada por el usuario.
        fechaInicial = separarFecha(fechaInicialForm, 'inicial')
        fechaFinal = separarFecha(fechaFinalForm, 'final')
        # consulta por rango de fecha inicial y final
        queryHistorial = HistorialPagos.objects.filter(
                                fechaPago__range=[fechaInicial, fechaFinal]
                            )
        totalPago = queryHistorial.aggregate(total=Sum('valorPago'))['total'] or 0

        template_name = 'reporte/pagosPorFecha.html'
        return render(request, template_name, {'query':queryHistorial,'post':'yes', 'fechaIncialF':fechaInicialForm, 'fechaFinalF':fechaFinalForm, 'totalPago':totalPago})

class ReporteExcelPago(TemplateView):
    def get(self, request, *args, **kwargs):
        fechaInicialForm = request.GET['fechaInicial']
        fechaFinalForm = request.GET['fechaFinal']
        # funcion que separa año, mes y dia de la fecha ingresada por el usuario.
        fechaInicial = separarFecha(fechaInicialForm, 'inicial')
        fechaFinal = separarFecha(fechaFinalForm, 'final')
        # consulta por rango de fecha inicial y final
        queryPagos = HistorialPagos.objects.filter(
            fechaPago__range=[fechaInicial, fechaFinal]
        )

        # Convertir la cadena de fecha a un objeto datetime
        fecha_objeto1 = datetime.strptime(fechaInicialForm, "%Y-%m-%d")
        # Formatear la fecha en el formato d-m-Y
        fecha_formateada1 = fecha_objeto1.strftime("%d-%m-%Y")
        # Convertir la cadena de fecha a un objeto datetime
        fecha_objeto2 = datetime.strptime(fechaFinalForm, "%Y-%m-%d")
        # Formatear la fecha en el formato d-m-Y
        fecha_formateada2 = fecha_objeto2.strftime("%d-%m-%Y")

        # Estilos
        bold_font = Font(bold=True, size=16, color="FFFFFF")  # Fuente en negrita, tamaño 12 y color blanco
        bold_font2 = Font(bold=True, size=12, color="000000")  # Fuente en negrita, tamaño 12 y color negro
        alignment_center = Alignment(horizontal="center", vertical="center")  # Alineación al centro
        fill = PatternFill(start_color="85B84C", end_color="85B84C", fill_type="solid")  # Relleno verde sólido

        wb = Workbook() #Creamos la instancia del Workbook
        ws = wb.active
        ws.title = 'Pagos'
        titulo1 = f"Reporte de Pagos desde {fecha_formateada1} - {fecha_formateada2}"
        ws['A1'] = titulo1    #Casilla en la que queremos poner la informacion
        ws.merge_cells('A1:N1')
        ws['A1'].font = bold_font
        ws['A1'].alignment = alignment_center
        ws['A1'].fill = fill

        ws['A2'] = 'Número Registro'
        ws['B2'] = 'Número Documento'
        ws['C2'] = 'Nombre Completo'
        ws['D2'] = 'Mes Pago'
        ws['E2'] = 'Valor Pago'
        ws['F2'] = 'Aporte'
        ws['G2'] = 'Bienestar Social'
        ws['H2'] = 'Mascota'
        ws['I2'] = 'Repatriación'
        ws['J2'] = 'Seguro Vida'
        ws['K2'] = 'Adicionales'
        ws['L2'] = 'Coohoperativitos'
        ws['M2'] = 'Diferencia'
        ws['N2'] = 'Forma Pago'
     
        bold_font2 = Font(bold=True)
        center_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

        for col in range(1,15):
            cell = ws.cell(row=2, column=col)
            cell.font = bold_font2
            cell.alignment = center_alignment

        ws.column_dimensions['A'].width = 11
        ws.column_dimensions['B'].width = 14
        ws.column_dimensions['C'].width = 30
        ws.column_dimensions['D'].width = 16
        ws.column_dimensions['E'].width = 14
        ws.column_dimensions['F'].width = 12
        ws.column_dimensions['G'].width = 12
        ws.column_dimensions['H'].width = 12
        ws.column_dimensions['I'].width = 12
        ws.column_dimensions['J'].width = 12
        ws.column_dimensions['K'].width = 12
        ws.column_dimensions['L'].width = 16
        ws.column_dimensions['M'].width = 12
        ws.column_dimensions['N'].width = 12

        #Inicia el primer registro en la celda numero 3
        cont = 3
        i = 1
        for pago in queryPagos:
            #Row, son las filas , A,B,C,D osea row es igual al contador, y columnas 1,2,3
            ws.cell(row = cont, column = 1).value = i                    
            ws.cell(row = cont, column = 2).value = int(pago.asociado.numDocumento)
            ws.cell(row = cont, column = 3).value = f'{pago.asociado.nombre}' + ' ' + f'{pago.asociado.apellido}'
            ws.cell(row = cont, column = 4).value = pago.mesPago.concepto
            ws.cell(row = cont, column = 5).value = pago.valorPago
            ws.cell(row = cont, column = 6).value = pago.aportePago
            ws.cell(row = cont, column = 7).value = pago.bSocialPago
            ws.cell(row = cont, column = 8).value = pago.mascotaPago
            ws.cell(row = cont, column = 9).value = pago.repatriacionPago
            ws.cell(row = cont, column = 10).value = pago.seguroVidaPago
            ws.cell(row = cont, column = 11).value = pago.adicionalesPago
            ws.cell(row = cont, column = 12).value = pago.coohopAporte + pago.coohopBsocial
            ws.cell(row = cont, column = 13).value = pago.diferencia
            ws.cell(row = cont, column = 14).value = pago.formaPago.formaPago
            i+=1
            cont+=1

        nombre_archivo = f"Reporte Pago_{fecha_formateada1}-{fecha_formateada2}.xlsx"
        response = HttpResponse(content_type = "application/ms-excel")
        content = "attachment; filename = {0}".format(nombre_archivo)
        response['Content-Disposition'] = content
        wb.save(response)
        return response
    
class FormatoExtracto(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'reporte/reporteExtracto.html'
        mes = MesTarifa.objects.all()
        return render(request, template_name, {'mes':mes})


    def post(self, request, *args, **kwargs):
        template_name = 'reporte/generarExtracto.html'
        
        objAsoc = Asociado.objects.exclude(estadoAsociado = 'RETIRO')
        mesExtracto = request.POST['mesExtracto']
        asociados = []
        for asociado in objAsoc:
            parametro = ParametroAsociado.objects.get(asociado = asociado.pk)
            mes = MesTarifa.objects.get(pk = mesExtracto)
            # Entra al except cuando un asociado no ha realizado ningun pago y no existe informacion en la query
            try:
                # se valida si el primer mes de pago es igual o mayor a la seleccion del form
                if mes.pk >= parametro.primerMes.pk:
                    
                    # Formato 4
                    fechaCorte = timedelta(15) + mes.fechaInicio
                    objTarifaAsociado = TarifaAsociado.objects.get(asociado = asociado.pk)
                    
                    cuotaPeriodica = objTarifaAsociado.cuotaAporte + objTarifaAsociado.cuotaBSocial
                    cuotaCoohop = objTarifaAsociado.cuotaCoohopAporte + objTarifaAsociado.cuotaCoohopBsocial
                    
                    # Obtener los meses pagados por el asociado, excluyendo los registros 9998 y 9999
                    mesesPagados = (HistorialPagos.objects
                                        .filter(asociado=asociado.pk)
                                        .exclude(pk__in=[9998, 9999])
                                        .values_list('mesPago', flat=True))
                    
                    # Obtener el rango de meses relevante
                    queryParamAsoc = ParametroAsociado.objects.get(asociado=asociado.pk)
                    queryMes = (MesTarifa.objects
                                    .exclude(pk__in=Subquery(mesesPagados))
                                    .exclude(pk__in=[9998, 9999])  # Excluir también en MesTarifa
                                    .filter(pk__gte=queryParamAsoc.primerMes.pk, pk__lte=mes.pk))
                    
                    queryParamAsoc = ParametroAsociado.objects.get(asociado = asociado.pk)
                  
                    # Inicializar contadores
                    cuotaVencida = 0
                    cuotaAdelantada = 0
                    cuotaPeriodicaTotal = 0

                    # Identificar meses faltantes
                    mesesFaltantes = queryMes.exclude(pk__in=mesesPagados)
                    
                    # Calcular cuotas vencidas y sumar las cuotas de meses pendientes
                    for mesFaltante in mesesFaltantes:
                        cuotaPeriodicaTotal += mesFaltante.aporte + mesFaltante.bSocial
                        cuotaVencida += 1

                    # Calcular cuotas adelantadas
                    for mesPagado in mesesPagados:
                        if mesPagado > mes.pk:  # Si el mes pagado está fuera del rango actual, es adelantado
                            cuotaAdelantada += 1

                    pagoTotal = cuotaPeriodicaTotal
                     
                    # variables iniciacion
                    saldo = 0
                    valorVencido = 0
                    valorVencidoMasc = 0
                    valorVencidoRep = 0
                    valorVencidoSeg = 0
                    valorVencidoAdic = 0
                    valorVencidoCoohop = 0
                    mensaje = ""
                    
                    # query mostrar beneficiarios y mascotas
                    objBeneficiario = Beneficiario.objects.filter(asociado = asociado.pk, estadoRegistro = True)
                    cuentaBeneficiario = len(objBeneficiario)
                    objMascota = Mascota.objects.filter(asociado = asociado.pk, estadoRegistro = True)
                    cuentaMascota = len(objMascota)
                    # query que suma la diferencia de pagos
                    querySaldoTotal = HistorialPagos.objects.filter(asociado = asociado.pk).aggregate(total=Sum('diferencia'))
                    for valor in querySaldoTotal.values():
                        # variable que guarda la diferencia en los saldos(0=esta al dia, > a 0, saldo favor, < a 0, saldo pendiente)
                        saldoDiferencia = valor
                    
                    # condicional si esta atrasado
                    if cuotaVencida > 0:
                        if objTarifaAsociado.cuotaMascota > 0:
                            valorVencidoMasc = cuotaVencida * objTarifaAsociado.cuotaMascota
                        if objTarifaAsociado.cuotaRepatriacion > 0:
                            valorVencidoRep = cuotaVencida * objTarifaAsociado.cuotaRepatriacion
                        if objTarifaAsociado.cuotaSeguroVida > 0:
                            valorVencidoSeg = cuotaVencida * objTarifaAsociado.cuotaSeguroVida
                        if objTarifaAsociado.cuotaAdicionales > 0:
                            valorVencidoAdic = cuotaVencida * objTarifaAsociado.cuotaAdicionales
                        if objTarifaAsociado.cuotaCoohopAporte > 0:
                            valorVencidoCoohop = cuotaVencida * (objTarifaAsociado.cuotaCoohopAporte + objTarifaAsociado.cuotaCoohopBsocial)
                    
                        if saldoDiferencia > 0:
                            # saldo a favor
                            valorVencido = cuotaPeriodicaTotal - saldoDiferencia
                            pagoTotal = valorVencido + valorVencidoMasc + valorVencidoRep + valorVencidoSeg + valorVencidoAdic + valorVencidoCoohop
                            mensaje = "Tiene un saldo a favor de $" + str(saldoDiferencia)
                        elif saldoDiferencia < 0:
                            # saldo a pagar
                            valorVencido = cuotaPeriodicaTotal - saldoDiferencia
                            pagoTotal = valorVencido + valorVencidoMasc + valorVencidoRep + valorVencidoSeg + valorVencidoAdic + valorVencidoCoohop
                            mensaje = "Tiene un saldo pendiente por pagar de $" + str((saldoDiferencia*-1))
                        else:
                            # saldo en 0
                            valorVencido = cuotaPeriodicaTotal
                            pagoTotal = valorVencido + valorVencidoMasc + valorVencidoRep + valorVencidoSeg + valorVencidoAdic + valorVencidoCoohop
                        asociados.append({'pkAsociado':asociado.pk, 'fechaCorte':fechaCorte,'objAsoc':asociado, 'objTarifaAsociado':objTarifaAsociado, 'cuotaPeriodica':cuotaPeriodica, 'cuotaCoohop':cuotaCoohop, 'cuotaVencida':cuotaVencida, 'valorVencido':valorVencido, 'valorVencidoMasc':valorVencidoMasc, 'valorVencidoRep':valorVencidoRep, 'valorVencidoSeg':valorVencidoSeg, 'valorVencidoAdic':valorVencidoAdic, 'valorVencidoCoohop':valorVencidoCoohop, 'pagoTotal':pagoTotal,'mes':mes, 'objBeneficiario':objBeneficiario, 'cuentaBeneficiario':cuentaBeneficiario, 'objMascota':objMascota, 'cuentaMascota':cuentaMascota, 'formato':5, 'saldo':saldo, 'mensaje':mensaje})
                        
                    # condicional si esta al dia y no tiene meses pendientes en los pagos
                    elif cuotaAdelantada == 0 and cuotaVencida == 0:
                        
                        valorMensual = objTarifaAsociado.cuotaAporte + objTarifaAsociado.cuotaBSocial + objTarifaAsociado.cuotaMascota + objTarifaAsociado.cuotaRepatriacion + objTarifaAsociado.cuotaSeguroVida + objTarifaAsociado.cuotaAdicionales + objTarifaAsociado.cuotaCoohopAporte + objTarifaAsociado.cuotaCoohopBsocial                
                    
                        # se valida si en el ultimo pago no hay diferencia
                        if saldoDiferencia == 0:
                            # no existen saldos
                            saldo = valorMensual
                        elif saldoDiferencia > 0:
                            # existe saldo positivo
                            saldo = valorMensual + saldoDiferencia
                        else:
                            # existe saldo negativo, al estar negativo en la bd, se suma lo que debe
                            saldo = valorMensual + saldoDiferencia
                        
                        # comparamos el valor que va en la casilla saldo frente a lo que realmente paga el asociado
                        if saldo == valorMensual:
                            # si es igual, se muestra 0 en el extracto a pagar
                            pagoTotal = 0
                            valorVencido = 0
                        elif saldo > valorMensual:
                            # si saldo es mayor, es porque tiene un saldo a favor, se muestra 0 y se envia mensaje
                            valorVencido = 0
                            pagoTotal = 0
                            dif = saldo - valorMensual
                            mensaje = 'Tiene un saldo a favor de ' + str(dif) + '.'
                        else:
                            # si saldo es menor, es porque tiene un saldo pendiente x pagar, se muestra el valor y se envia mensaje
                            valorVencido = valorMensual - saldo
                            pagoTotal = valorMensual - saldo
                            dif = valorMensual - saldo
                            mensaje = 'Tiene un saldo pendiente por pagar de ' + str(dif) + '.'
                        asociados.append({'pkAsociado':asociado.pk, 'fechaCorte':fechaCorte,'objAsoc':asociado, 'objTarifaAsociado':objTarifaAsociado, 'cuotaPeriodica':cuotaPeriodica, 'cuotaCoohop':cuotaCoohop, 'cuotaVencida':cuotaVencida, 'valorVencido':valorVencido, 'valorVencidoMasc':valorVencidoMasc, 'valorVencidoRep':valorVencidoRep, 'valorVencidoSeg':valorVencidoSeg, 'valorVencidoAdic':valorVencidoAdic, 'valorVencidoCoohop':valorVencidoCoohop, 'pagoTotal':pagoTotal,'mes':mes, 'objBeneficiario':objBeneficiario, 'cuentaBeneficiario':cuentaBeneficiario, 'objMascota':objMascota, 'cuentaMascota':cuentaMascota, 'formato':5, 'saldo':saldo, 'mensaje':mensaje})
                    
                    # condicional si esta adelantado
                    else:
                        pagoTotal = 0
                        # obtenemos el valor total que tiene pago el asociado, desde el mes seleccionado en la query hasta el pago en la bd
                        query = (HistorialPagos.objects
                                        .exclude(mesPago__in=[9998, 9999])
                                        .filter(mesPago__gte = mes.pk, asociado = kwargs['pkAsociado'])
                                        .aggregate(total=Sum('valorPago')))
                        
                        # Obtenemos el saldo actual del asociado, del mes seleccionado hasta el ultimo pago
                        for valor in query.values():
                            saldoActual = valor
                        
                        # si tiene un saldo en diferencia, se calcula el saldo
                        if saldoDiferencia > 0:
                            saldo = saldoActual + saldoDiferencia
                        elif saldoDiferencia < 0:
                            saldo = saldoActual + saldoDiferencia
                        else:
                            saldo = saldoActual

                        # Obtenemos el pk de la tabla de pagos con el pk del pago mas alto
                        max_mes_pago_pk = (HistorialPagos.objects
                                        .exclude(mesPago__in=[9998, 9999])
                                        .filter(asociado = kwargs['pkAsociado'])
                                        .aggregate(max_mes_pk=Max('mesPago'))['max_mes_pk'])
                        
                        # Obtenemos el nombre del mes con el pk del pago mas alto
                        obj_historial_pago = (HistorialPagos.objects
                                                    .filter(mesPago=max_mes_pago_pk, asociado=kwargs['pkAsociado'])
                                                    .first())
                        
                        mensaje = "Tiene Pago hasta el mes de " + obj_historial_pago.mesPago.concepto + "."
                        
                        asociados.append({'pkAsociado':asociado.pk, 'fechaCorte':fechaCorte,'objAsoc':asociado, 'objTarifaAsociado':objTarifaAsociado, 'cuotaPeriodica':cuotaPeriodica, 'cuotaCoohop':cuotaCoohop, 'cuotaVencida':cuotaVencida, 'valorVencido':valorVencido, 'valorVencidoMasc':valorVencidoMasc, 'valorVencidoRep':valorVencidoRep, 'valorVencidoSeg':valorVencidoSeg, 'valorVencidoAdic':valorVencidoAdic, 'valorVencidoCoohop':valorVencidoCoohop, 'pagoTotal':pagoTotal,'mes':mes, 'objBeneficiario':objBeneficiario, 'cuentaBeneficiario':cuentaBeneficiario, 'objMascota':objMascota, 'cuentaMascota':cuentaMascota, 'formato':5, 'saldo':saldo, 'mensaje':mensaje})
                
            # si no hay pagos en la bd
            except Exception as e:
                # query mostrar beneficiarios y mascotas
                objBeneficiario = Beneficiario.objects.filter(asociado = asociado.pk, estadoRegistro = True)
                saldo = 0 
                cuentaBeneficiario = len(objBeneficiario)
                objMascota = Mascota.objects.filter(asociado = asociado.pk, estadoRegistro = True)
                cuentaMascota = len(objMascota)
                valorVencidoMasc = objTarifaAsociado.cuotaMascota
                valorVencidoRep = objTarifaAsociado.cuotaRepatriacion
                valorVencidoSeg = objTarifaAsociado.cuotaSeguroVida
                valorVencidoAdic = objTarifaAsociado.cuotaAdicionales
                valorVencidoCoohop = objTarifaAsociado.cuotaCoohopAporte + objTarifaAsociado.cuotaCoohopBsocial
                # obtenemos el parametro del primer mes q debe pagar
                if cuotaVencida == 0:
                    # mes seleccionado igual al parametro.primerMes
                    valorVencido = cuotaPeriodicaTotal
                    pagoTotal = valorVencido + valorVencidoMasc + valorVencidoRep + valorVencidoSeg + valorVencidoAdic + valorVencidoCoohop
                elif cuotaVencida > 0:
                    # mes adelantado al parametro.primerMes
                    valorVencido = cuotaPeriodicaTotal
                    valorVencidoMasc = objTarifaAsociado.cuotaMascota * cuotaVencida
                    valorVencidoRep = objTarifaAsociado.cuotaRepatriacion * cuotaVencida
                    valorVencidoSeg = objTarifaAsociado.cuotaSeguroVida * cuotaVencida
                    valorVencidoAdic = objTarifaAsociado.cuotaAdicionales * cuotaVencida
                    valorVencidoCoohop = (objTarifaAsociado.cuotaCoohopAporte + objTarifaAsociado.cuotaCoohopBsocial) * cuotaVencida
                    pagoTotal = valorVencido + valorVencidoMasc + valorVencidoRep + valorVencidoSeg + valorVencidoAdic + valorVencidoCoohop
                else:
                    pass
                asociados.append({'pkAsociado':asociado.pk, 'fechaCorte':fechaCorte,'objAsoc':asociado, 'objTarifaAsociado':objTarifaAsociado, 'cuotaPeriodica':cuotaPeriodica, 'cuotaCoohop':cuotaCoohop, 'cuotaVencida':cuotaVencida, 'valorVencido':valorVencido, 'valorVencidoMasc':valorVencidoMasc, 'valorVencidoRep':valorVencidoRep, 'valorVencidoSeg':valorVencidoSeg, 'valorVencidoAdic':valorVencidoAdic, 'valorVencidoCoohop':valorVencidoCoohop, 'pagoTotal':pagoTotal,'mes':mes, 'objBeneficiario':objBeneficiario, 'cuentaBeneficiario':cuentaBeneficiario, 'objMascota':objMascota, 'cuentaMascota':cuentaMascota, 'formato':5, 'saldo':saldo})                     
        return render(request, template_name, {'lista':asociados, 'mes':mes})
    
class VerDescuentosNomina(ListView):
    template_name = 'reporte/dctosNomina.html'
    
    def get(self, request, *args, **kwargs):
        empresas = TipoAsociado.objects.all()
        return render(request, self.template_name, {'empresas':empresas})
    
    def post(self, request, *args, **kwargs):
        empresas = TipoAsociado.objects.all()
        array = []
        arrayEmp = []
        granTotalGeneral = 0

        for empresa in empresas:
            if len(request.POST.getlist('select'+str(empresa.pk))) == 1:
                query = obtenerDescuentoNomina(empresa.pk)
                array.extend(query['query'])
                arrayEmp.append(empresa.pk)
                granTotalGeneral += query['granTotal']

        return render(request, self.template_name,{'array':array, 'post':'yes', 'empresas':empresas, 'arrayEmp':arrayEmp, 'granTotalGeneral':granTotalGeneral})

class ExcelDescuentosNomina(TemplateView):
    def get(self, request, *args, **kwargs):
        empresas_ids = [key.replace("select", "") for key in request.GET.keys() if key.startswith("select")]
        
        if not empresas_ids:
            return HttpResponse("No se seleccionaron empresas.", content_type="text/plain")

        array = []
        for empresa_id in empresas_ids:
            query = obtenerDescuentoNomina(empresa_id)
            array.extend(query['query'])

        # Estilos
        bold_font = Font(bold=True, size=16, color="FFFFFF")  # Fuente en negrita, tamaño 12 y color blanco
        bold_font2 = Font(bold=True, size=12, color="000000")  # Fuente en negrita, tamaño 12 y color negro
        alignment_center = Alignment(horizontal="center", vertical="center")  # Alineación al centro
        fill = PatternFill(start_color="85B84C", end_color="85B84C", fill_type="solid")  # Relleno verde sólido

        wb = Workbook() #Creamos la instancia del Workbook
        ws = wb.active
        ws.title = 'Descuentos'
        titulo1 = f"Reporte descuentos nomina"
        ws['A1'] = titulo1    #Casilla en la que queremos poner la informacion
        ws.merge_cells('A1:R1')
        ws['A1'].font = bold_font
        ws['A1'].alignment = alignment_center
        ws['A1'].fill = fill

        ws['A2'] = 'Número registro'
        ws['B2'] = 'Codigo'
        ws['C2'] = 'Número Documento'
        ws['D2'] = 'Nombre Completo'
        ws['E2'] = 'Empresa'
        ws['F2'] = 'Valor'
        ws['G2'] = 'Aporte'
        ws['H2'] = 'Bienestar Social'
        ws['I2'] = 'Mascota'
        ws['J2'] = 'Repatriación'
        ws['K2'] = 'Seguro Vida'
        ws['L2'] = 'Adicionales'
        ws['M2'] = 'Coohoperativitos Aporte'
        ws['N2'] = 'Coohoperativitos B Social'
        ws['O2'] = 'Convenios'
        ws['P2'] = 'Descuento Vinculación'
        ws['Q2'] = 'Descuento Crédito'
        ws['R2'] = 'Descuento Crédito Home Elements'

     
        bold_font2 = Font(bold=True)
        center_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

        for col in range(1,19):
            cell = ws.cell(row=2, column=col)
            cell.font = bold_font2
            cell.alignment = center_alignment

        ws.column_dimensions['A'].width = 11
        ws.column_dimensions['B'].width = 11
        ws.column_dimensions['C'].width = 14
        ws.column_dimensions['D'].width = 36
        ws.column_dimensions['E'].width = 20
        ws.column_dimensions['F'].width = 14
        ws.column_dimensions['G'].width = 14
        ws.column_dimensions['H'].width = 14
        ws.column_dimensions['I'].width = 14
        ws.column_dimensions['J'].width = 14
        ws.column_dimensions['K'].width = 14
        ws.column_dimensions['L'].width = 14
        ws.column_dimensions['M'].width = 14
        ws.column_dimensions['N'].width = 14
        ws.column_dimensions['O'].width = 14
        ws.column_dimensions['P'].width = 14
        ws.column_dimensions['Q'].width = 14
        ws.column_dimensions['R'].width = 14

        #Inicia el primer registro en la celda numero 3
        cont = 3
        i = 1
        for obj in array:
            #Row, son las filas , A,B,C,D osea row es igual al contador, y columnas 1,2,3
            ws.cell(row = cont, column = 1).value = i
            ws.cell(row = cont, column = 2).value = obj.asociado.pk
            ws.cell(row = cont, column = 3).value = int(obj.asociado.numDocumento)
            ws.cell(row = cont, column = 4).value = f'{obj.asociado.nombre}' + ' ' + f'{obj.asociado.apellido}'
            ws.cell(row = cont, column = 5).value = obj.asociado.tAsociado.concepto
            ws.cell(row = cont, column = 6).value = obj.total_final
            ws.cell(row = cont, column = 7).value = obj.tarifaAsociado.cuotaAporte
            ws.cell(row = cont, column = 8).value = obj.tarifaAsociado.cuotaBSocial
            ws.cell(row = cont, column = 9).value = obj.tarifaAsociado.cuotaMascota
            ws.cell(row = cont, column = 10).value = obj.tarifaAsociado.cuotaRepatriacion
            ws.cell(row = cont, column = 11).value = obj.tarifaAsociado.cuotaSeguroVida
            ws.cell(row = cont, column = 12).value = obj.tarifaAsociado.cuotaAdicionales
            ws.cell(row = cont, column = 13).value = obj.tarifaAsociado.cuotaCoohopAporte
            ws.cell(row = cont, column = 14).value = obj.tarifaAsociado.cuotaCoohopBsocial
            ws.cell(row = cont, column = 15).value = obj.tarifaAsociado.cuotaConvenio
            ws.cell(row = cont, column = 16).value = obj.cuota_vinculacion if obj.cuota_vinculacion else 0
            ws.cell(row = cont, column = 17).value = obj.cuota_credito if obj.cuota_credito else 0
            ws.cell(row = cont, column = 18).value = obj.cuota_credito_home_elements if obj.cuota_credito_home_elements else 0
            i+=1
            cont+=1

        nombre_archivo = f"Reporte_Descuento_Nomina.xlsx"
        response = HttpResponse(content_type = "application/ms-excel")
        content = "attachment; filename = {0}".format(nombre_archivo)
        response['Content-Disposition'] = content
        wb.save(response)
        return response
    
class VerConciliacionBancaria(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'reporte/listarConciliacionBancaria.html'
        formaPago = FormaPago.objects.all().order_by('formaPago')
        return render(request, template_name, {'formaPago': formaPago})
    
    def post(self, request, *args, **kwargs):
        formaPago = FormaPago.objects.all().order_by('formaPago')
        fechaInicialForm = request.POST['fechaInicial']
        fechaFinalForm = request.POST['fechaFinal']
        banco = int(request.POST['banco'])
        # funcion que separa año, mes y dia de la fecha ingresada por el usuario.
        fechaInicial = separarFecha(fechaInicialForm, 'inicial')
        fechaFinal = separarFecha(fechaFinalForm, 'final')
        # consulta por rango de fecha inicial y final
        queryHistorial = HistorialPagos.objects.filter(
            fechaPago__range=[fechaInicial, fechaFinal],
            formaPago_id=banco
            ).values('asociado__id',
                 'asociado__nombre',
                 'asociado__apellido',
                 'asociado__numDocumento',
                 'formaPago_id__formaPago',
                'fechaPago',
            ).annotate(total_pagado=Sum('valorPago')).order_by('fechaPago')
        
        totalPago = queryHistorial.aggregate(total=Sum('total_pagado'))['total'] or 0
            
        template_name = 'reporte/listarConciliacionBancaria.html'
        return render(request, template_name, {'query':queryHistorial,'post':'post', 'fechaIncialF':fechaInicialForm, 'fechaFinalF':fechaFinalForm, 'formaPago':formaPago, 'banco':banco, 'totalPago':totalPago})

class ExcelConciliacionBancaria(TemplateView):
    def get(self, request, *args, **kwargs):
        fechaInicialForm = request.GET['fechaInicial']
        fechaFinalForm = request.GET['fechaFinal']
        banco = int(request.GET['banco'])
        # funcion que separa año, mes y dia de la fecha ingresada por el usuario.
        fechaInicial = separarFecha(fechaInicialForm, 'inicial')
        fechaFinal = separarFecha(fechaFinalForm, 'final')
        # consulta por rango de fecha inicial y final
        queryHistorial = HistorialPagos.objects.filter(
            fechaPago__range=[fechaInicial, fechaFinal],
            formaPago_id=banco
            ).values('asociado__id',
                 'asociado__nombre',
                 'asociado__apellido',
                 'asociado__numDocumento',
                 'formaPago_id__formaPago',
                'fechaPago',
            ).annotate(total_pagado=Sum('valorPago')).order_by('fechaPago')

        # Estilos
        bold_font = Font(bold=True, size=16, color="FFFFFF")  # Fuente en negrita, tamaño 12 y color blanco
        bold_font2 = Font(bold=True, size=12, color="000000")  # Fuente en negrita, tamaño 12 y color negro
        alignment_center = Alignment(horizontal="center", vertical="center")  # Alineación al centro
        fill = PatternFill(start_color="85B84C", end_color="85B84C", fill_type="solid")  # Relleno verde sólido

        wb = Workbook() #Creamos la instancia del Workbook
        ws = wb.active
        ws.title = 'Conciliación Bancaria'
        titulo1 = f"Conciliación Bancaria"
        ws['A1'] = titulo1    #Casilla en la que queremos poner la informacion
        ws.merge_cells('A1:F1')
        ws['A1'].font = bold_font
        ws['A1'].alignment = alignment_center
        ws['A1'].fill = fill

        ws['A2'] = 'Número registro'
        ws['B2'] = 'Número Documento'
        ws['C2'] = 'Nombre Completo'
        ws['D2'] = 'Movimiento'
        ws['E2'] = 'Valor'
        ws['F2'] = 'Fecha Movimiento'
     
        bold_font2 = Font(bold=True)
        center_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

        for col in range(1,7):
            cell = ws.cell(row=2, column=col)
            cell.font = bold_font2
            cell.alignment = center_alignment

        ws.column_dimensions['A'].width = 11
        ws.column_dimensions['B'].width = 14
        ws.column_dimensions['C'].width = 36
        ws.column_dimensions['D'].width = 25
        ws.column_dimensions['E'].width = 14
        ws.column_dimensions['F'].width = 14

        #Inicia el primer registro en la celda numero 3
        cont = 3
        i = 1
        
        for query in queryHistorial:

            fecha_pago = query['fechaPago']
            fecha_formateada = fecha_pago.strftime("%d/%m/%Y") if fecha_pago else ""
            #Row, son las filas , A,B,C,D osea row es igual al contador, y columnas 1,2,3
            ws.cell(row = cont, column = 1).value = i                    
            ws.cell(row = cont, column = 2).value = int(query['asociado__numDocumento'])
            ws.cell(row = cont, column = 3).value = f'{query['asociado__nombre']}' + ' ' + f'{query['asociado__apellido']}'
            ws.cell(row = cont, column = 4).value = query['formaPago_id__formaPago']
            ws.cell(row = cont, column = 5).value = query['total_pagado']
            ws.cell(row = cont, column = 6).value = fecha_formateada
        
            i+=1
            cont+=1

        nombre_archivo = f"Reporte_Conciliacion_Bancaria.xlsx"
        response = HttpResponse(content_type = "application/ms-excel")
        content = "attachment; filename = {0}".format(nombre_archivo)
        response['Content-Disposition'] = content
        wb.save(response)
        return response
    
# Excel Listado Asociados, Excel Tarifas Asociado
class DescargarExcel(ListView):
    
    def get(self, request, *args, **kwargs):
        tipo_formato = kwargs.get('tipoFormato')

        # Estilos
        bold_font = Font(bold=True, size=16, color="FFFFFF")  # Fuente en negrita, tamaño 12 y color blanco
        bold_font2 = Font(bold=True, size=12, color="000000")  # Fuente en negrita, tamaño 12 y color negro
        alignment_center = Alignment(horizontal="center", vertical="center")  # Alineación al centro
        fill = PatternFill(start_color="85B84C", end_color="85B84C", fill_type="solid")  # Relleno verde sólido

        wb = Workbook() #Creamos la instancia del Workbook
        ws = wb.active

        if tipo_formato == 1:
            ws.title = 'Listado Asociados'
            titulo1 = f"Listado Asociados"
            ws['A1'] = titulo1    #Casilla en la que queremos poner la informacion
            ws.merge_cells('A1:V1')
            ws['A1'].font = bold_font
            ws['A1'].alignment = alignment_center
            ws['A1'].fill = fill

            ws['A2'] = 'Número registro'
            ws['B2'] = 'Codigo'
            ws['C2'] = 'Nombres'
            ws['D2'] = 'Apellidos'
            ws['E2'] = 'Número Documento'
            ws['F2'] = 'Genero'
            ws['G2'] = 'Estado Civil'
            ws['H2'] = 'Tipo Vivienda'
            ws['I2'] = 'Estrato'
            ws['J2'] = 'Dirección'
            ws['K2'] = 'Barrio'
            ws['L2'] = 'Departamento Residencia'
            ws['M2'] = 'Municipio Residencia'
            ws['N2'] = 'Fecha Nacimiento'
            ws['O2'] = 'Indicativo Celular'
            ws['P2'] = 'Número Celular'
            ws['Q2'] = 'Email'
            ws['R2'] = 'Estado Asociado'
            ws['S2'] = 'Tipo Asociado'
            ws['T2'] = 'Fecha Ingreso'
            ws['U2'] = 'Funeraria'
            ws['V2'] = 'Fecha Retiro'
                    
            bold_font2 = Font(bold=True)
            center_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

            for col in range(1,24):
                cell = ws.cell(row=2, column=col)
                cell.font = bold_font2
                cell.alignment = center_alignment

            ws.column_dimensions['A'].width = 11
            ws.column_dimensions['B'].width = 11
            ws.column_dimensions['C'].width = 20
            ws.column_dimensions['D'].width = 20
            ws.column_dimensions['E'].width = 20
            ws.column_dimensions['F'].width = 20
            ws.column_dimensions['G'].width = 20
            ws.column_dimensions['H'].width = 20
            ws.column_dimensions['I'].width = 10
            ws.column_dimensions['J'].width = 25
            ws.column_dimensions['K'].width = 25
            ws.column_dimensions['L'].width = 14
            ws.column_dimensions['M'].width = 20
            ws.column_dimensions['N'].width = 15
            ws.column_dimensions['O'].width = 12
            ws.column_dimensions['P'].width = 15
            ws.column_dimensions['Q'].width = 20
            ws.column_dimensions['R'].width = 18
            ws.column_dimensions['S'].width = 20
            ws.column_dimensions['T'].width = 20
            ws.column_dimensions['U'].width = 22
            ws.column_dimensions['V'].width = 20

            #Inicia el primer registro en la celda numero 3
            cont = 3
            i = 1
            
            queryAsociado = Asociado.objects.all().annotate(funeraria=F('parametroasociado__funeraria__concepto'))

            for asociado in queryAsociado:

                #Row, son las filas , A,B,C,D osea row es igual al contador, y columnas 1,2,3
                ws.cell(row = cont, column = 1).value = i
                ws.cell(row = cont, column = 2).value = asociado.pk             
                ws.cell(row = cont, column = 3).value = asociado.nombre
                ws.cell(row = cont, column = 4).value = asociado.apellido
                ws.cell(row = cont, column = 5).value = int(asociado.numDocumento)
                ws.cell(row = cont, column = 6).value = asociado.genero
                ws.cell(row = cont, column = 7).value = asociado.estadoCivil
                ws.cell(row = cont, column = 8).value = asociado.tipoVivienda
                ws.cell(row = cont, column = 9).value = asociado.estrato
                ws.cell(row = cont, column = 10).value = asociado.direccion
                ws.cell(row = cont, column = 11).value = asociado.barrio
                ws.cell(row = cont, column = 12).value = asociado.deptoResidencia.nombre
                ws.cell(row = cont, column = 13).value = asociado.mpioResidencia.nombre
                ws.cell(row = cont, column = 14).value = asociado.fechaNacimiento.strftime("%d/%m/%Y")
                ws.cell(row = cont, column = 15).value = getattr(asociado.indicativoCelular, 'indicativo', '')
                ws.cell(row = cont, column = 16).value = int(asociado.numCelular)
                ws.cell(row = cont, column = 17).value = asociado.email
                ws.cell(row = cont, column = 18).value = asociado.estadoAsociado
                ws.cell(row = cont, column = 19).value = asociado.tAsociado.concepto
                ws.cell(row = cont, column = 20).value = asociado.fechaIngreso.strftime("%d/%m/%Y")
                ws.cell(row = cont, column = 21).value = asociado.funeraria
                if asociado.fechaRetiro:
                    ws.cell(row = cont, column = 22).value = asociado.fechaRetiro.strftime("%d/%m/%Y")
                else:
                    ws.cell(row = cont, column = 22).value = ''
                i+=1
                cont+=1

            nombre_archivo = f"Reporte_Listado_Asociados.xlsx"

        elif tipo_formato == 2:
            ws.title = 'Listado '
            titulo1 = f"Listado Tarifas Asociados"
            ws['A1'] = titulo1    #Casilla en la que queremos poner la informacion
            ws.merge_cells('A1:O1')
            ws['A1'].font = bold_font
            ws['A1'].alignment = alignment_center
            ws['A1'].fill = fill

            ws['A2'] = 'Número registro'
            ws['B2'] = 'Codigo'
            ws['C2'] = 'Número Documento'
            ws['D2'] = 'Nombre Completo'
            ws['E2'] = 'Tipo Asociado'
            ws['F2'] = 'Valor'
            ws['G2'] = 'Aporte'
            ws['H2'] = 'Bienestar Social'
            ws['I2'] = 'Mascota'
            ws['J2'] = 'Repatriación'
            ws['K2'] = 'Seguro Vida'
            ws['L2'] = 'Adicionales'
            ws['M2'] = 'Coohoperativitos Aporte'
            ws['N2'] = 'Coohoperativitos B Social'
            ws['O2'] = 'Convenio'
        
            bold_font2 = Font(bold=True)
            center_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

            for col in range(1,16):
                cell = ws.cell(row=2, column=col)
                cell.font = bold_font2
                cell.alignment = center_alignment

            ws.column_dimensions['A'].width = 11
            ws.column_dimensions['B'].width = 11
            ws.column_dimensions['C'].width = 14
            ws.column_dimensions['D'].width = 36
            ws.column_dimensions['E'].width = 20
            ws.column_dimensions['F'].width = 14
            ws.column_dimensions['G'].width = 14
            ws.column_dimensions['H'].width = 14
            ws.column_dimensions['I'].width = 14
            ws.column_dimensions['J'].width = 14
            ws.column_dimensions['K'].width = 14
            ws.column_dimensions['L'].width = 14
            ws.column_dimensions['M'].width = 14
            ws.column_dimensions['N'].width = 14
            ws.column_dimensions['O'].width = 14

            #Inicia el primer registro en la celda numero 3
            cont = 3
            i = 1

            queryTarifa = TarifaAsociado.objects.values('asociado__id',
                            'asociado__nombre','asociado__apellido','asociado__numDocumento','asociado__tAsociado__concepto', 'cuotaAporte', 'cuotaBSocial', 'cuotaMascota', 'cuotaRepatriacion', 
                            'cuotaSeguroVida', 'cuotaAdicionales', 'cuotaCoohopAporte', 'cuotaCoohopBsocial', 'cuotaConvenio', 'total'
                        )

            for query in queryTarifa:
                #Row, son las filas , A,B,C,D osea row es igual al contador, y columnas 1,2,3
                ws.cell(row = cont, column = 1).value = i
                ws.cell(row = cont, column = 2).value = query['asociado__id']
                ws.cell(row = cont, column = 3).value = int(query['asociado__numDocumento'])
                ws.cell(row = cont, column = 4).value = f'{query['asociado__nombre']}' + ' ' + f'{query['asociado__apellido']}'
                ws.cell(row = cont, column = 5).value = query['asociado__tAsociado__concepto']
                ws.cell(row = cont, column = 6).value = query['total']
                ws.cell(row = cont, column = 7).value = query['cuotaAporte']
                ws.cell(row = cont, column = 8).value = query['cuotaBSocial']
                ws.cell(row = cont, column = 9).value = query['cuotaMascota']
                ws.cell(row = cont, column = 10).value = query['cuotaRepatriacion']
                ws.cell(row = cont, column = 11).value = query['cuotaSeguroVida']
                ws.cell(row = cont, column = 12).value = query['cuotaAdicionales']
                ws.cell(row = cont, column = 13).value = query['cuotaCoohopAporte']
                ws.cell(row = cont, column = 14).value = query['cuotaCoohopBsocial']
                ws.cell(row = cont, column = 15).value = query['cuotaConvenio']
                i+=1
                cont+=1
            nombre_archivo = f"Reporte_Tarifas_Asociado.xlsx"

        elif tipo_formato == 3:
            pass
        
        response = HttpResponse(content_type = "application/ms-excel")
        content = "attachment; filename = {0}".format(nombre_archivo)
        response['Content-Disposition'] = content
        wb.save(response)
        return response

class DescargarExcelBeneficiarios(ListView):
    
    def get(self, request, *args, **kwargs):
        tipo_formato = kwargs.get('tipoFormato')

        # Estilos
        bold_font = Font(bold=True, size=16, color="FFFFFF")  # Fuente en negrita, tamaño 12 y color blanco
        bold_font2 = Font(bold=True, size=12, color="000000")  # Fuente en negrita, tamaño 12 y color negro
        alignment_center = Alignment(horizontal="center", vertical="center")  # Alineación al centro
        fill = PatternFill(start_color="85B84C", end_color="85B84C", fill_type="solid")  # Relleno verde sólido

        wb = Workbook() #Creamos la instancia del Workbook
        ws = wb.active

        if tipo_formato == 1:
            ws.title = 'Listado Beneficiarios'
            titulo1 = f"Listado Beneficiarios"
            ws['A1'] = titulo1    #Casilla en la que queremos poner la informacion
            ws.merge_cells('A1:M1')
            ws['A1'].font = bold_font
            ws['A1'].alignment = alignment_center
            ws['A1'].fill = fill

            ws['A2'] = 'Número registro'
            ws['B2'] = 'Codigo Titular'
            ws['C2'] = 'Nombres Titular'
            ws['D2'] = 'Apellidos Titular'
            ws['E2'] = 'Número Documento Titular'
            ws['F2'] = 'Codigo Beneficiario'
            ws['G2'] = 'Nombres Beneficiario'
            ws['H2'] = 'Apellidos Beneficiario'
            ws['I2'] = 'Número Documento Beneficiario'
            ws['J2'] = 'Tipo Documento'
            ws['K2'] = 'Fecha Nacimiento'
            ws['L2'] = 'Parentesco'
            ws['M2'] = 'Repatración'
                    
            bold_font2 = Font(bold=True)
            center_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

            for col in range(1,14):
                cell = ws.cell(row=2, column=col)
                cell.font = bold_font2
                cell.alignment = center_alignment

            ws.column_dimensions['A'].width = 11
            ws.column_dimensions['B'].width = 11
            ws.column_dimensions['C'].width = 20
            ws.column_dimensions['D'].width = 20
            ws.column_dimensions['E'].width = 20
            ws.column_dimensions['F'].width = 12
            ws.column_dimensions['G'].width = 20
            ws.column_dimensions['H'].width = 20
            ws.column_dimensions['I'].width = 20
            ws.column_dimensions['J'].width = 20
            ws.column_dimensions['K'].width = 20
            ws.column_dimensions['L'].width = 20
            ws.column_dimensions['M'].width = 20

            #Inicia el primer registro en la celda numero 3
            cont = 3
            i = 1
            
            queryBeneficiario = Beneficiario.objects.filter(estadoRegistro = True)

            for obj in queryBeneficiario:

                #Row, son las filas , A,B,C,D osea row es igual al contador, y columnas 1,2,3
                ws.cell(row = cont, column = 1).value = i
                ws.cell(row = cont, column = 2).value = obj.asociado.pk             
                ws.cell(row = cont, column = 3).value = obj.asociado.nombre
                ws.cell(row = cont, column = 4).value = obj.asociado.apellido
                ws.cell(row = cont, column = 5).value = int(obj.asociado.numDocumento)
                ws.cell(row = cont, column = 6).value = obj.pk
                ws.cell(row = cont, column = 7).value = obj.nombre
                ws.cell(row = cont, column = 8).value = obj.apellido
                ws.cell(row = cont, column = 9).value = int(obj.numDocumento)
                ws.cell(row = cont, column = 10).value = obj.tipoDocumento
                ws.cell(row = cont, column = 11).value = obj.fechaNacimiento.strftime("%d/%m/%Y")
                ws.cell(row = cont, column = 12).value = obj.parentesco.nombre
                if obj.repatriacion == True:
                    ws.cell(row = cont, column = 13).value = f'{obj.paisRepatriacion.nombre}' + '-' + f'{obj.ciudadRepatriacion}'
                else:
                    ws.cell(row = cont, column = 13).value = ''

                i+=1
                cont+=1
                nombre_archivo = f"Reporte_Listado_Beneficiarios.xlsx"
        elif tipo_formato == 2:
            ws.title = 'Listado Mascotas'
            titulo1 = f"Listado Mascotas"
            ws['A1'] = titulo1    #Casilla en la que queremos poner la informacion
            ws.merge_cells('A1:H1')
            ws['A1'].font = bold_font
            ws['A1'].alignment = alignment_center
            ws['A1'].fill = fill

            ws['A2'] = 'Número registro'
            ws['B2'] = 'Codigo'
            ws['C2'] = 'Nombre Completo Titular'
            ws['D2'] = 'Número Documento Titular'
            ws['E2'] = 'Nombre Mascota'
            ws['F2'] = 'Tipo'
            ws['G2'] = 'Raza'
            ws['H2'] = 'Fecha Nacimiento'    
        
            bold_font2 = Font(bold=True)
            center_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

            for col in range(1,9):
                cell = ws.cell(row=2, column=col)
                cell.font = bold_font2
                cell.alignment = center_alignment

            ws.column_dimensions['A'].width = 11
            ws.column_dimensions['B'].width = 11
            ws.column_dimensions['C'].width = 20
            ws.column_dimensions['D'].width = 20
            ws.column_dimensions['E'].width = 20
            ws.column_dimensions['F'].width = 20
            ws.column_dimensions['G'].width = 20
            ws.column_dimensions['H'].width = 20

            #Inicia el primer registro en la celda numero 3
            cont = 3
            i = 1

            queryMascota = Mascota.objects.filter(estadoRegistro = True)

            for query in queryMascota:
                #Row, son las filas , A,B,C,D osea row es igual al contador, y columnas 1,2,3
                ws.cell(row = cont, column = 1).value = i
                ws.cell(row = cont, column = 2).value = query.asociado.pk
                ws.cell(row = cont, column = 3).value = query.asociado.nombre + ' ' + query.asociado.apellido
                ws.cell(row = cont, column = 4).value = int(query.asociado.numDocumento)
                ws.cell(row = cont, column = 5).value = query.nombre
                ws.cell(row = cont, column = 6).value = query.tipo
                ws.cell(row = cont, column = 7).value = query.raza
                ws.cell(row = cont, column = 8).value = query.fechaNacimiento.strftime("%d/%m/%Y")
                i+=1
                cont+=1
            nombre_archivo = f"Reporte_Listado_Mascotas.xlsx"
        elif tipo_formato == 3:
            pass
        response = HttpResponse(content_type = "application/ms-excel")
        content = "attachment; filename = {0}".format(nombre_archivo)
        response['Content-Disposition'] = content
        wb.save(response)
        return response

class DescargaAuxilio(ListView):
    def get(self, request, *args, **kwargs):
        template = 'reporte/modalReporte.html'
        return render(request, template, {'tipoReporte':'auxilio'})
    
    def post(self, request, *args, **kwargs):
        fechaInicialForm = request.POST['fechaInicial']
        fechaFinalForm = request.POST['fechaFinal']

        queryAuxilio = HistoricoAuxilio.objects.filter(
            fechaSolicitud__range=[fechaInicialForm, fechaFinalForm]
        )

        # Convertir la cadena de fecha a un objeto datetime
        fecha_objeto1 = datetime.strptime(fechaInicialForm, "%Y-%m-%d")
        # Formatear la fecha en el formato d-m-Y
        fecha_formateada1 = fecha_objeto1.strftime("%d-%m-%Y")
        # Convertir la cadena de fecha a un objeto datetime
        fecha_objeto2 = datetime.strptime(fechaFinalForm, "%Y-%m-%d")
        # Formatear la fecha en el formato d-m-Y
        fecha_formateada2 = fecha_objeto2.strftime("%d-%m-%Y")

        # Estilos
        bold_font = Font(bold=True, size=16, color="FFFFFF")  # Fuente en negrita, tamaño 12 y color blanco
        bold_font2 = Font(bold=True, size=12, color="000000")  # Fuente en negrita, tamaño 12 y color negro
        alignment_center = Alignment(horizontal="center", vertical="center")  # Alineación al centro
        fill = PatternFill(start_color="85B84C", end_color="85B84C", fill_type="solid")  # Relleno verde sólido

        wb = Workbook() #Creamos la instancia del Workbook
        ws = wb.active
        ws.title = 'Auxilios'
        titulo1 = f"Reporte de Auxilios desde {fecha_formateada1} - {fecha_formateada2}"
        ws['A1'] = titulo1    #Casilla en la que queremos poner la informacion
        ws.merge_cells('A1:K1')
        ws['A1'].font = bold_font
        ws['A1'].alignment = alignment_center
        ws['A1'].fill = fill

        ws['A2'] = 'Número Registro'
        ws['B2'] = 'Número Documento'
        ws['C2'] = 'Nombre Completo'
        ws['D2'] = 'Tipo Auxilio'
        ws['E2'] = 'Entidad Bancaria'
        ws['F2'] = 'Número Cuenta'
        ws['G2'] = 'Valor Auxilio'
        ws['H2'] = 'Fecha Solicitud'
        ws['I2'] = 'Estado'
        ws['J2'] = 'Observaciones'
        ws['K2'] = 'Fecha Desembolso'
     
        bold_font2 = Font(bold=True)
        center_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

        for col in range(1,12):
            cell = ws.cell(row=2, column=col)
            cell.font = bold_font2
            cell.alignment = center_alignment

        ws.column_dimensions['A'].width = 11
        ws.column_dimensions['B'].width = 14
        ws.column_dimensions['C'].width = 32
        ws.column_dimensions['D'].width = 26
        ws.column_dimensions['E'].width = 28
        ws.column_dimensions['F'].width = 15
        ws.column_dimensions['G'].width = 12
        ws.column_dimensions['H'].width = 13
        ws.column_dimensions['I'].width = 13
        ws.column_dimensions['J'].width = 20
        ws.column_dimensions['K'].width = 13

        #Inicia el primer registro en la celda numero 3
        cont = 3
        i = 1
        for auxilio in queryAuxilio:
            #Row, son las filas , A,B,C,D osea row es igual al contador, y columnas 1,2,3
            ws.cell(row = cont, column = 1).value = i                    
            ws.cell(row = cont, column = 2).value = int(auxilio.asociado.numDocumento)
            ws.cell(row = cont, column = 3).value = f'{auxilio.asociado.nombre}' + ' ' + f'{auxilio.asociado.apellido}'
            ws.cell(row = cont, column = 4).value = auxilio.tipoAuxilio.nombre
            ws.cell(row = cont, column = 5).value = auxilio.entidadBancaria
            ws.cell(row = cont, column = 6).value = auxilio.numCuenta
            ws.cell(row = cont, column = 7).value = auxilio.valor
            ws.cell(row = cont, column = 8).value = auxilio.fechaSolicitud.strftime("%d/%m/%Y")
            ws.cell(row = cont, column = 9).value = auxilio.estado
            ws.cell(row = cont, column = 10).value = auxilio.observacion
            if auxilio.fechaDesembolso:
                ws.cell(row = cont, column = 11).value = auxilio.fechaDesembolso.strftime("%d/%m/%Y")
            else:
                ws.cell(row = cont, column = 11).value = ''
            i+=1
            cont+=1

        nombre_archivo = f"Reporte_Auxilio_{fecha_formateada1}-{fecha_formateada2}.xlsx"
        response = HttpResponse(content_type = "application/ms-excel")
        content = "attachment; filename = {0}".format(nombre_archivo)
        response['Content-Disposition'] = content
        wb.save(response)
        return response

class DescargaCredito(ListView):
    def get(self, request, *args, **kwargs):
        template = 'reporte/modalReporte.html'
        return render(request, template, {'tipoReporte':'credito'})
    
    def post(self, request, *args, **kwargs):
        fechaInicialForm = request.POST['fechaInicial']
        fechaFinalForm = request.POST['fechaFinal']

        queryCredito = HistoricoCredito.objects.filter(
            fechaSolicitud__range=[fechaInicialForm, fechaFinalForm]
        )

        # Convertir la cadena de fecha a un objeto datetime
        fecha_objeto1 = datetime.strptime(fechaInicialForm, "%Y-%m-%d")
        # Formatear la fecha en el formato d-m-Y
        fecha_formateada1 = fecha_objeto1.strftime("%d-%m-%Y")
        # Convertir la cadena de fecha a un objeto datetime
        fecha_objeto2 = datetime.strptime(fechaFinalForm, "%Y-%m-%d")
        # Formatear la fecha en el formato d-m-Y
        fecha_formateada2 = fecha_objeto2.strftime("%d-%m-%Y")

        # Estilos
        bold_font = Font(bold=True, size=16, color="FFFFFF")  # Fuente en negrita, tamaño 12 y color blanco
        bold_font2 = Font(bold=True, size=12, color="000000")  # Fuente en negrita, tamaño 12 y color negro
        alignment_center = Alignment(horizontal="center", vertical="center")  # Alineación al centro
        fill = PatternFill(start_color="85B84C", end_color="85B84C", fill_type="solid")  # Relleno verde sólido

        wb = Workbook() #Creamos la instancia del Workbook
        ws = wb.active
        ws.title = 'Creditos'
        titulo1 = f"Reporte de Créditos desde {fecha_formateada1} - {fecha_formateada2}"
        ws['A1'] = titulo1    #Casilla en la que queremos poner la informacion
        ws.merge_cells('A1:R1')
        ws['A1'].font = bold_font
        ws['A1'].alignment = alignment_center
        ws['A1'].fill = fill

        ws['A2'] = 'Número Registro'
        ws['B2'] = 'Número Documento'
        ws['C2'] = 'Nombre Completo'
        ws['D2'] = 'Fecha Solicitud'
        ws['E2'] = 'Valor'
        ws['F2'] = 'Número Cuotas'
        ws['G2'] = 'Valor Cuota'
        ws['H2'] = 'Total Credito'
        ws['I2'] = 'Estado'
        ws['J2'] = 'Linea Credito'
        ws['K2'] = 'Amortización'
        ws['L2'] = 'Tasa Interes'
        ws['M2'] = 'Forma Desembolso'
        ws['N2'] = 'Medio de Pago'
        ws['O2'] = 'Tipo Asociado'
        ws['P2'] = 'Banco'
        ws['Q2'] = 'Tipo de Cuenta'
        ws['R2'] = 'Número de Cuenta'
        
        bold_font2 = Font(bold=True)
        center_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

        for col in range(1,19):
            cell = ws.cell(row=2, column=col)
            cell.font = bold_font2
            cell.alignment = center_alignment

        ws.column_dimensions['A'].width = 11
        ws.column_dimensions['B'].width = 14
        ws.column_dimensions['C'].width = 32
        ws.column_dimensions['D'].width = 15
        ws.column_dimensions['E'].width = 12
        ws.column_dimensions['F'].width = 12
        ws.column_dimensions['G'].width = 12
        ws.column_dimensions['H'].width = 13
        ws.column_dimensions['I'].width = 13
        ws.column_dimensions['J'].width = 21
        ws.column_dimensions['K'].width = 16
        ws.column_dimensions['L'].width = 13
        ws.column_dimensions['M'].width = 28
        ws.column_dimensions['N'].width = 15
        ws.column_dimensions['O'].width = 17
        ws.column_dimensions['P'].width = 16
        ws.column_dimensions['Q'].width = 18
        ws.column_dimensions['R'].width = 15

        #Inicia el primer registro en la celda numero 3
        cont = 3
        i = 1
        for credito in queryCredito:
            #Row, son las filas , A,B,C,D osea row es igual al contador, y columnas 1,2,3
            ws.cell(row = cont, column = 1).value = i                    
            ws.cell(row = cont, column = 2).value = int(credito.asociado.numDocumento)
            ws.cell(row = cont, column = 3).value = f'{credito.asociado.nombre}' + ' ' + f'{credito.asociado.apellido}'
            ws.cell(row = cont, column = 4).value = credito.fechaSolicitud.strftime("%d/%m/%Y")
            ws.cell(row = cont, column = 5).value = credito.valor
            ws.cell(row = cont, column = 6).value = credito.cuotas
            ws.cell(row = cont, column = 7).value = credito.valorCuota
            ws.cell(row = cont, column = 8).value = credito.totalCredito
            ws.cell(row = cont, column = 9).value = credito.estado
            ws.cell(row = cont, column = 10).value = credito.lineaCredito
            ws.cell(row = cont, column = 11).value = credito.amortizacion
            ws.cell(row = cont, column = 12).value = credito.tasaInteres.porcentaje * 100 if credito.tasaInteres else 0
            ws.cell(row = cont, column = 13).value = credito.formaDesembolso
            ws.cell(row = cont, column = 14).value = credito.medioPago
            ws.cell(row = cont, column = 15).value = credito.asociado.tAsociado.concepto
            ws.cell(row = cont, column = 16).value = credito.banco
            ws.cell(row = cont, column = 17).value = credito.tipoCuenta
            ws.cell(row = cont, column = 18).value = credito.numCuenta
            i+=1
            cont+=1

        nombre_archivo = f"Reporte_Credito_{fecha_formateada1}-{fecha_formateada2}.xlsx"
        response = HttpResponse(content_type = "application/ms-excel")
        content = "attachment; filename = {0}".format(nombre_archivo)
        response['Content-Disposition'] = content
        wb.save(response)
        return response