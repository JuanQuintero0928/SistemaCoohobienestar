from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy

from zoneinfo import ZoneInfo
from datetime import datetime

from beneficiario.models import Mascota, Beneficiario
from historico.models import HistorialPagos
from funciones.function import fechaUtc, separarFecha

#Libreria para generar el Excel
from openpyxl import Workbook

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
        # consulta por rango de fecha inicial y final
        queryMascota = Mascota.objects.filter(
            fechaModificacion__range=[fechaInicial, fechaFinal]
        )
        queryBeneficiario = Beneficiario.objects.filter(
            fechaModificacion__range=[fechaInicial, fechaFinal]
        )
        # fechaInicialEnvio = fechaInicial.strftime("%Y-%m-%d")
        template_name = 'reporte/modificacionesPorFecha.html'
        return render(request, template_name, {'queryM':queryMascota, 'queryB':queryBeneficiario, 'post':'yes', 'fechaIncialF':fechaInicialForm, 'fechaFinalF':fechaFinalForm})

class ReporteExcelFecha(TemplateView):
    def get(self, request, *args, **kwargs):
        fechaInicialForm = request.GET['fechaInicial']
        fechaFinalForm = request.GET['fechaFinal']
        # funcion que separa año, mes y dia de la fecha ingresada por el usuario.
        fechaInicial = separarFecha(fechaInicialForm, 'inicial')
        fechaFinal = separarFecha(fechaFinalForm, 'final')
        # consulta por rango de fecha inicial y final
        queryMascota = Mascota.objects.filter(
            fechaModificacion__range=[fechaInicial, fechaFinal]
        )
        queryBeneficiario = Beneficiario.objects.filter(
            fechaModificacion__range=[fechaInicial, fechaFinal]
        )
        wb = Workbook() #Creamos la instancia del Workbook
        ws = wb.active
        ws.title = 'Mascotas'
        titulo1 = f"Reporte de Novedades Mascota Funeraria desde {fechaInicialForm} - {fechaFinalForm}"
        ws['A1'] = titulo1    #Casilla en la que queremos poner la informacion
        ws.merge_cells('A1:G1')

        ws['A2'] = 'Número registro'
        ws['B2'] = 'Mascota'
        ws['C2'] = 'tipo'
        ws['D2'] = 'raza'
        ws['E2'] = 'fechaNacimiento'
        ws['F2'] = 'Novedad'
        ws['G2'] = 'Fecha Retiro'
     
        #Inicia el primer registro en la celda numero 3
        cont = 3
        i = 1
        for mascota in queryMascota:
            #Row, son las filas , A,B,C,D osea row es igual al contador, y columnas 1,2,3
            ws.cell(row = cont, column = 1).value = i                    
            ws.cell(row = cont, column = 2).value = mascota.nombre
            ws.cell(row = cont, column = 3).value = mascota.tipo
            ws.cell(row = cont, column = 4).value = mascota.raza
            ws.cell(row = cont, column = 5).value = mascota.fechaNacimiento
            if mascota.fechaCreacion == mascota.fechaModificacion:
                ws.cell(row = cont, column = 6).value = 'Ingreso'
            elif mascota.fechaCreacion != mascota.fechaModificacion:
                if mascota.estadoRegistro == True:
                    ws.cell(row = cont, column = 6).value = 'Modificación'
                else:
                    ws.cell(row = cont, column = 6).value = 'Retiro'
                    ws.cell(row = cont, column = 7).value = mascota.fechaRetiro
            i+=1
            cont+=1
        
        # se crea una nueva hoja
        wb.create_sheet('Beneficiarios')
        # se selecciona la hoja creada
        ws2 = wb['Beneficiarios']
        titulo2 = f"Reporte de Novedades Beneficiarios Funeraria desde {fechaInicialForm} - {fechaFinalForm}"
        ws2['A1'] = titulo2    #Casilla en la que queremos poner la informacion
        ws2.merge_cells('A1:I1')
        ws2['A2'] = 'Número registro'
        ws2['B2'] = 'Nombre'
        ws2['C2'] = 'Tipo Documento'
        ws2['D2'] = 'Número Documento'
        ws2['E2'] = 'Fecha Nacimiento'
        ws2['F2'] = 'Parentesco'
        ws2['G2'] = 'Pais Repatriacion'
        ws2['H2'] = 'Novedad'
        ws2['I2'] = 'Fecha Retiro'

        #Inicia el primer registro en la celda numero 3
        cont = 3
        i = 1
        for beneficiario in queryBeneficiario:
            #Row, son las filas , A,B,C,D osea row es igual al contador, y columnas 1,2,3
            ws2.cell(row = cont, column = 1).value = i                    
            ws2.cell(row = cont, column = 2).value = f'{beneficiario.asociado.nombre}' + ' ' + f'{beneficiario.asociado.apellido}'
            ws2.cell(row = cont, column = 3).value = beneficiario.tipoDocumento
            ws2.cell(row = cont, column = 4).value = int(beneficiario.numDocumento)
            ws2.cell(row = cont, column = 5).value = beneficiario.fechaNacimiento
            ws2.cell(row = cont, column = 6).value = beneficiario.parentesco.nombre
            if beneficiario.repatriacion == True:
                ws2.cell(row = cont, column = 7).value = beneficiario.paisRepatriacion.nombre
            else:
                ws2.cell(row = cont, column = 7).value = ''
            if beneficiario.fechaCreacion == beneficiario.fechaModificacion:
                ws2.cell(row = cont, column = 8).value = 'Ingreso'
            elif beneficiario.fechaCreacion != beneficiario.fechaModificacion:
                if beneficiario.estadoRegistro == True:
                    ws2.cell(row = cont, column = 8).value = 'Modificación'
                else:
                    ws2.cell(row = cont, column = 8).value = 'Retiro'
                    ws2.cell(row = cont, column = 9).value = beneficiario.fechaRetiro
            i+=1
            cont+=1

        nombre_archivo = f"Reporte Modificaciones_{fechaInicialForm}-{fechaFinalForm}.xlsx"
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
        # consulta por rango de fecha inicial y final
        queryHistorial = HistorialPagos.objects.filter(
            fechaCreacion__range=[fechaInicial, fechaFinal]
        )
        template_name = 'reporte/pagosPorFecha.html'
        return render(request, template_name, {'query':queryHistorial,'post':'yes', 'fechaIncialF':fechaInicialForm, 'fechaFinalF':fechaFinalForm})

