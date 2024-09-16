from tabnanny import check
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models.functions import TruncDate
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Sum

from zoneinfo import ZoneInfo
from datetime import date, datetime, timedelta

from asociado.models import Asociado, Financiera, Laboral, Nacimiento, ParametroAsociado, Residencia, TarifaAsociado
from beneficiario.models import Mascota, Beneficiario
from historico.models import HistorialPagos, HistoricoAuxilio
from funciones.function import fechaUtc, separarFecha
from parametro.models import MesTarifa, TipoAsociado

#Libreria para generar el Excel
from openpyxl import Workbook


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
        # consulta por rango de fecha inicial y final
        queryAsociado = Asociado.objects.filter(
            fechaModificacion__range=[fechaInicial, fechaFinal]
        )
        queryMascota = Mascota.objects.filter(
            fechaModificacion__range=[fechaInicial, fechaFinal]
        )
        queryBeneficiario = Beneficiario.objects.filter(
            fechaModificacion__range=[fechaInicial, fechaFinal]
        )
        # fechaInicialEnvio = fechaInicial.strftime("%Y-%m-%d")
        template_name = 'reporte/modificacionesPorFecha.html'
        return render(request, template_name, {'queryM':queryMascota, 'queryB':queryBeneficiario, 'post':'yes', 'fechaIncialF':fechaInicialForm, 'fechaFinalF':fechaFinalForm, 'queryAsociado':queryAsociado})