class ReporteExcelPago(TemplateView):
    def get(self, request, *args, **kwargs):
        fechaInicialForm = request.GET['fechaInicial']
        fechaFinalForm = request.GET['fechaFinal']
        # funcion que separa año, mes y dia de la fecha ingresada por el usuario.
        fechaInicial = separarFecha(fechaInicialForm, 'inicial')
        fechaFinal = separarFecha(fechaFinalForm, 'final')
        # consulta por rango de fecha inicial y final
        queryPagos = HistorialPagos.objects.filter(
            fechaCreacion__range=[fechaInicial, fechaFinal]
        )
        wb = Workbook() #Creamos la instancia del Workbook
        ws = wb.active
        ws.title = 'Pagos'
        titulo1 = f"Reporte de Pagos desde {fechaInicialForm} - {fechaFinalForm}"
        ws['A1'] = titulo1    #Casilla en la que queremos poner la informacion
        ws.merge_cells('A1:N1')

        ws['A2'] = 'numero registro'
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
        ws['M2'] = 'Coohoperativitos'
        ws['N2'] = 'Forma Pago'
     
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

        nombre_archivo = f"Reporte Pago_{fechaInicialForm}-{fechaFinalForm}.xlsx"
        response = HttpResponse(content_type = "application/ms-excel")
        content = "attachment; filename = {0}".format(nombre_archivo)
        response['Content-Disposition'] = content
        wb.save(response)
        return response