class ReporteExcelFecha(TemplateView):
    def get(self, request, *args, **kwargs):
        fechaInicialForm = request.GET['fechaInicial']
        fechaFinalForm = request.GET['fechaFinal']
        # funcion que separa año, mes y dia de la fecha ingresada por el usuario.
        fechaInicial = separarFecha(fechaInicialForm, 'inicial')
        fechaFinal = separarFecha(fechaFinalForm, 'final')
        # consulta por rango de fecha inicial y final
        queryAsociado = Asociado.objects.annotate(
            fecha_solo = TruncDate('fechaModificacion')).filter(
            fechaModificacion__range=[fechaInicial, fechaFinal]
        )
    
        queryMascota = Mascota.objects.annotate(
            fecha_solo = TruncDate('fechaModificacion')).filter(
            fechaModificacion__range=[fechaInicial, fechaFinal]
        )
        queryBeneficiario = Beneficiario.objects.annotate(
            fecha_solo = TruncDate('fechaModificacion')).filter(
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
        ws['G2'] = 'Fecha'
     
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
                ws.cell(row = cont, column = 7).value = mascota.fechaIngreso
            elif mascota.fechaCreacion != mascota.fechaModificacion:
                if mascota.estadoRegistro == True:
                    ws.cell(row = cont, column = 6).value = 'Modificación'
                    ws.cell(row = cont, column = 7).value = mascota.fecha_solo
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
        ws2['I2'] = 'Fecha'

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
                ws2.cell(row = cont, column = 9).value = beneficiario.fechaIngreso
            elif beneficiario.fechaCreacion != beneficiario.fechaModificacion:
                if beneficiario.estadoRegistro == True:
                    ws2.cell(row = cont, column = 8).value = 'Modificación'
                    ws2.cell(row = cont, column = 9).value = beneficiario.fecha_solo
                else:
                    ws2.cell(row = cont, column = 8).value = 'Retiro'
                    ws2.cell(row = cont, column = 9).value = str(beneficiario.fechaRetiro)
            i+=1
            cont+=1
        
        # se crea una nueva hoja
        wb.create_sheet('Asociados')
        # se selecciona la hoja creada
        ws2 = wb['Asociados']
        titulo2 = f"Reporte de Novedades Asociados Funeraria desde {fechaInicialForm} - {fechaFinalForm}"
        ws2['A1'] = titulo2    #Casilla en la que queremos poner la informacion
        ws2.merge_cells('A1:G1')
        ws2['A2'] = 'Número registro'
        ws2['B2'] = 'Nombre'
        ws2['C2'] = 'Tipo Documento'
        ws2['D2'] = 'Número Documento'
        ws2['E2'] = 'Fecha Nacimiento'
        ws2['F2'] = 'Novedad'
        ws2['G2'] = 'Fecha'

        #Inicia el primer registro en la celda numero 3
        cont = 3
        i = 1
        for asociado in queryAsociado:
            #Row, son las filas , A,B,C,D osea row es igual al contador, y columnas 1,2,3
            obj = Nacimiento.objects.get(asociado = asociado.pk)
            ws2.cell(row = cont, column = 1).value = i                    
            ws2.cell(row = cont, column = 2).value = f'{asociado.nombre}' + ' ' + f'{asociado.apellido}'
            ws2.cell(row = cont, column = 3).value = asociado.tipoDocumento
            ws2.cell(row = cont, column = 4).value = int(asociado.numDocumento)
            ws2.cell(row = cont, column = 5).value = obj.fechaNacimiento
            if asociado.fechaCreacion == asociado.fechaModificacion:
                ws2.cell(row = cont, column = 6).value = 'Ingreso'
                ws2.cell(row = cont, column = 7).value = asociado.fechaIngreso
            elif asociado.fechaCreacion != asociado.fechaModificacion:
                if asociado.estadoRegistro == True:
                    ws2.cell(row = cont, column = 6).value = 'Modificación'
                    ws2.cell(row = cont, column = 7).value = asociado.fecha_solo
                else:
                    ws2.cell(row = cont, column = 6).value = 'Retiro'
                    ws2.cell(row = cont, column = 7).value = asociado.fechaRetiro
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
    
class FormatoExtracto(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'reporte/reporteExtracto.html'
        mes = MesTarifa.objects.all()
        return render(request, template_name, {'mes':mes})


    def post(self, request, *args, **kwargs):
        template_name = 'reporte/generarExtracto.html'
        
        objAsoc = Asociado.objects.filter(estadoAsociado = 'ACTIVO')
        mesExtracto = request.POST['mesExtracto']
        asociados = []
        for asociado in objAsoc:
            parametro = ParametroAsociado.objects.get(asociado = asociado.pk)
            mes = MesTarifa.objects.get(pk = mesExtracto)
            # se valida si el primer mes de pago es igual o mayor a la seleccion del form
            if mes.pk >= parametro.primerMes.pk:
                objResidencia = Residencia.objects.get(asociado = asociado.pk)
                # Formato 4
                fechaCorte = timedelta(15) + mes.fechaInicio
                objTarifaAsociado = TarifaAsociado.objects.get(asociado = asociado.pk)
                # query del ultimo pago hecho por el asociado
                objHistorialPago = HistorialPagos.objects.filter(asociado = asociado.pk).last()     
                cuotaPeriodica = objTarifaAsociado.cuotaAporte + objTarifaAsociado.cuotaBSocial
                cuotaCoohop = objTarifaAsociado.cuotaCoohopAporte + objTarifaAsociado.cuotaCoohopBsocial
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
                objBeneficiario = Beneficiario.objects.filter(asociado = asociado.pk)
                cuentaBeneficiario = len(objBeneficiario)
                objMascota = Mascota.objects.filter(asociado = asociado.pk)
                cuentaMascota = len(objMascota)
                # query que suma la diferencia de pagos
                querySaldoTotal = HistorialPagos.objects.filter(asociado = asociado.pk).aggregate(total=Sum('diferencia'))
                for valor in querySaldoTotal.values():
                    # variable que guarda la diferencia en los saldos(0=esta al dia, > a 0, saldo favor, < a 0, saldo pendiente)
                    saldoDiferencia = valor
                
                # Entra al try cuando un asociado no ha realizado ningun pago y no existe informacion en la query
                try:
                    # condicional si esta atrasado
                    if mes.pk > objHistorialPago.mesPago.pk:
                        cuotaVencida = mes.pk - objHistorialPago.mesPago.pk
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
                            valorVencido = (cuotaPeriodica * cuotaVencida) - saldoDiferencia
                            pagoTotal = valorVencido + valorVencidoMasc + valorVencidoRep + valorVencidoSeg + valorVencidoAdic + valorVencidoCoohop
                            mensaje = "Tiene un saldo a favor de $" + str(saldoDiferencia)
                        elif saldoDiferencia < 0:
                            # saldo a pagar
                            valorVencido = (cuotaPeriodica * cuotaVencida) - saldoDiferencia
                            pagoTotal = valorVencido + valorVencidoMasc + valorVencidoRep + valorVencidoSeg + valorVencidoAdic + valorVencidoCoohop
                            mensaje = "Tiene un saldo pendiente por pagar de $" + str((saldoDiferencia*-1))
                        else:
                            # saldo en 0
                            valorVencido = (cuotaPeriodica * cuotaVencida)
                            pagoTotal = valorVencido + valorVencidoMasc + valorVencidoRep + valorVencidoSeg + valorVencidoAdic + valorVencidoCoohop
                        asociados.append({'pkAsociado':asociado.pk, 'fechaCorte':fechaCorte,'objAsoc':asociado, 'objResidencia':objResidencia, 'objTarifaAsociado':objTarifaAsociado, 'cuotaPeriodica':cuotaPeriodica, 'cuotaCoohop':cuotaCoohop, 'cuotaVencida':cuotaVencida, 'valorVencido':valorVencido, 'valorVencidoMasc':valorVencidoMasc, 'valorVencidoRep':valorVencidoRep, 'valorVencidoSeg':valorVencidoSeg, 'valorVencidoAdic':valorVencidoAdic, 'valorVencidoCoohop':valorVencidoCoohop, 'pagoTotal':pagoTotal,'mes':mes, 'objBeneficiario':objBeneficiario, 'cuentaBeneficiario':cuentaBeneficiario, 'objMascota':objMascota, 'cuentaMascota':cuentaMascota, 'formato':5, 'saldo':saldo, 'mensaje':mensaje})
                        
                    # condicional si esta al dia
                    elif mes.pk == objHistorialPago.mesPago.pk:
                        cuotaVencida = 0
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
                        asociados.append({'pkAsociado':asociado.pk, 'fechaCorte':fechaCorte,'objAsoc':asociado, 'objResidencia':objResidencia, 'objTarifaAsociado':objTarifaAsociado, 'cuotaPeriodica':cuotaPeriodica, 'cuotaCoohop':cuotaCoohop, 'cuotaVencida':cuotaVencida, 'valorVencido':valorVencido, 'valorVencidoMasc':valorVencidoMasc, 'valorVencidoRep':valorVencidoRep, 'valorVencidoSeg':valorVencidoSeg, 'valorVencidoAdic':valorVencidoAdic, 'valorVencidoCoohop':valorVencidoCoohop, 'pagoTotal':pagoTotal,'mes':mes, 'objBeneficiario':objBeneficiario, 'cuentaBeneficiario':cuentaBeneficiario, 'objMascota':objMascota, 'cuentaMascota':cuentaMascota, 'formato':5, 'saldo':saldo, 'mensaje':mensaje})
                    
                    # condicional si esta adelantado
                    else:
                        cuotaVencida = 0
                        pagoTotal = 0
                        # obtenemos el valor total que tiene pago el asociado, desde el mes seleccionado en la query hasta el pago en la bd
                        query = HistorialPagos.objects.filter(mesPago__gte = mes.pk, asociado = asociado.pk).aggregate(total=Sum('valorPago'))
                        for valor in query.values():
                            saldoActual = valor
                        
                        valorMensual = (objTarifaAsociado.cuotaAporte + objTarifaAsociado.cuotaBSocial + objTarifaAsociado.cuotaMascota + objTarifaAsociado.cuotaRepatriacion + objTarifaAsociado.cuotaSeguroVida + objTarifaAsociado.cuotaAdicionales + objTarifaAsociado.cuotaCoohopAporte + objTarifaAsociado.cuotaCoohopBsocial) * ((objHistorialPago.mesPago.pk - mes.pk)+1)
                        
                        if saldoDiferencia > 0:
                            saldo = valorMensual + saldoDiferencia
                        elif saldoDiferencia < 0:
                            saldo = valorMensual + saldoDiferencia
                        else:
                            saldo = valorMensual

                        mensaje = "Tiene Pago hasta el mes de " + objHistorialPago.mesPago.concepto + "."
                        
                        asociados.append({'pkAsociado':asociado.pk, 'fechaCorte':fechaCorte,'objAsoc':asociado, 'objResidencia':objResidencia, 'objTarifaAsociado':objTarifaAsociado, 'cuotaPeriodica':cuotaPeriodica, 'cuotaCoohop':cuotaCoohop, 'cuotaVencida':cuotaVencida, 'valorVencido':valorVencido, 'valorVencidoMasc':valorVencidoMasc, 'valorVencidoRep':valorVencidoRep, 'valorVencidoSeg':valorVencidoSeg, 'valorVencidoAdic':valorVencidoAdic, 'valorVencidoCoohop':valorVencidoCoohop, 'pagoTotal':pagoTotal,'mes':mes, 'objBeneficiario':objBeneficiario, 'cuentaBeneficiario':cuentaBeneficiario, 'objMascota':objMascota, 'cuentaMascota':cuentaMascota, 'formato':5, 'saldo':saldo, 'mensaje':mensaje})
                
                # si no hay pagos en la bd
                except Exception as e:
                    valorVencidoMasc = objTarifaAsociado.cuotaMascota
                    valorVencidoRep = objTarifaAsociado.cuotaRepatriacion
                    valorVencidoSeg = objTarifaAsociado.cuotaSeguroVida
                    valorVencidoAdic = objTarifaAsociado.cuotaAdicionales
                    valorVencidoCoohop = objTarifaAsociado.cuotaCoohopAporte + objTarifaAsociado.cuotaCoohopBsocial
                    # obtenemos el parametro del primer mes q debe pagar
                    objParametroAsoc = ParametroAsociado.objects.get(asociado = asociado.pk)
                    cuotaVencida = mes.pk - objParametroAsoc.primerMes.pk
                    cuotaVencida += 1
                    if cuotaVencida == 0:
                        # mes seleccionado igual al parametro.primerMes
                        valorVencido = cuotaPeriodica
                        pagoTotal = valorVencido + valorVencidoMasc + valorVencidoRep + valorVencidoSeg + valorVencidoAdic + valorVencidoCoohop
                    elif cuotaVencida > 0:
                        # mes adelantado al parametro.primerMes
                        valorVencido = cuotaPeriodica * cuotaVencida
                        valorVencidoMasc = objTarifaAsociado.cuotaMascota * cuotaVencida
                        valorVencidoRep = objTarifaAsociado.cuotaRepatriacion * cuotaVencida
                        valorVencidoSeg = objTarifaAsociado.cuotaSeguroVida * cuotaVencida
                        valorVencidoAdic = objTarifaAsociado.cuotaAdicionales * cuotaVencida
                        valorVencidoCoohop = (objTarifaAsociado.cuotaCoohopAporte + objTarifaAsociado.cuotaCoohopBsocial) * cuotaVencida
                        pagoTotal = valorVencido + valorVencidoMasc + valorVencidoRep + valorVencidoSeg + valorVencidoAdic + valorVencidoCoohop
                    else:
                        pass
                    asociados.append({'pkAsociado':asociado.pk, 'fechaCorte':fechaCorte,'objAsoc':asociado, 'objResidencia':objResidencia, 'objTarifaAsociado':objTarifaAsociado, 'cuotaPeriodica':cuotaPeriodica, 'cuotaCoohop':cuotaCoohop, 'cuotaVencida':cuotaVencida, 'valorVencido':valorVencido, 'valorVencidoMasc':valorVencidoMasc, 'valorVencidoRep':valorVencidoRep, 'valorVencidoSeg':valorVencidoSeg, 'valorVencidoAdic':valorVencidoAdic, 'valorVencidoCoohop':valorVencidoCoohop, 'pagoTotal':pagoTotal,'mes':mes, 'objBeneficiario':objBeneficiario, 'cuentaBeneficiario':cuentaBeneficiario, 'objMascota':objMascota, 'cuentaMascota':cuentaMascota, 'formato':5, 'saldo':saldo})                     
        return render(request, template_name, {'lista':asociados, 'mes':mes})
    
class VerDescuentosNomina(ListView):
    template_name = 'reporte/dctosNomina.html'
    
    def get(self, request, *args, **kwargs):
        empresas = TipoAsociado.objects.all()
        return render(request, self.template_name, {'empresas':empresas})
    
    def post(self, request, *args, **kwargs):
        variable = request.POST.getlist('variable')
        empresas = TipoAsociado.objects.all()
        array = []
        arrayEmp = []
        for empresa in empresas:
            if len(request.POST.getlist('select'+str(empresa.pk))) == 1:
                query = ParametroAsociado.objects.filter(empresa = empresa.pk)
                # query = ParametroAsociado.objects.select_related('asociado').filter(empresa = empresa.pk)
                array.append(query)
                arrayEmp.append(empresa.pk)
        return render(request, self.template_name,{'array':array, 'post':'yes', 'empresas':empresas, 'arrayEmp':arrayEmp})
        