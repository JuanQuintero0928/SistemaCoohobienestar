// Funcion que cambia el formato numero a formato pesos para mostrar en el extracto
function formatearNumero(numero){
    numero = Number(numero);
    const formateado = numero.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    const numeroConSimbolo = `$ ${formateado}`;
    return numeroConSimbolo;
}

function formatearNumeroSinSimbolo(numero){
    numero = Number(numero);
    const formateado = numero.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    return formateado;
}

// Funcion que convierte la imagen en documento pdf para rellenar
function loadImage(url) {
    return new Promise(resolve => {
        const xhr = new XMLHttpRequest();
        xhr.open('GET',url,true);
        xhr.responseType = "blob";
        xhr.onload = function (e) {
            const reader = new FileReader();
            reader.onload = function(event) {
                const res = event.target.result;
                resolve(res);
            }
            const file = this.response;
            reader.readAsDataURL(file)
        }
        xhr.send();
    });
}

// Funcion que obtiene todos los datos del formulario para rellenarlos en el pdf
async function llamarPDF(numFormato, url) {
    // Obtenemos la informacion del model Asociado, del template formatos.html por medio de su id  
    switch(numFormato){
        // Formato Actualizacion y registro de asociado
        case 1:
            let actualizacion = document.getElementById('id_actualizacion').value;
            let fechaHoy = document.getElementById('id_fechaActual').value;
            let tPersona = document.getElementById('id_tPersona').value;
            let nombre = document.getElementById('id_nombre').value;
            let apellido = document.getElementById('id_apellido').value;
            let tipoDocumento = document.getElementById('id_tipoDocumento').value;
            let numDocumento = document.getElementById('id_numDocumento').value;
            let fechaExpedicion = document.getElementById('id_fechaExpedicion').value;
            let mpioDoc = document.getElementById('id_mpioDoc').value;
            let nacionalidad = document.getElementById('id_nacionalidad').value;
            let genero = document.getElementById('id_genero').value;
            let estadoCivil = document.getElementById('id_estadoCivil').value;
            let email = document.getElementById('id_email').value;
            let numResidencia = document.getElementById('id_numResidencia').value;
            let numCelular = document.getElementById('id_numCelular').value;
            let envioInfoCorreo = document.getElementById('id_envioInfoCorreo').value;
            let envioInfoMensaje = document.getElementById('id_envioInfoMensaje').value;
            let envioInfoWhatsapp = document.getElementById('id_envioInfoWhatsapp').value;
            let nivelEducativo = document.getElementById('id_nivelEducativo').value;
            let tituloPregrado = document.getElementById('id_tituloPregrado').value;
            let tituloPosgrado = document.getElementById('id_tituloPosgrado').value;
            let fechaNacimiento = document.getElementById('id_fechaNacimiento').value;
            let dtoNacimiento = document.getElementById('id_dtoNacimiento').value;
            let mpioNacimiento = document.getElementById('id_mpioNacimiento').value;
            let tipoVivienda = document.getElementById('id_tipoVivienda').value;
            let estrato = document.getElementById('id_estrato').value;
            let direccion = document.getElementById('id_direccion').value;
            let barrio = document.getElementById('id_barrio').value;
            let deptoResidencia = document.getElementById('id_deptoResidencia').value;
            let mpioResidencia = document.getElementById('id_mpioResidencia').value;
            // Obtenemos la informacion del model Laboral, del template formatos.html por medio de su id
            let ocupacion = document.getElementById('id_ocupacion').value;
            let nombreEmpresa = document.getElementById('id_nombreEmpresa').value;
            let cargo = document.getElementById('id_cargo').value;
            let nomRepresenLegal = document.getElementById('id_nomRepresenLegal').value;
            let numDocRL = document.getElementById('id_numDocRL').value;
            let fechaInicio = document.getElementById('id_fechaInicio').value;
            let fechaTerminacion = document.getElementById('id_fechaTerminacion').value;
            let direccionLab = document.getElementById('id_direccionLab').value;
            let mpioTrabajo = document.getElementById('id_mpioTrabajo').value;
            let dptoTrabajo = document.getElementById('id_dptoTrabajo').value;
            let telefono = document.getElementById('id_telefono').value;
            let admRP = document.getElementById('id_admRP').value;
            let pep = document.getElementById('id_pep').value;
            let activEcono = document.getElementById('id_activEcono').value;
            let ciiu = document.getElementById('id_ciiu').value;
            let banco = document.getElementById('id_banco').value;
            let numCuenta = document.getElementById('id_numCuenta').value;
            let tipoCuenta = document.getElementById('id_tipoCuenta').value;
            let nombreRF = document.getElementById('id_nombreRF').value;
            let parentesco = document.getElementById('id_parentesco').value;
            let numContacto = document.getElementById('id_numContacto').value;
            let autorizaciondcto = document.getElementById('id_autorizaciondcto').value;
            let empresa = document.getElementById('id_empresa').value;
            // Obtenemos la informacion del model Financiera, del template formatos.html por medio de su id
            let ingresosActPrin = document.getElementById('id_ingresosActPrin').value;
            let otroIngreso1 = document.getElementById('id_otroIngreso1').value;
            let otroIngreso2 = document.getElementById('id_otroIngreso2').value;
            let egresos = document.getElementById('id_egresos').value;
            let activos = document.getElementById('id_activos').value;
            let pasivos = document.getElementById('id_pasivos').value;
            let patrimonio = document.getElementById('id_patrimonio').value;
            // Obtenemos informacion del usuario que realiza la operacion
            let usuario = document.getElementById('usuario').value;
            generarPDF(url, nombre, apellido, tipoDocumento, numDocumento, fechaExpedicion, mpioDoc, nacionalidad, fechaNacimiento, genero, estadoCivil, email, numResidencia, numCelular,envioInfoCorreo, envioInfoMensaje, envioInfoWhatsapp, nivelEducativo, tituloPregrado, tituloPosgrado, dtoNacimiento, mpioNacimiento, tipoVivienda, estrato, direccion, barrio, deptoResidencia, mpioResidencia, ocupacion, nombreEmpresa, cargo, nomRepresenLegal, numDocRL, fechaInicio, fechaTerminacion, direccionLab, mpioTrabajo, dptoTrabajo, telefono, admRP, pep, activEcono, ciiu, banco, numCuenta, tipoCuenta, actualizacion, tPersona, fechaHoy, nombreRF, parentesco, numContacto, autorizaciondcto, empresa, ingresosActPrin, otroIngreso1, otroIngreso2, egresos, activos, pasivos, patrimonio, usuario);
        break
        // Formato Actualizacion servicios exequiales
        case 2:
            let actualizacionF2 = document.getElementById('id_actualizacion').value;
            let tPersonaF2 = document.getElementById('id_tPersona').value;
            let fechaHoyF2 = document.getElementById('id_fechaActual').value;
            let nombreF2 = document.getElementById('id_nombre').value;
            let apellidoF2 = document.getElementById('id_apellido').value;
            let tipoDocumentoF2 = document.getElementById('id_tipoDocumento').value;
            let numDocumentoF2 = document.getElementById('id_numDocumento').value;
            let emailF2 = document.getElementById('id_email').value;
            let numCelularF2 = document.getElementById('id_numCelular').value;
            let envioInfoCorreoF2 = document.getElementById('id_envioInfoCorreo').value;
            let envioInfoMensajeF2 = document.getElementById('id_envioInfoMensaje').value;
            let envioInfoWhatsappF2 = document.getElementById('id_envioInfoWhatsapp').value;
            let fechaNacimientoF2 = document.getElementById('id_fechaNacimiento').value;
            let direccionF2 = document.getElementById('id_direccion').value;
            let barrioF2 = document.getElementById('id_barrio').value;
            let mpioResidenciaF2 = document.getElementById('id_mpioResidencia').value;
            let numContactoF2 = document.getElementById('id_numContacto').value;
            // Obtenemos la informacion del model Beneficiarios, del template formatos.html por medio de su id
            let cuentaBeneficiarios = document.getElementById('id_cuentaBeneficiario').value;
            let arrayBeneficiarios = [];
            for(let i = 1; i <= cuentaBeneficiarios ; i++){
                let nombre = (document.getElementById('id_nombreBenef_'+i).value);
                let apellido = (document.getElementById('id_apellidoBenef_'+i).value);
                let numDocu = (document.getElementById('id_numDocume_'+i).value);
                let parentesco = (document.getElementById('id_parentesco_'+i).value);
                let nac = (document.getElementById('id_NacBen_'+i).value);
                let repatriacion = (document.getElementById('id_paisRepatriacion_'+i).value);
                let ciudadRepatriacion = (document.getElementById('id_ciudadRepatriacion_'+i).value);
                arrayBeneficiarios.push([nombre, apellido, numDocu, parentesco, nac, repatriacion, ciudadRepatriacion]);
            }
            // Obtenemos la informacion del model Mascota, del template formatos.html por medio de su id
            let cuentaMascota = document.getElementById('id_cuentaMascota').value;
            let arrayMascotas = [];
            if(cuentaMascota > 0){
                for(let i = 1; i <= cuentaMascota ; i++){
                    let nombreMasc = (document.getElementById('id_nombreMasc_'+i).value);
                    let tipoMasc = (document.getElementById('id_tipoMasc_'+i).value);
                    let raza = (document.getElementById('id_raza_'+i).value);
                    let nacMasc = (document.getElementById('id_nacMasc_'+i).value);
                    let vacunas = (document.getElementById('id_vacunas_'+i).value);
                    arrayMascotas.push([nombreMasc, tipoMasc, raza, nacMasc, vacunas]);
                }
            }
            generarPDFf2(url, actualizacionF2, tPersonaF2, fechaHoyF2, nombreF2, apellidoF2, tipoDocumentoF2, numDocumentoF2, emailF2, numCelularF2, direccionF2, barrioF2, mpioResidenciaF2, numContactoF2, cuentaBeneficiarios, arrayBeneficiarios, arrayMascotas, envioInfoCorreoF2, envioInfoMensajeF2, envioInfoWhatsappF2)
        break
        // Formato Solicitud auxilio
        case 3:
            let fechaHoyF3 = document.getElementById('id_fechaActual').value;
            let nombreF3 = document.getElementById('id_nombre').value;
            let apellidoF3 = document.getElementById('id_apellido').value;
            let tipoDocumentoF3 = document.getElementById('id_tipoDocumento').value;
            let numDocumentoF3 = document.getElementById('id_numDocumento').value;
            let fechaExpedicionF3 = document.getElementById('id_fechaExpedicion').value;
            let mpioDocF3 = document.getElementById('id_mpioDoc').value;
            let emailF3 = document.getElementById('id_email').value;
            let numCelularF3 = document.getElementById('id_numCelular').value;
            let envioInfoCorreoF3 = document.getElementById('id_envioInfoCorreo').value;
            let envioInfoMensajeF3 = document.getElementById('id_envioInfoMensaje').value;
            let envioInfoWhatsappF3 = document.getElementById('id_envioInfoWhatsapp').value;
            let direccionF3 = document.getElementById('id_direccion').value;
            let barrioF3 = document.getElementById('id_barrio').value;
            let mpioResidenciaF3 = document.getElementById('id_mpioResidencia').value;
            let fechaNacimientoF3 = document.getElementById('id_fechaNacimiento').value;
            // Obtenemos la informacion del model Laboral, del template formatos.html por medio de su id
            let nombreEmpresaF3 = document.getElementById('id_nombreEmpresa').value;
            let cargoF3 = document.getElementById('id_cargo').value;
            let telefonoF3 = document.getElementById('id_telefono').value;
            // Obtenemos la informacion del model Financiera, del template formatos.html por medio de su id
            let ingresosActPrinF3 = document.getElementById('id_ingresosActPrin').value;
            let bancoF3 = document.getElementById('id_banco').value;
            let numCuentaF3 = document.getElementById('id_numCuenta').value;
            // Obtenemos la informacion del model HistoricoAuxilio, del template formatos.html por medio de su id
            let tipoAuxilio = document.getElementById('id_tipoAuxilio').value;
            let nombre2 = document.getElementById('id_nombre2').value;
            let numDoc2 = document.getElementById('id_numDoc2').value;
            let parentescoF3 = document.getElementById('id_parentesco').value;
            let nivelEducativoF3 = document.getElementById('id_nivelEducativo').value;
            let anexoOne = document.getElementById('id_anexoOne').value;
            let anexoTwo = document.getElementById('id_anexoTwo').value;
            let anexoThree = document.getElementById('id_anexoThree').value;
            let anexoFour = document.getElementById('id_anexoFour').value;
            let anexoFive = document.getElementById('id_anexoFive').value;
            let anexoSix = document.getElementById('id_anexoSix').value;
            let anexoSeven = document.getElementById('id_anexoSeven').value;
            let anexoEight = document.getElementById('id_anexoEight').value;
            generarPDFf3(url, fechaHoyF3, nombreF3, apellidoF3, tipoDocumentoF3, numDocumentoF3, fechaExpedicionF3, mpioDocF3, emailF3, numCelularF3, direccionF3, barrioF3, mpioResidenciaF3, fechaNacimientoF3, nombreEmpresaF3, cargoF3, telefonoF3, ingresosActPrinF3, bancoF3, numCuentaF3, nombre2, numDoc2, parentescoF3, nivelEducativoF3, anexoOne, anexoTwo, anexoThree, anexoFour, anexoFive, anexoSix, anexoSeven, anexoEight, envioInfoCorreoF3, envioInfoMensajeF3, envioInfoWhatsappF3, tipoAuxilio)
        break
        // Formato Extracto
        case 4:
            let fechaCorte = document.getElementById('id_fechaCorte').value;
            let nombreF4 = document.getElementById('id_nombre').value;
            let numDocF4 = document.getElementById('id_numDoc').value;
            let mpioResidenciaF4 = document.getElementById('id_mpioResidencia').value;
            let direccionF4 = document.getElementById('id_direccion').value;
            let numCelularF4 = document.getElementById('id_numCelular').value;
            let concepto1 = document.getElementById('id_concepto1').value;
            let saldo = document.getElementById('id_saldo').value;
            let cuotaVencida = document.getElementById('id_cuotaVencida').value;
            let cuotaMes1 = document.getElementById('id_cuotaMes').value;
            let totalConcepto1 = document.getElementById('id_totalConcepto1').value;

            let concepto2 = document.getElementById('id_concepto2').value;
            let cuotaMes2 = document.getElementById('id_cuotaMes2').value;
            let totalConcepto2 = document.getElementById('id_totalConcepto2').value;

            let concepto3 = document.getElementById('id_concepto3').value;
            let cuotaMes3 = document.getElementById('id_cuotaMes3').value;
            let totalConcepto3 = document.getElementById('id_totalConcepto3').value;

            let concepto4 = document.getElementById('id_concepto4').value;
            let cuotaMes4 = document.getElementById('id_cuotaMes4').value;
            let totalConcepto4 = document.getElementById('id_totalConcepto4').value;

            let concepto5 = document.getElementById('id_concepto5').value;
            let cuotaMes5 = document.getElementById('id_cuotaMes5').value;
            let totalConcepto5 = document.getElementById('id_totalConcepto5').value;

            let concepto6 = document.getElementById('id_concepto6').value;
            let cuotaMes6 = document.getElementById('id_cuotaMes6').value;
            let totalConcepto6 = document.getElementById('id_totalConcepto6').value;

            // let concepto7 = document.getElementById('id_concepto7').value;
            // let cuotaMes7 = document.getElementById('id_cuotaMes7').value;
            // let totalConcepto7 = document.getElementById('id_totalConcepto7').value;
            
            let arrayConveniosF4 = []
            const convenios = document.querySelectorAll(".convenio");
            convenios.forEach((c, index) => {
                const concepto = c.querySelector(".concepto").value;
                const cantidadMeses = c.querySelector(".cantidad_meses").value;
                const valorMes = c.querySelector(".cuota_mes").value;
                const total = c.querySelector(".valor_vencido_convenio").value;
                arrayConveniosF4.push({
                    concepto: concepto,
                    cantidadMeses: parseInt(cantidadMeses),
                    valorMes: parseFloat(valorMes),
                    total: parseFloat(total)
                });
            });

            let pagoTotal = document.getElementById('id_pagoTotal').value;
            let mensaje = document.getElementById('id_mensaje').value;
            // Obtenemos la informacion del model Beneficiarios, del template formatos.html por medio de su id
            let cuentaBeneficiariosF4 = document.getElementById('id_cuentaBeneficiario').value;
            let arrayBeneficiariosF4 = [];
            for(let i = 1; i <= cuentaBeneficiariosF4 ; i++){
                let nombre = (document.getElementById('id_nombreBenef_'+i).value);
                let parentesco = (document.getElementById('id_parentesco_'+i).value);
                let repatriacion = (document.getElementById('id_paisRepatriacion_'+i).value);
                arrayBeneficiariosF4.push([nombre, parentesco, repatriacion]);
            }
            // Obtenemos la informacion del model Mascota, del template formatos.html por medio de su id
            let cuentaMascotaF4 = document.getElementById('id_cuentaMascota').value;
            let arrayMascotasF4 = [];
            if(cuentaMascotaF4 > 0){
                for(let i = 1; i <= cuentaMascotaF4 ; i++){
                    let nombreMasc = (document.getElementById('id_nombreMasc_'+i).value);
                    arrayMascotasF4.push([nombreMasc]);
                }
            }
            let pdf = generarPDFf4(url, fechaCorte, nombreF4, numDocF4, mpioResidenciaF4, direccionF4, numCelularF4, concepto1, cuotaVencida, cuotaMes1, totalConcepto1, concepto2, cuotaMes2, totalConcepto2, concepto3, cuotaMes3, totalConcepto3, concepto4, cuotaMes4, totalConcepto4, concepto5, cuotaMes5, totalConcepto5, concepto6, cuotaMes6, totalConcepto6, arrayConveniosF4, pagoTotal, cuentaBeneficiariosF4, arrayBeneficiariosF4, arrayMascotasF4, saldo, mensaje)
            return pdf;
    }
}

async function llamarPDFCredito(valor, cuotas, url, idCredito) {
    let fechaHoy_F5 = document.getElementById('id_fechaActual').value;
    let nombre_F5 = document.getElementById('id_nombre').value;
    let apellido_F5 = document.getElementById('id_apellido').value;
    let tipoDocumento_F5 = document.getElementById('id_tipoDocumento').value;
    let numDocumento_F5 = document.getElementById('id_numDocumento').value;
    let fechaExpedicion_F5 = document.getElementById('id_fechaExp').value;
    let mpioDoc_F5 = document.getElementById('id_lugarExp').value;
    let nacionalidad_F5 = document.getElementById('id_nacionalidad').value;
    let genero_F5 = document.getElementById('id_genero').value;
    let estadoCivil_F5 = document.getElementById('id_estadoCivil').value;
    let email_F5 = document.getElementById('id_email').value;
    let numCelular_F5 = document.getElementById('id_numCelular').value;
    let numResidencia_F5 = document.getElementById('id_numResidencia').value;
    let fechaNacimiento_F5 = document.getElementById('id_fechaNac').value;
    let dtoNacimiento_F5 = document.getElementById('id_dtoNac').value;
    let mpioNacimiento_F5 = document.getElementById('id_mpioNac').value;
    let tipoVivienda_F5 = document.getElementById('id_tipoVivienda').value;
    let estrato_F5 = document.getElementById('id_estrato').value;
    let direccion_F5 = document.getElementById('id_direccion').value;
    let barrio_F5 = document.getElementById('id_barrio').value;
    let deptoResidencia_F5 = document.getElementById('id_deptoResidencia').value;
    let mpioResidencia_F5 = document.getElementById('id_mpioResidencia').value;
    let envioInfoCorreo_F5 = document.getElementById('id_envioInfoCorreo').value;
    let envioInfoMensaje_F5 = document.getElementById('id_envioInfoMensaje').value;
    let envioInfoWhatsapp_F5 = document.getElementById('id_envioInfoWhatsapp').value;
    let nivelEducativo_F5 = document.getElementById('id_nivelEducativo').value;
    let profesion_F5 = document.getElementById('id_tituloPregrado').value;
    let nombreEmpresa_F5 = document.getElementById('id_nombreEmpresa').value;
    let cargo_F5 = document.getElementById('id_cargo').value;
    let fechaInicio_F5 = document.getElementById('id_fechaInicio').value;
    let fechaTerminacion_F5 = document.getElementById('id_fechaTerminacion').value;
    let nomRepresenLegal_F5 = document.getElementById('id_nomRepresenLegal').value;
    let numDocRL_F5 = document.getElementById('id_numDocRL').value;
    let direccionTrabajo_F5 = document.getElementById('id_direccionTrabajo').value;
    let mpioTrabajo_F5 = document.getElementById('id_mpioTrabajo').value;
    let dptoTrabajo_F5 = document.getElementById('id_dptoTrabajo').value;
    let telefono_F5 = document.getElementById('id_telefono').value;
    let admRP_F5 = document.getElementById('id_admRP').value;
    let pep_F5 = document.getElementById('id_pep').value;
    let activEcono_F5 = document.getElementById('id_activEcono').value;
    let ciiu_F5 = document.getElementById('id_ciiu').value;
    let banco_F5 = document.getElementById('id_banco').value;
    let numCuenta_F5 = document.getElementById('id_numCuenta').value;
    let tipoCuenta_F5 = document.getElementById('id_tipoCuenta').value;
    let usuario_F5 = document.getElementById('usuario').value;
    let autorizaciondcto_F5 = document.getElementById('id_autorizaciondcto').value;
    let empresa_F5 = document.getElementById('id_empresa').value;
    let lineaCredito_F5 = document.getElementById(`lineaCredito${idCredito}`).value;
    let medioPago_F5 = document.getElementById(`medioPago${idCredito}`).value;
    let formaDesembolso_F5 = document.getElementById(`formaDesembolso${idCredito}`).value;
    let existCodeudor = document.getElementById(`existCodeudor${idCredito}`).value;

    generarPDFfCredito(url, valor, cuotas, nombre_F5, apellido_F5, tipoDocumento_F5, numDocumento_F5, fechaExpedicion_F5, mpioDoc_F5, nacionalidad_F5, fechaNacimiento_F5, genero_F5, estadoCivil_F5, email_F5, numCelular_F5, dtoNacimiento_F5, mpioNacimiento_F5, tipoVivienda_F5, estrato_F5, direccion_F5, barrio_F5, deptoResidencia_F5, mpioResidencia_F5, usuario_F5, fechaHoy_F5, numResidencia_F5, envioInfoCorreo_F5, envioInfoMensaje_F5, envioInfoWhatsapp_F5, profesion_F5, nombreEmpresa_F5, cargo_F5, fechaInicio_F5, fechaTerminacion_F5, nomRepresenLegal_F5, numDocRL_F5, mpioTrabajo_F5, dptoTrabajo_F5, telefono_F5, admRP_F5, pep_F5, activEcono_F5, ciiu_F5, banco_F5, numCuenta_F5, tipoCuenta_F5, direccionTrabajo_F5, nivelEducativo_F5, autorizaciondcto_F5, empresa_F5, lineaCredito_F5, medioPago_F5, formaDesembolso_F5, existCodeudor); 
}

async function llamarPDFPagare(url, numDoc, idCredito) {
    const existCodeudor = document.getElementById(`existCodeudor${idCredito}`).value;
    let fechaHoy_F5 = document.getElementById('id_fechaActual').value;


    const datos = {
        existCodeudor: existCodeudor,
        nombre: document.getElementById('id_nombre').value,
        apellido: document.getElementById('id_apellido').value,
        numDocumento: document.getElementById('id_numDocumento').value,
        tipoDocumento: document.getElementById('id_tipoDocumento').value,
        mpioDoc: document.getElementById('id_lugarExp').value,
        email: document.getElementById('id_email').value,
        celular: document.getElementById('id_numCelular').value,
        direccion: document.getElementById('id_direccion').value,
    };

    if(existCodeudor === "True"){
        datos.nombreCodeudor = document.getElementById(`nombreCod${idCredito}`).value;
        datos.apellidoCodeudor = document.getElementById(`apellidoCod${idCredito}`).value;
        datos.tipoDocumentoCodeudor = document.getElementById(`tipoDocumentoCod${idCredito}`).value;
        datos.numDocumentoCodeudor = document.getElementById(`numDocumentoCod${idCredito}`).value;
        datos.mpioCodeudor = document.getElementById(`mpioDocCod${idCredito}`).value;
        datos.emailCodeudor = document.getElementById(`emailCod${idCredito}`).value;
        datos.celularCodeudor = document.getElementById(`numCelularCod${idCredito}`).value;
        datos.direccionCodeudor = document.getElementById(`direccionCod${idCredito}`).value;
    }else {
        datos.nombreCodeudor = '';
        datos.apellidoCodeudor = '';
        datos.tipoDocumentoCodeudor = '';
        datos.numDocumentoCodeudor = '';
        datos.mpioCodeudor = '';
        datos.emailCodeudor = '';
        datos.celularCodeudor = '';
        datos.direccionCodeudor = '';
    }

    descargarPagare(url, numDoc, datos, fechaHoy_F5);
}
    

async function llamarPDFTablaAmortizacion(url, numDoc, fechaSolicitud, valor, cuotas, tasa, idCredito) {
    
    const existCodeudor = document.getElementById(`existCodeudor${idCredito}`).value;
    
    const datos = {
        existCodeudor: existCodeudor,
        numCredito: document.getElementById(`numCredito${idCredito}`).value,
        nombre: document.getElementById('id_nombre').value,
        apellido: document.getElementById('id_apellido').value,
        numDocumento: document.getElementById('id_numDocumento').value,
        tipoDocumento: document.getElementById('id_tipoDocumento').value,
        mpioDoc: document.getElementById('id_lugarExp').value,

        lineaCredito: document.getElementById(`lineaCredito${idCredito}`).value,
        amortizacion: document.getElementById(`amortizacion${idCredito}`).value,
        medioPago: document.getElementById(`medioPago${idCredito}`).value,
        valorCuota: document.getElementById(`valorCuota${idCredito}`).value,
        totalCredito: document.getElementById(`totalCredito${idCredito}`).value,
    };

    if(existCodeudor === "True"){
        datos.nombreCodeudor = document.getElementById(`nombreCod${idCredito}`).value;
        datos.apellidoCodeudor = document.getElementById(`apellidoCod${idCredito}`).value;
        datos.tipoDocumentoCodeudor = document.getElementById(`tipoDocumentoCod${idCredito}`).value;
        datos.numDocumentoCodeudor = document.getElementById(`numDocumentoCod${idCredito}`).value;
        datos.mpioCodeudor = document.getElementById(`mpioDocCod${idCredito}`).value;
    }else {
        datos.nombreCodeudor = '';
        datos.apellidoCodeudor = '';
        datos.tipoDocumentoCodeudor = '';
        datos.numDocumentoCodeudor = '';
        datos.mpioCodeudor = '';
    }
    
    descargarTablaAmortizacion(url, numDoc, fechaSolicitud, valor, cuotas, tasa, datos);
}

// Formato 1
// Formato de registro y actualizacion
async function generarPDF(url, nombre, apellido, tipoDocumento, numDocumento, fechaExpedicion, mpioDoc, nacionalidad, fechaNacimiento, genero, estadoCivil, email, numResidencia, numCelular,envioInfoCorreo, envioInfoMensaje, envioInfoWhatsapp, nivelEducativo, tituloPregrado, tituloPosgrado, dtoNacimiento, mpioNacimiento, tipoVivienda, estrato, direccion, barrio, deptoResidencia, mpioResidencia, ocupacion, nombreEmpresa, cargo, nomRepresenLegal, numDocRL, fechaInicio, fechaTerminacion, direccionLab, mpioTrabajo, dptoTrabajo, telefono, admRP, pep, activEcono, ciiu, banco, numCuenta, tipoCuenta, actualizacion, tPersona, fechaHoy, nombreRF, parentesco, numContacto, autorizaciondcto, empresa, ingresosActPrin, otroIngreso1, otroIngreso2, egresos, activos, pasivos, patrimonio, usuario) {

    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'legal');
    pdf.addImage(image, 'PNG', 0, 0, 613, 1010);

    pdf.setFontSize(12);

    // fecha encabezado
    var arrFechaHoy = fechaHoy.split("-")
    pdf.text(arrFechaHoy[2], 253,135);
    pdf.text(arrFechaHoy[1], 292,135);
    pdf.text(arrFechaHoy[0], 332,135);

    // renglon 0
    if(actualizacion == "True"){
        pdf.text("X", 411, 157);
    }else if(tPersona == "PERSONA NATURAL"){
        pdf.text("X", 22, 157);
    }else{
        pdf.text("X", 222, 157);
    }

    // renglon 1
    pdf.text(nombre, 20,219);
    pdf.text(apellido, 322,219);

    // renglon 2
    if(tipoDocumento == 'CEDULA'){
        pdf.text("X", 40, 252);
    }else if (tipoDocumento == 'REGISTRO CIVIL'){
        pdf.text("X", 20, 252);
    }else if(tipoDocumento == 'TARJETA IDENTIDAD'){
        pdf.text("X", 62, 252);
    }else if(tipoDocumento == 'CEDULA EXTRANJERIA'){
        pdf.text("X", 82, 252);
    }else{
        pdf.text("X", 105, 252);
    }
    pdf.text(numDocumento, 132,252);
    // se separa la fecha en un array por -
    var arrFechaExp = fechaExpedicion.split("-")
    pdf.text(arrFechaExp[2], 326,252);
    pdf.text(arrFechaExp[1], 358,252);
    pdf.text(arrFechaExp[0], 395,252);
    pdf.text(mpioDoc, 440,252);

    // renglon 3
    pdf.text(nacionalidad, 20,300);
    var arrFechaNac = fechaNacimiento.split("-")
    pdf.text(arrFechaNac[2], 157,300);
    pdf.text(arrFechaNac[1], 192,300);
    pdf.text(arrFechaNac[0], 230,300);
    pdf.text(dtoNacimiento, 280,300);
    pdf.text(mpioNacimiento, 383,300);

    if(genero == 'FEMENINO'){
        pdf.text('X', 508,300)
    }else{
        pdf.text('X', 559,300);
    }

    // renglon 4
    if(estadoCivil == 'SOLTERO(A)'){
        pdf.text("X", 30, 333);
    }else if (estadoCivil == 'CASADO(A)'){
        pdf.text("X", 74, 333);
    }else if(estadoCivil == 'UNION LIBRE'){
        pdf.text("X", 120, 333);
    }else if(estadoCivil == 'SEPARADO(A)'){
        pdf.text("X", 160, 333);
    }else if(estadoCivil == 'DIVORCIADO(A)'){
        pdf.text("X", 208, 333);
    }else{
        pdf.text("X", 256, 333);
    }

    if(tipoVivienda == 'PROPIA'){
        pdf.text("X", 294, 333);
    }else if(tipoVivienda == 'FAMILIAR'){
        pdf.text("X", 347, 333);
    }else{
        pdf.text("X", 405, 333);
    }
 
    if(estrato == 1){
        pdf.text("X", 441, 333);
    }else if(estrato == 2){
        pdf.text("X", 470, 333);
    }else if(estrato == 3){
        pdf.text("X", 499, 333);
    }else if(estrato == 4){
        pdf.text("X", 524, 333);
    }else if(estrato == 5){
        pdf.text("X", 547, 333);
    }else{
        pdf.text("X", 576, 333);
    }

    // renglon 5
    pdf.text(direccion, 20, 367);
    pdf.text(barrio, 285, 367);
    pdf.text(mpioResidencia, 473, 367);

    // renglon 6
    pdf.text(deptoResidencia, 20, 399);
    pdf.text(email, 135, 399);
    pdf.text(numResidencia, 394, 399);
    pdf.text(numCelular, 500, 399);

    // renglon 7
    if(envioInfoCorreo == "True"){
        pdf.text("X", 104, 431)
    }
    if(envioInfoMensaje == "True"){
        pdf.text("X", 227, 431)
    }
    if(envioInfoWhatsapp == "True"){
        pdf.text("X", 330, 431)
    }

    // renglon 8
    if(nivelEducativo == "PRIMARIA"){
        pdf.text("X", 30, 463);
    }else if(nivelEducativo == "SECUNDARIA"){
        pdf.text("X", 74, 463);
    }else if(nivelEducativo == "TECNICO"){
        pdf.text("X", 121, 463);
    }else if(nivelEducativo == "TECNOLOGICO"){
        pdf.text("X", 178, 463);
    }else if(nivelEducativo == "PREGRADO"){
        pdf.text("X", 243, 463);
    }else if(nivelEducativo == "ESPECIALIZACION"){
        pdf.text("X", 308, 463);
    }else if(nivelEducativo == "MAESTRIA"){
        pdf.text("X", 363, 463);
    }else{
        pdf.text("X", 406, 463);
    }

    // renglon 9
    if(tituloPregrado != "None"){
        pdf.text(tituloPregrado, 20, 497);
    }
    if(tituloPosgrado != "None"){
        pdf.text(tituloPosgrado, 333, 497);
    }

    // renglon 10
    pdf.text(ocupacion, 20, 533);
    pdf.text(nombreEmpresa, 158, 533);
    pdf.text(cargo, 421, 533);

    // renglon 11
    pdf.text(nomRepresenLegal, 20, 570);
    if(numDocRL != "None"){
        pdf.text(numDocRL, 231, 570);
    }
    if(fechaInicio != ''){
        var arrFechaInicio = fechaInicio.split("-")
        pdf.text(arrFechaInicio[2], 440,570);
        pdf.text(arrFechaInicio[1], 467,570);
        pdf.text(arrFechaInicio[0], 489,570);
    
    }
    if(fechaTerminacion != ''){
        var arrFechaTerminacion = fechaTerminacion.split("-")
        pdf.text(arrFechaTerminacion[2], 521,570);
        pdf.text(arrFechaTerminacion[1], 544,570);
        pdf.text(arrFechaTerminacion[0], 566,570);
    }
    
    // renglon 12
    pdf.text(direccionLab, 20, 603);
    if(mpioTrabajo != 'None'){
        pdf.text(mpioTrabajo, 256, 603);
    }
    if(dptoTrabajo != 'None'){
        pdf.text(dptoTrabajo, 395, 603);
    }
    if(telefono != "None"){
        pdf.text(telefono, 503, 603);
    }

    // renglon 13
    if(admRP == "SI"){
        pdf.text("X", 42, 638);
    }else{
        pdf.text("X", 105, 638);
    }
    if(pep == "SI"){
        pdf.text("X", 192, 638);
    }else{
        pdf.text("X", 278, 638);
    }
    if(activEcono != 'None'){
        pdf.text(activEcono, 326, 638);
    }
    if(ciiu != 'None'){
        pdf.text(ciiu, 550, 638);
    }
    
    // renglon 14
    pdf.text(banco, 20, 672);
    if(numCuenta != 'None'){
        pdf.text(numCuenta, 329, 672);
    }
    if(tipoCuenta != 0){
        pdf.text(tipoCuenta, 471, 672);
    }
    // Informacion Financiera
    pdf.text(ingresosActPrin, 400, 725);
    if(otroIngreso1 != 'None'){
        pdf.text(otroIngreso1, 400, 740);
    }
    if(otroIngreso2 != 'None'){
        pdf.text(otroIngreso2, 400, 755);
    }
    if(egresos != 'None'){
        pdf.text(egresos, 400, 815);
    }
    if(activos != 'None'){
        pdf.text(activos, 400, 840);
    }
    if(pasivos != 'None'){
        pdf.text(pasivos, 400, 855);
    }
    if(patrimonio != 'None'){
        pdf.text(patrimonio, 400, 870);
    }

    // renglon referencia familiar
    pdf.text(nombreRF, 23, 938);
    pdf.text(parentesco, 314, 938);
    pdf.text(numContacto, 471, 938);


    /////////////////////////////////////////////////////////////////////////////////////////
    // Se añade Pagina 2 al documento
    pdf.addPage();
    const image2 = await loadImage('/static/img/Registro_page_0002.jpg');
    pdf.addImage(image2, 'PNG', 0, 0, 613, 1010);

    // Firma del Asociado
    var nomCompleto = nombre + " "+ apellido
    pdf.text(nomCompleto, 165, 784);
    pdf.text(numDocumento, 165, 811);

    // Autorizacion descuento Nomina
    // se realiza validacion para insertar el texto en el documento
    if(autorizaciondcto == "True"){
        pdf.setFontSize(10);
        pdf.text(nomCompleto, 36, 862);
        pdf.text(mpioResidencia, 423, 862);
        pdf.text(numDocumento, 85, 872);
        pdf.text(mpioDoc, 222, 872);
        pdf.text(empresa, 152, 916);
    } 


    /////////////////////////////////////////////////////////////////////////////////////////
    // Se añade Pagina 3 al documento
    pdf.addPage();
    const image3 = await loadImage('/static/img/Registro_page_0003.jpg');
    pdf.addImage(image3, 'PNG', 0, 0, 613, 1010);
    
    // Firma y Huella
    pdf.setFontSize(12);
    pdf.text(arrFechaHoy[2], 227,680);
    pdf.text(arrFechaHoy[1], 372,680);
    pdf.text(arrFechaHoy[0], 495,680);
    pdf.text("ARMENIA", 25, 690);

    // Ultima Fila
    pdf.text(nomCompleto, 165, 752);
    pdf.text(numDocumento, 165, 773);

    // Espacio reservado para coohobienestar
    pdf.setFontSize(10);
    pdf.text(arrFechaHoy[2], 60,837);
    pdf.text(arrFechaHoy[1], 82,837);
    pdf.text(arrFechaHoy[0], 105,837);
    pdf.text(usuario, 227,837);
    pdf.text("Auxiliar administrativo", 495,837);

    pdf.save('Formato_Registro_'+numDocumento+'.pdf');


}

// Formato 2
// Formato Servicios Exequiales
async function generarPDFf2(url, actualizacionF2, tPersonaF2, fechaHoyF2, nombreF2, apellidoF2, tipoDocumentoF2, numDocumentoF2, emailF2, numCelularF2, direccionF2, barrioF2, mpioResidenciaF2, numContactoF2, cuentaBeneficiarios, arrayBeneficiarios, arrayMascotas, envioInfoCorreoF2, envioInfoMensajeF2, envioInfoWhatsappF2) {

    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'legal');
    pdf.addImage(image, 'PNG', 0, 0, 613, 1010);

    pdf.setFontSize(12);

    // fecha encabezado
    var arrFechaHoy = fechaHoyF2.split("-");
    const fechaF2 = arrFechaHoy[2] + '/' + arrFechaHoy[1] + '/' + arrFechaHoy[0];
    pdf.text(fechaF2, 276,111);

    // renglon 0
    if(actualizacionF2 == "True"){
        pdf.text("X", 417, 130);
    }else if(tPersonaF2 == "PERSONA NATURAL"){
        pdf.text("X", 20, 130);
    }else{
        pdf.text("X", 218, 130);
    }

    // Fila 1
    pdf.text(nombreF2, 19,184);
    pdf.text(apellidoF2, 322,184);

    // Fila 2
    if(tipoDocumentoF2 == 'REGISTRO CIVIL'){
        pdf.text("X", 20,215);
    }else if (tipoDocumentoF2 == 'CEDULA'){
        pdf.text("X", 40,215);
    }else if (tipoDocumentoF2 == 'TARJETA IDENTIDAD'){
        pdf.text("X", 63,215);
    }else if (tipoDocumentoF2 == 'CEDULA EXTRANJERIA'){
        pdf.text("X", 83,215);
    }else{
        pdf.text("X", 105,215);
    }

    pdf.text(numDocumentoF2, 133,216);
    pdf.text(direccionF2, 324,216);

    // Fila 3
    pdf.text(barrioF2, 19,248);
    pdf.text(mpioResidenciaF2, 190,248);
    pdf.text(numCelularF2, 323,248);
    pdf.text(numContactoF2, 471,248);

    // Fila 4
    pdf.text(emailF2, 19,281);

    // Fila 5
    if(envioInfoCorreoF2 == "True"){
        pdf.text("X", 105,313);
    }
    if(envioInfoMensajeF2 == "True"){
        pdf.text("X", 228,313);
    }
    if(envioInfoWhatsappF2 == "True"){
        pdf.text("X", 329,313);
    }

    //  Cuadro de beneficiarios
    pdf.setFontSize(9);
    let fila = 401;
    let filaR = 598;
    for(let i = 0; i < arrayBeneficiarios.length; i++){
        // se diligencia el cuadro de beneficiarios
        pdf.text("X", 51,fila);
        pdf.setFontSize(8);
        pdf.text(arrayBeneficiarios[i][0], 125 ,fila);
        if(arrayBeneficiarios[i][1] == 'CEDULA'){
            pdf.text('CC', 315 ,fila);
        }else if(arrayBeneficiarios[i][1] == 'REGISTRO CIVIL'){
            pdf.text('RC', 315 ,fila);
        }else if(arrayBeneficiarios[i][1] == 'REGISTRO CIVIL'){
            pdf.text('RC', 315 ,fila);
        }else if(arrayBeneficiarios[i][1] == 'TARJETA IDENTIDAD'){
            pdf.text('TI', 315 ,fila);
        }else if(arrayBeneficiarios[i][1] == 'CEDULA EXTRANJERA'){
            pdf.text('CE', 315 ,fila);
        }else if(arrayBeneficiarios[i][1] == 'PASAPORTE'){
            pdf.text('PA', 315 ,fila);
        }
        pdf.text(arrayBeneficiarios[i][2], 367 ,fila);
        pdf.text(arrayBeneficiarios[i][3], 451 ,fila);
        var fecha = arrayBeneficiarios[i][4].split("-");
        pdf.text(fecha[2], 530 ,fila);
        pdf.text(fecha[1], 552 ,fila);
        pdf.text(fecha[0], 574 ,fila);
        // se diligencia el cuadro de repatriacion
        if(arrayBeneficiarios[i][5] != 'None'){
            pdf.text("X", 51,filaR);
            pdf.setFontSize(8);
            pdf.text(arrayBeneficiarios[i][0], 125 ,filaR);
            pdf.text(arrayBeneficiarios[i][2], 299 ,filaR);
            pdf.text(arrayBeneficiarios[i][6], 393 ,filaR);
            pdf.text(arrayBeneficiarios[i][5], 499 ,filaR);
        }
        if(arrayBeneficiarios[i][5] != 'None'){
            filaR = filaR + 15;
        }
        fila = fila + 15;
    }

    // Se diligencia Cuadro de Mascota
    let filaM = 705;
    for(let i = 0; i < arrayMascotas.length; i++){
        pdf.text("X", 51,filaM);
        pdf.text(arrayMascotas[i][0], 125 ,filaM);
        if(arrayMascotas[i][1] == 'GATO'){
            pdf.text("X", 283 ,filaM);
        }else{
            pdf.text("X", 305 ,filaM);
        }
        pdf.text(arrayMascotas[i][2], 321 ,filaM);
        var fechaMasc = arrayMascotas[i][3].split("-");
        pdf.text(fechaMasc[2], 447 ,filaM);
        pdf.text(fechaMasc[1], 474 ,filaM);
        pdf.text(fechaMasc[0], 500 ,filaM);
        if(arrayMascotas[i][4] == 'True'){
            pdf.text("X", 543 ,filaM);
        }else{
            pdf.text("X", 580 ,filaM);
        }
        filaM = filaM + 14.5;    
    }

    // Firma y Huella
    pdf.setFontSize(12);
    pdf.text(arrFechaHoy[2], 299,861);
    pdf.text(arrFechaHoy[1], 444,861);
    pdf.text(arrFechaHoy[0], 541,861);
    pdf.text("Armenia", 72,871);

    // Firma
    var nomCompleto = nombreF2 + " " + apellidoF2
    pdf.text(nomCompleto, 155 ,929);
    pdf.text(numDocumentoF2, 155 ,952);

    pdf.save('Formato_Servicios_Exequiales_'+numDocumentoF2+'.pdf');

}

// Formato 3
// Formato Auxilios
async function generarPDFf3(url, fechaHoyF3, nombreF3, apellidoF3, tipoDocumentoF3, numDocumentoF3, fechaExpedicionF3, mpioDocF3, emailF3, numCelularF3, direccionF3, barrioF3, mpioResidenciaF3, fechaNacimientoF3, nombreEmpresaF3, cargoF3, telefonoF3, ingresosActPrinF3, bancoF3, numCuentaF3, nombre2, numDoc2, parentescoF3, nivelEducativoF3, anexoOne, anexoTwo, anexoThree, anexoFour, anexoFive, anexoSix, anexoSeven, anexoEight, envioInfoCorreoF3, envioInfoMensajeF3, envioInfoWhatsappF3, tipoAuxilio) {
    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'legal');
    pdf.addImage(image, 'PNG', 0, 0, 613, 1010);

    pdf.setFontSize(12);

    // fecha encabezado
    var arrFechaHoy = fechaHoyF3.split("-");
    const fecha = arrFechaHoy[2] + '/' + arrFechaHoy[1] + '/' + arrFechaHoy[0];
    pdf.text(fecha, 274,110);
    
    // renglon 0
    pdf.text(nombreF3, 17,162);
    pdf.text(apellidoF3, 323,162);

    // // renglon 1
    if (tipoDocumentoF3 == 'REGISTRO CIVIL'){
        pdf.text("X", 19,190);
    }else if (tipoDocumentoF3 == 'CEDULA'){
        pdf.text("X", 41,190);
    }else if (tipoDocumentoF3 == 'TARJETA IDENTIDAD'){
        pdf.text("X", 63,190);
    }else if (tipoDocumentoF3 == 'CEDULA EXTRANJERA'){
        pdf.text("X", 83,190);
    }else if (tipoDocumentoF3 == 'PASAPORTE'){
        pdf.text("X", 105,190);
    }else{
        // Si no es ninguno de los anteriores, se marca cedula extranjera ya que no hay casilla de ppt
        pdf.text("X", 83,190);
    }
    pdf.text(numDocumentoF3, 137,190);
    pdf.text(direccionF3, 323,190);

    // // renglon 2
    pdf.setFontSize(8);
    pdf.text(barrioF3, 17,219);
    pdf.text(mpioResidenciaF3, 187,219);
    pdf.setFontSize(12);
    pdf.text(numCelularF3, 465,219);

    // // renglon 3
    pdf.text(emailF3, 17,247);

    // // renglon 4
    pdf.text(bancoF3, 17,276);
    pdf.text(numCuentaF3, 325,276);

    // // renglon 5
    // campo autorizacion envio informacion
    if(envioInfoCorreoF3 == 'True'){
        pdf.text("X", 106, 305);
    }

    if(envioInfoMensajeF3 == 'True'){
        pdf.text("X", 227, 305);
    }

    if(envioInfoWhatsappF3 == 'True'){
        pdf.text("X", 329, 305);
    }

    // Tipos Auxilios
    // optico
    if(tipoAuxilio == '1'){
        pdf.text("X", 40,420);
    }// incapacidad medica
    else if(tipoAuxilio == '2'){
        pdf.text("X", 329,403);
    }// auxilio educativo-u
    else if(tipoAuxilio == '4'){
        pdf.text("X", 40,384);
    }// kit maternidad
    else if(tipoAuxilio == '3'){
        pdf.text("X", 329,349);
    }//auxilio educativo-maestria
    else if(tipoAuxilio == '5'){
        pdf.text("X", 40,403);
    }// Auxilio Educativo Tecnico
    else if(tipoAuxilio == '6'){
        pdf.text("X", 40,349);
    }//calamidad domestica
    else if(tipoAuxilio == '7'){
        pdf.text("X", 329,367);
    }//calamidad domestica-medica
    else if(tipoAuxilio == '8'){
        pdf.text("X", 329,384);
    }// Auxilio Educativo Tenologia
    else if(tipoAuxilio == '8'){
        pdf.text("X", 40,367);
    }

    // Campo - se solicita para
    if(tipoAuxilio == '4' || tipoAuxilio == '5' || tipoAuxilio == '6' || tipoAuxilio == '9'){
        pdf.text(nombre2, 17, 480);
        pdf.text(numDoc2, 325, 480);
        pdf.text(parentescoF3, 480, 480);
        pdf.text(nivelEducativoF3, 127, 494);
    }

    // Campo - Anexos
    pdf.setFontSize(10);

    const anexos = []

    if(anexoOne != 'None'){
        anexos.push(anexoOne);
    }
    if(anexoTwo != 'None'){
        anexos.push(anexoTwo);
    }
    if(anexoThree != 'None'){
        anexos.push(anexoThree);
    }
    if(anexoFour != 'None'){
        anexos.push(anexoFour);
    }
    if(anexoFive != 'None'){
        anexos.push(anexoFive);  
    }
    if(anexoSix != 'None'){
        anexos.push(anexoSix);
    }
    if(anexoSeven != 'None'){
        anexos.push(anexoSeven);
    }
    if(anexoEight != 'None'){
        anexos.push(anexoEight);
    }

    const texto = anexos.join(', ');

    // Maximo 82 caracteres
    const maxCaracteres = 82;

    // Dividir el texto en lineas de maximo 82 caracteres
    const lineas = [];
    for (let i = 0; i < texto.length; i += maxCaracteres) {
        lineas.push(texto.substring(i, i + maxCaracteres));
    }

    // Imprimir las lineas en el PDF
    let y = 534;
    lineas.forEach(linea => {
        pdf.text(linea, 37, y);
        y += 13;
    });


    // Firma y Huella
    pdf.setFontSize(12);
    pdf.text(arrFechaHoy[2], 297,618);
    pdf.text(arrFechaHoy[1], 443,618);
    pdf.text(arrFechaHoy[0], 539,618);
    pdf.text("ARMENIA", 69,629);
    const nombreCompleto = nombreF3 + " " + apellidoF3;
    pdf.text(nombreCompleto, 153, 687);
    pdf.text(numDocumentoF3, 153, 710);

    pdf.save('Formato_Auxilios_'+numDocumentoF3+'.pdf');

}

// Formato 4
// Formato Extracto
async function generarPDFf4(url, fechaCorte, nombreF4, numDocF4, mpioResidenciaF4, direccionF4, numCelularF4, concepto1, cuotaVencida, cuotaMes1, totalConcepto1, concepto2, cuotaMes2, totalConcepto2, concepto3, cuotaMes3, totalConcepto3, concepto4, cuotaMes4, totalConcepto4, concepto5, cuotaMes5, totalConcepto5, concepto6, cuotaMes6, totalConcepto6, arrayConveniosF4, pagoTotal, cuentaBeneficiariosF4, arrayBeneficiariosF4, arrayMascotasF4, saldo, mensaje) {
    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'legal');
    pdf.addImage(image, 'PNG', 0, 0, 613, 1010);
    pdf.setFont("helvetica", "normal");

    // renglon 0
    pdf.setFontSize(11);
    pdf.text(nombreF4, 18,138.5);
    pdf.text(formatearNumeroSinSimbolo(numDocF4), 244, 138.5);
    pdf.text(mpioResidenciaF4, 339,138.5);

    var arrFechaCorte = fechaCorte.split("-");
    const fecha = arrFechaCorte[2] + '/' + arrFechaCorte[1] + '/' + arrFechaCorte[0]
    pdf.text(fecha, 486,138.5);

    pdf.text(direccionF4, 91,157.8);
    pdf.text(numCelularF4, 486,157.8);

    // valores a pagar
    pdf.setFontSize(9);
    
    pdf.text(concepto1, 17,285);
    pdf.text(fecha, 166,285);

    if(saldo != 0){;
        pdf.text(formatearNumero(saldo), 236,285);
    }

    pdf.text(cuotaVencida, 329,285);
    pdf.text(formatearNumero(cuotaMes1), 385,285);
    // pdf.text('0', 452,285); interes de mora
    pdf.text(formatearNumero(totalConcepto1), 531,285);

    let fila = 305
    if(cuotaMes2 > 0){
        pdf.text(concepto2, 17,fila);
        pdf.text(fecha, 166,fila);
        // pdf.text('saldo', 248,fila);
        pdf.text(cuotaVencida, 329,fila);
        pdf.text(formatearNumero(cuotaMes2), 385,fila);
        // pdf.text('interes mora', 452,fila);
        pdf.text(formatearNumero(totalConcepto2), 531,fila);
        fila = fila + 20
    }
    if(cuotaMes3 > 0){
        pdf.text(concepto3, 17,fila);
        pdf.text(fecha, 166,fila);
        // pdf.text('saldo', 248,fila);
        pdf.text(cuotaVencida, 329,fila);
        pdf.text(formatearNumero(cuotaMes3), 385,fila);
        // pdf.text('interes mora', 452,fila);
        pdf.text(formatearNumero(totalConcepto3), 531,fila);
        fila = fila + 20
    }
    if(cuotaMes4 > 0){
        pdf.text(concepto4, 17,fila);
        pdf.text(fecha, 166,fila);
        // pdf.text('saldo', 248,fila);
        pdf.text(cuotaVencida, 329,fila);
        pdf.text(formatearNumero(cuotaMes4), 385,fila);
        // pdf.text('interes mora', 452,fila);
        pdf.text(formatearNumero(totalConcepto4), 531,fila);
        fila = fila + 20
    }
    if(cuotaMes5 > 0){
        pdf.text(concepto5, 17,fila);
        pdf.text(fecha, 166,fila);
        // pdf.text('saldo', 248,fila);
        pdf.text(cuotaVencida, 329,fila);
        pdf.text(formatearNumero(cuotaMes5), 385,fila);
        // pdf.text('interes mora', 452,fila);
        pdf.text(formatearNumero(totalConcepto5), 531,fila);
        fila = fila + 20
    }
    if(cuotaMes6 > 0){
        pdf.text(concepto6, 17,fila);
        pdf.text(fecha, 166,fila);
        // pdf.text('saldo', 248,fila);
        pdf.text(cuotaVencida, 329,fila);
        pdf.text(formatearNumero(cuotaMes6), 385,fila);
        // pdf.text('interes mora', 452,fila);
        pdf.text(formatearNumero(totalConcepto6), 531,fila);
        fila = fila + 20
    }
    // Listas Convenios del asociado
    for (let i=0; i < arrayConveniosF4.length; i++){
        const convenio = arrayConveniosF4[i];
        pdf.text("CONVENIO -" + " " + convenio.concepto, 17,fila);
        pdf.text(fecha, 166,fila);
        pdf.text(convenio.cantidadMeses.toString(), 329,fila);
        pdf.text(formatearNumero(convenio.valorMes), 385,fila);
        pdf.text(formatearNumero(convenio.total), 531,fila);
        fila = fila + 20
    }
    // if(cuotaMes7 > 0){
    //     pdf.text(concepto7, 17,fila);
    //     pdf.text(fecha, 166,fila);
    //     // pdf.text('saldo', 248,fila);
    //     pdf.text(cuotaVencida, 329,fila);
    //     pdf.text(formatearNumero(cuotaMes7), 385,fila);
    //     // pdf.text('interes mora', 452,fila);
    //     pdf.text(formatearNumero(totalConcepto7), 531,fila);
    //     fila = fila + 20
    // }
    
    // valor total a pagar
    pdf.setTextColor(255,255,255)
    pdf.setFont(undefined, "bold");
    pdf.setFontSize(12)

    pdf.text(formatearNumero(pagoTotal), 523,526.7);

    // observaciones
    pdf.setTextColor(0,0,0);
    pdf.setFont(undefined, "normal");
    // pdf.setFontSize(10)
    // pdf.text(mensaje, 30,460);

    pdf.setFontSize(8)
    let filaB = 621.3;
    let num_filas = 0
    let columna_1 = 17;
    let columna_2 = 181;
    let columna_3 = 255;

    // se lista beneficiarios
    for(let i = 0;i < arrayBeneficiariosF4.length; i++){
        let nombre = arrayBeneficiariosF4[i][0];

        if (nombre.length > 28) {
            nombre = nombre.substring(0, 25) + "..."; 
        }
        pdf.text(nombre, columna_1,filaB);

        if(arrayBeneficiariosF4[i][2] != 'None'){
            // pdf.text(arrayBeneficiariosF4[i][2], 332,filaB);  NOMBRE DEL PAIS
            pdf.text("SI", columna_2,filaB);
            pdf.text("NO", columna_3,filaB);
        }else{
            pdf.text("NO", columna_2,filaB);
            pdf.text("NO", columna_3,filaB);
        }
        // pdf.text(arrayBeneficiariosF4[i][1], 515,filaB); PARENTESCO
        filaB = filaB + 17;
        num_filas += 1;
        if (num_filas == 8){
            columna_1 = 301;
            columna_2 = 472;
            columna_3 = 549;
            filaB = 621.3;
        }
    }

    // se lista mascotas
    for(let i = 0;i < arrayMascotasF4.length; i++){
        pdf.text(arrayMascotasF4[i][0], columna_1,filaB);
        pdf.text("NO", columna_2,filaB);
        pdf.text("SI", columna_3,filaB);
        filaB += 17;
        num_filas += 1;
        if (num_filas == 8){
            columna_1 = 301;
            columna_2 = 472;
            columna_3 = 549;
            filaB = 621.3;
        }
    }

    // pago pse
    // pdf.textWithLink('                ', 430, 875, {url:"https://bit.ly/3XBQdEE"});
    // sede google maps
    pdf.textWithLink('                  ', 283, 941, {url:"https://maps.app.goo.gl/VbPt5H2EJ6nTxU6Q6"});
    // WhatsApp
    pdf.textWithLink('                  ', 131, 941, {url:"https://api.whatsapp.com/send/?phone=573135600507&text=Hola%2C+me+gustar%C3%ADa+obtener+m%C3%A1s+informaci%C3%B3n.&type=phone_number&app_absent=0"});
    // contacto
    pdf.textWithLink('                  ', 201, 941, {url:"mailto:contacto@coohobienestar.org"});
    // icono instagram
    pdf.textWithLink('                  ', 443, 941, {url:"https://www.instagram.com/coohobienestar/"});
    // icono facebook
    pdf.textWithLink('                  ', 364, 941, {url:"https://www.facebook.com/ccoohobienestar/"});

    pdf.save('Formato_Extracto_'+numDocF4+'.pdf');

}

// Formato 5
// Formato Extracto TODOS
async function generarPDFf5(url, arrayExtracto, mes) {
    
    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'legal');
    pdf.addImage(image, 'PNG', 0, 0, 613, 1010);

    for(let i = 0; i < arrayExtracto.length ; i++){
        
        // renglon 0
        pdf.setFontSize(9);
        pdf.text(arrayExtracto[i][0], 29,151);
        pdf.text(formatearNumeroSinSimbolo(arrayExtracto[i][1]), 257,151);
        pdf.text(arrayExtracto[i][3], 335,151);

        var arrFechaCorte = arrayExtracto[i][2].split("-");
        pdf.text(arrFechaCorte[2]+'/', 471,151);
        pdf.text(arrFechaCorte[1]+'/', 486,151);
        pdf.text(arrFechaCorte[0], 502,151);

        pdf.text(arrayExtracto[i][5], 105,172);
        pdf.text(arrayExtracto[i][4], 437,172);

        // valores a pagar
        pdf.setFontSize(9);
        
        // inicia posicion 8
        // concepto
        pdf.text(arrayExtracto[i][8], 30,285);
        // fecha
        pdf.text(arrFechaCorte[2]+'/', 177,285);
        pdf.text(arrFechaCorte[1]+'/', 190,285);
        pdf.text(arrFechaCorte[0], 204,285);
        // validacion saldo
        if(arrayExtracto[i][9] != 0){
            pdf.text(formatearNumero(arrayExtracto[i][9]), 252,285);
        }
        //cuota vencida 
        pdf.text(arrayExtracto[i][10], 324,285);
        // cuota Mes
        pdf.text(formatearNumero(arrayExtracto[i][11]), 382,285);
        // pdf.text('0', 452,285); interes de mora
        pdf.text(formatearNumero(arrayExtracto[i][12]), 520,285);

        let fila = 305
        // inicia posicion 13
        if(arrayExtracto[i][14] > 0){
            pdf.text(arrayExtracto[i][13], 30,fila);
            pdf.text(arrFechaCorte[2]+'/', 177,fila);
            pdf.text(arrFechaCorte[1]+'/', 190,fila);
            pdf.text(arrFechaCorte[0], 204,fila);
            // pdf.text('saldo', 248,fila);
            pdf.text(arrayExtracto[i][10], 324,fila);
            pdf.text(formatearNumero(arrayExtracto[i][14]), 382,fila);
            // pdf.text('interes mora', 452,fila);
            pdf.text(formatearNumero(arrayExtracto[i][15]), 520,fila);
            fila = fila + 20
        }
        // inicia posicion 16
        if(arrayExtracto[i][17] > 0){
            pdf.text(arrayExtracto[i][16], 30,fila);
            pdf.text(arrFechaCorte[2]+'/', 177,fila);
            pdf.text(arrFechaCorte[1]+'/', 190,fila);
            pdf.text(arrFechaCorte[0], 204,fila);
            // pdf.text('saldo', 248,fila);
            pdf.text(arrayExtracto[i][10], 324,fila);
            pdf.text(formatearNumero(arrayExtracto[i][17]), 382,fila);
            // pdf.text('interes mora', 452,fila);
            pdf.text(formatearNumero(arrayExtracto[i][18]), 520,fila);
            fila = fila + 20
        }
        // inicia posicion 19
        if(arrayExtracto[i][20] > 0){
            pdf.text(arrayExtracto[i][19], 30,fila);
            pdf.text(arrFechaCorte[2]+'/', 177,fila);
            pdf.text(arrFechaCorte[1]+'/', 190,fila);
            pdf.text(arrFechaCorte[0], 204,fila);
            // pdf.text('saldo', 248,fila);
            pdf.text(arrayExtracto[i][10], 324,fila);
            pdf.text(formatearNumero(arrayExtracto[i][20]), 382,fila);
            // pdf.text('interes mora', 452,fila);
            pdf.text(formatearNumero(arrayExtracto[i][21]), 520,fila);
            fila = fila + 20
        }
        // inicia posicion 22
        if(arrayExtracto[i][23] > 0){
            pdf.text(arrayExtracto[i][22], 30,fila);
            pdf.text(arrFechaCorte[2]+'/', 177,fila);
            pdf.text(arrFechaCorte[1]+'/', 190,fila);
            pdf.text(arrFechaCorte[0], 204,fila);
            // pdf.text('saldo', 248,fila);
            pdf.text(arrayExtracto[i][10], 324,fila);
            pdf.text(formatearNumero(arrayExtracto[i][23]), 382,fila);
            // pdf.text('interes mora', 452,fila);
            pdf.text(formatearNumero(arrayExtracto[i][24]), 520,fila);
            fila = fila + 20
        }
        // inicia posicion 25
        if(arrayExtracto[i][26] > 0){
            pdf.text(arrayExtracto[i][25], 30,fila);
            pdf.text(arrFechaCorte[2]+'/', 177,fila);
            pdf.text(arrFechaCorte[1]+'/', 190,fila);
            pdf.text(arrFechaCorte[0], 204,fila);
            // pdf.text('saldo', 248,fila);
            pdf.text(arrayExtracto[i][10], 324,fila);
            pdf.text(formatearNumero(arrayExtracto[i][26]), 382,fila);
            // pdf.text('interes mora', 452,fila);
            pdf.text(formatearNumero(arrayExtracto[i][27]), 520,fila);
            fila = fila + 20
        }

        // inicia posicion 28
        if(arrayExtracto[i][29] > 0){
            pdf.text(arrayExtracto[i][28], 30,fila);
            pdf.text(arrFechaCorte[2]+'/', 177,fila);
            pdf.text(arrFechaCorte[1]+'/', 190,fila);
            pdf.text(arrFechaCorte[0], 204,fila);
            // pdf.text('saldo', 248,fila);
            pdf.text(arrayExtracto[i][10], 324,fila);
            pdf.text(formatearNumero(arrayExtracto[i][29]), 382,fila);
            // pdf.text('interes mora', 452,fila);
            pdf.text(formatearNumero(arrayExtracto[i][30]), 520,fila);
            fila = fila + 20
        }
    

        // valor total a pagar
        pdf.setTextColor(255,255,255)
        pdf.setFont(undefined, "bold");
        pdf.setFontSize(12)
        // inicia posicion 31
        pdf.text(formatearNumero(arrayExtracto[i][31]), 523,439);
        // observaciones
        pdf.setTextColor(0,0,0);
        pdf.setFont(undefined, "normal");

        pdf.setFontSize(10)
        pdf.text(arrayExtracto[i][32], 30,460);

        pdf.setFontSize(8)
        let filaB = 567;
        // se lista beneficiarios, inicia posicion 6
        for(let j = 0;j < arrayExtracto[i][6].length; j++){
            pdf.text(arrayExtracto[i][6][j][0], 30,filaB);
            if(arrayExtracto[i][6][j][2] != 'None'){
                pdf.text(arrayExtracto[i][6][j][2], 332,filaB);
            }
            pdf.text(arrayExtracto[i][6][j][1], 515,filaB);
            filaB = filaB + 13;
            
        }

        // var perro = new Image()
        // perro.src = '/static/img/icons/huella.png';
        // perro.onload = () => {

        // se lista mascotas, inicia posicion 7
        for(let j = 0; j < arrayExtracto[i][7].length; j++){
            pdf.text(arrayExtracto[i][7][j][0], 30,filaB);
            pdf.text(arrayExtracto[i][7][j][1], 450,filaB);
            pdf.text('MASCOTA', 515,filaB);
            filaB += 13;
        }

        // pago pse
        pdf.textWithLink('                ', 430, 875, {url:"https://bit.ly/3XBQdEE"});
        // sede google maps
        pdf.textWithLink('                                    ', 38, 927, {url:"https://goo.gl/maps/Jzk8Jkupy8KKgzgk6"});
        // WhatsApp
        pdf.textWithLink('                           ', 169, 927, {url:"https://api.whatsapp.com/send/?phone=573135600507&text=Hola%2C+me+gustar%C3%ADa+obtener+m%C3%A1s+informaci%C3%B3n.&type=phone_number&app_absent=0"});
        // contacto
        pdf.textWithLink('                                                  ', 274, 927, {url:"mailto:contacto@coohobienestar.org"});
        // icono instagram
        pdf.textWithLink('           ', 480, 927, {url:"https://www.instagram.com/coohobienestar/"});
        // icono facebook
        pdf.textWithLink('           ', 527, 927, {url:"https://www.facebook.com/ccoohobienestar/"});
        
        if(i+1 < arrayExtracto.length){
            pdf.addPage();
            const image2 = await loadImage('/static/img/Formato_ExtractoPago_page_0001.jpg');
            pdf.addImage(image2, 'PNG', 0, 0, 613, 1010);
        }


    }
    pdf.save('Extractos_'+mes+'.pdf');    

    
}

async function generarTxt(arrayExtracto2) {
    // Contenido del archivo
    const texto = arrayExtracto2.join('\n');

    // Crear un Blob con el contenido
    const blob = new Blob([texto], { type: "text/plain" });

    // Crear un enlace temporal para la descarga
    const enlace = document.createElement("a");
    enlace.href = URL.createObjectURL(blob);
    enlace.download = "archivo.txt"; // Nombre del archivo

    // Simular un clic para descargar el archivo
    enlace.click();

    // Limpiar el URL Object creado
    URL.revokeObjectURL(enlace.href);
    
}

// Formato Solicitud de Crédito
async function generarPDFfCredito(url, valor, cuotas, nombre_F5, apellido_F5, tipoDocumento_F5, numDocumento_F5, fechaExpedicion_F5, mpioDoc_F5, nacionalidad_F5, fechaNacimiento_F5, genero_F5, estadoCivil_F5, email_F5, numCelular_F5, dtoNacimiento_F5, mpioNacimiento_F5, tipoVivienda_F5, estrato_F5, direccion_F5, barrio_F5, deptoResidencia_F5, mpioResidencia_F5, usuario_F5, fechaHoy_F5, numResidencia_F5, envioInfoCorreo_F5, envioInfoMensaje_F5, envioInfoWhatsapp_F5, profesion_F5, nombreEmpresa_F5, cargo_F5, fechaInicio_F5, fechaTerminacion_F5, nomRepresenLegal_F5, numDocRL_F5, mpioTrabajo_F5, dptoTrabajo_F5, telefono_F5, admRP_F5, pep_F5, activEcono_F5, ciiu_F5, banco_F5, numCuenta_F5, tipoCuenta_F5, direccionTrabajo_F5, nivelEducativo_F5, autorizaciondcto_F5, empresa_F5, lineaCredito_F5, medioPago_F5, formaDesembolso_F5, existCodeudor) {

    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'legal');
    pdf.addImage(image, 'PNG', 0, 0, 613, 1010);

    pdf.setFontSize(8);
    // fecha encabezado
    var arrFechaHoy = fechaHoy_F5.split("-")
    pdf.text(arrFechaHoy[2], 236,136);
    pdf.text(arrFechaHoy[1], 249,136);
    pdf.text(arrFechaHoy[0], 265,136);

    pdf.setFontSize(10);
    // Condiciones Financieras
    if (lineaCredito_F5 == 'SOLUCION INMEDIATA'){
        pdf.text('X', 199,279);
    }else if (lineaCredito_F5 == 'ANTICIPO NOMINA'){
        pdf.text('X', 101,279);
    }else if (lineaCredito_F5 == 'CREDILIBRE'){
        pdf.text('X', 282,279);
    }else if (lineaCredito_F5 == 'CREDICONTIGO'){
        pdf.text('X', 355,279);
    }
    
    pdf.text(formatearNumero(valor), 384,281);
    pdf.text(cuotas, 534,281);

    // Medio de Pago
    if (medioPago_F5 == 'PAGO DIRECTO'){
        pdf.text('X', 207,312);
    }else {
        pdf.text('X', 264,312);
    }
    // Coudeudor
    if (existCodeudor == 'True'){
        pdf.text('X', 304,312);
    } else {
        pdf.text('X', 329,312);
    }
    // Forma de Desembolso
    if (formaDesembolso_F5 == 'TRANSFERENCIA ELECTRONICA'){
        pdf.text('X', 395,312);
    }else if (formaDesembolso_F5 == 'CHEQUE'){
        pdf.text('X', 481,312);
    }else if (formaDesembolso_F5 == 'CUENTA AHORROS'){
        pdf.text('X', 548,312);
    }

    // Datos del Asociado
    // Fila 1
    pdf.text(nombre_F5, 20,377);
    pdf.text(apellido_F5, 321,377);

    // Fila 2
    if(tipoDocumento_F5 == 'CEDULA'){
        pdf.text('X', 41,426);
    }else if(tipoDocumento_F5 == 'CEDULA EXTRANJERA'){
        pdf.text('X', 82,426);
    }else {
        pdf.text('X', 104,426);
    }
    pdf.text(numDocumento_F5, 134,426);
    var arrFechaExp = fechaExpedicion_F5.split("-");
    pdf.text(arrFechaExp[2], 327,426);
    pdf.text(arrFechaExp[1], 355,426);
    pdf.text(arrFechaExp[0], 390,426);
    pdf.text(mpioDoc_F5, 435,426);

    // Fila 3
    pdf.text(nacionalidad_F5, 20,474);
    var arrFechaNac = fechaNacimiento_F5.split("-")
    pdf.text(arrFechaNac[2], 149,474);
    pdf.text(arrFechaNac[1], 188,474);
    pdf.text(arrFechaNac[0], 222,474);
    pdf.text(dtoNacimiento_F5, 278,474);
    pdf.text(mpioNacimiento_F5, 385,474);
    if (genero_F5 == 'FEMENINO'){
        pdf.text('X', 504,474);
    }else{
        pdf.text('X', 558,474);
    }
    
    // Fila 4
    if (estadoCivil_F5 == 'SOLTERO(A)'){
        pdf.text('X', 27,505);
    }else if (estadoCivil_F5 == 'CASADO(A)'){
        pdf.text('X', 68,505);
    }else if (estadoCivil_F5 == 'UNION LIBRE'){
        pdf.text('X', 114,505);
    }else if (estadoCivil_F5 == 'SEPARADO(A)'){
        pdf.text('X', 153,505);
    }else if (estadoCivil_F5 == 'DIVORCIADO(A)'){
        pdf.text('X', 209,505);
    }else{
        pdf.text('X', 253,505);
    }

    if (tipoVivienda_F5 == 'PROPIA'){
        pdf.text('X', 293,505);
    }else if (tipoVivienda_F5 == 'FAMILIAR'){
        pdf.text('X', 327,505);
    }else if (tipoVivienda_F5 == 'ARRENDADA'){
        pdf.text('X', 357,505);
    }else {
        pdf.text('X', 397,505);
    }

    // Fila 5
    if (estrato_F5 == '1'){
        pdf.text('X', 20,538);
    }else if (estrato_F5 == '2'){
        pdf.text('X', 41,538);
    }else if (estrato_F5 == '3'){
        pdf.text('X', 41,538);
    }else if (estrato_F5 == '4'){
        pdf.text('X', 62,538);
    }else if (estrato_F5 == '5'){
        pdf.text('X', 85,538);
    }else{
        pdf.text('X', 107,538);
    }

    // Casillas jefe de hogar
    // pdf.text('X', 129,538);
    // pdf.text(direccion_F5, 322,539);

    // Fila 6
    pdf.text(barrio_F5, 20,573);
    pdf.text(mpioResidencia_F5, 190, 573);
    pdf.text(deptoResidencia_F5, 325, 573);
    pdf.text(numCelular_F5, 465, 573);

    // Fila 7
    pdf.text(numResidencia_F5, 20,605);
    pdf.text(numCelular_F5, 127, 605);
    pdf.text(email_F5, 281, 605);

    // Fila 8
    if (envioInfoCorreo_F5 == 'True') pdf.text('X',106,635);
    if (envioInfoMensaje_F5 == 'True') pdf.text('X',229,635);
    if (envioInfoWhatsapp_F5 == 'True') pdf.text('X',330,635);

    // Fila 9
    if (nivelEducativo_F5 == 'PRIMARIA'){
        pdf.text('X', 31,669);
    }else if (nivelEducativo_F5 == 'SECUNDARIA'){
        pdf.text('X', 73,669);
    }else if (nivelEducativo_F5 == 'TECNICO'){
        pdf.text('X', 117,669);
    }else if (nivelEducativo_F5 == 'TECNOLOGICO'){
        pdf.text('X', 174,669);
    }else if (nivelEducativo_F5 == 'PREGRADO'){
        pdf.text('X', 238,669);
    }else if (nivelEducativo_F5 == 'ESPECIALIZACION'){
        pdf.text('X', 304,669);
    }else if (nivelEducativo_F5 == 'MAESTRIA'){
        pdf.text('X', 359,669);
    }else{
        pdf.text('X', 402,669);
    }

    // Fila 10
    pdf.text(profesion_F5, 20,703);
    // Campos de opciones de ocupacion
    // pdf.text('X', 345,703);
    // pdf.text('X', 401,703);
    // pdf.text('X', 454,703);
    // pdf.text('X', 507,703);
    // pdf.text('X', 561,703);

    // Informacion Laboral
    // Fila 1
    if (nombreEmpresa_F5 != 'None') pdf.text(nombreEmpresa_F5, 20,764);
    if (cargo_F5 != 'None') pdf.text(cargo_F5, 322,764);

    // Fila 2
    if (fechaInicio_F5 != ''){
        var arrFechaInicio = fechaInicio_F5.split("-");
        pdf.text(arrFechaInicio[2], 20,801);
        pdf.text(arrFechaInicio[1], 37,801);
        pdf.text(arrFechaInicio[0], 66,801);
    }
    if (fechaTerminacion_F5 != ''){
        var arrFechaTerminacion = fechaTerminacion_F5.split("-");
        pdf.text(arrFechaTerminacion[2], 104,801);
        pdf.text(arrFechaTerminacion[1], 126,801);
        pdf.text(arrFechaTerminacion[0], 155,801);
    }
    if (nomRepresenLegal_F5 != 'None') pdf.text(nomRepresenLegal_F5, 188,801);
    if (numDocRL_F5 != 'None') pdf.text(numDocRL_F5, 411,801);

    // Fila 3
    if (direccionTrabajo_F5 != 'None') pdf.text(direccionTrabajo_F5, 386,837);

    // Fila 4
    if (mpioTrabajo_F5 != 'None') pdf.text(mpioTrabajo_F5, 20,870);
    if (dptoTrabajo_F5 != 'None') pdf.text(dptoTrabajo_F5, 147,870);
    if (telefono_F5 != 'None') pdf.text(telefono_F5, 280,870);

    // Fila 5
    if (admRP_F5 == 'SI'){
        pdf.text('X', 39,905);
    }else{
        pdf.text('X', 103,905);
    }
    if (pep_F5 == 'SI'){
        pdf.text('X', 191,905);
    }else{
        pdf.text('X', 277,905);
    }
    if (activEcono_F5 != 'None'){
        pdf.text(activEcono_F5, 323,905);
    }
    if (ciiu_F5 != 'None'){
        pdf.text(ciiu_F5, 543,905)
    }

    // Fila 6
    if (banco_F5 != 'None') pdf.text(banco_F5, 20,939);
    if (numCuenta_F5 != 'None') pdf.text(numCuenta_F5, 324,939);
    pdf.text(tipoCuenta_F5, 463,939);

    /////////////////////////////////////////////////////////////////////////////////////////
    // Se añade Pagina 2 al documento
    pdf.addPage();
    const image2 = await loadImage('/static/img/Solicitud_Credito_page_0002.jpg');
    pdf.addImage(image2, 'PNG', 0, 0, 613, 1010);

    // Espacio de Autorizacion de descuento de nomina
    let nombreCompleto = nombre_F5 + " " + apellido_F5
    pdf.text(nombreCompleto, 45,761);
    pdf.text(mpioResidencia_F5 +" - "+deptoResidencia_F5, 17,773);
    pdf.text(numDocumento_F5, 430,773);
    pdf.text(mpioDoc_F5, 17,783);

    /////////////////////////////////////////////////////////////////////////////////////////
    // Se añade Pagina 3 al documento
    pdf.addPage();
    const image3 = await loadImage('/static/img/Solicitud_Credito_page_0003.jpg');
    pdf.addImage(image3, 'PNG', 0, 0, 613, 1010);

    // Espacio de Firma y huella
    pdf.text(arrFechaHoy[2], 224,286);
    pdf.text(arrFechaHoy[1], 374,286);
    pdf.text(arrFechaHoy[0], 491,286);
    pdf.text("ARMENIA", 20,296);

    pdf.save('Formato_Solicitud_Credito_'+numDocumento_F5+'.pdf');
    
    // se cierra el onload del image
}

async function descargarPagare(url, numDoc, datos, fechaHoy_F5) {
    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'legal');
    pdf.addImage(image, 'PNG', 0, 0, 613, 1010);


    var arrFechaHoy = fechaHoy_F5.split("-")
    

    let nomCompleto = datos.nombre + " " + datos.apellido
    let nomCompletoCod = datos.nombreCodeudor + " " + datos.apellidoCodeudor
    
    pdf.setFontSize(8);
    pdf.text(nomCompleto, 66, 258);
    pdf.text(nomCompletoCod, 66, 280);

    pdf.setFontSize(10);
    pdf.text(datos.tipoDocumento, 209, 258);
    pdf.text(datos.numDocumento, 275, 258);
    pdf.text(datos.mpioDoc, 369, 258);
    
    pdf.text(datos.tipoDocumentoCodeudor, 209, 280);
    pdf.text(datos.numDocumentoCodeudor, 275, 280);
    pdf.text(datos.mpioCodeudor, 369, 280);


    /////////////////////////////////////////////////////////////////////////////////////////
    // Se añade Pagina 2 al documento
    pdf.addPage();
    const image2 = await loadImage('/static/img/Pagare_page_0002.jpg');
    pdf.addImage(image2, 'PNG', 0, 0, 613, 1010);

    pdf.text("ARMENIA", 73, 768);
    pdf.text(convertirDias(arrFechaHoy[2]), 250, 768);
    pdf.text(arrFechaHoy[2], 455,768);
    pdf.text(convertirMes(arrFechaHoy[1]), 73,784);
    pdf.text(arrFechaHoy[0], 265,784);

    //Datos Deudor
    pdf.setFontSize(9);
    pdf.text(nomCompleto, 109, 852);
    pdf.text(datos.numDocumento, 93, 866);
    pdf.text(datos.mpioDoc, 171, 866);
    pdf.text(datos.celular, 110, 882);
    pdf.text(datos.direccion, 116, 898);
    pdf.text(datos.email, 98, 914);

    //Datos Codeudor
    pdf.text(nomCompletoCod, 368, 852);
    pdf.text(datos.numDocumentoCodeudor, 354, 866);
    pdf.text(datos.mpioCodeudor, 431, 866);
    pdf.text(datos.celularCodeudor, 369, 882);
    pdf.text(datos.direccionCodeudor, 381, 898);
    pdf.text(datos.emailCodeudor, 363, 914);



    /////////////////////////////////////////////////////////////////////////////////////////
    // Se añade Pagina 3 al documento
    pdf.addPage();
    const image3 = await loadImage('/static/img/Pagare_page_0003.jpg');
    pdf.addImage(image3, 'PNG', 0, 0, 613, 1010);

    pdf.text("ARMENIA", 73, 730);
    pdf.text(convertirDias(arrFechaHoy[2]), 250, 730);
    pdf.text(arrFechaHoy[2], 455,730);
    pdf.text(convertirMes(arrFechaHoy[1]), 73,746);
    pdf.text(arrFechaHoy[0], 265,746);

    //Datos Deudor
    pdf.setFontSize(9);
    pdf.text(nomCompleto, 109, 841);
    pdf.text(datos.numDocumento, 93, 856);
    pdf.text(datos.mpioDoc, 171, 856);
    pdf.text(datos.celular, 110, 872);
    pdf.text(datos.direccion, 116, 888);
    pdf.text(datos.email, 98, 904);

    //Datos Codeudor
    pdf.text(nomCompletoCod, 368, 841);
    pdf.text(datos.numDocumentoCodeudor, 354, 856);
    pdf.text(datos.mpioCodeudor, 431, 856);
    pdf.text(datos.celularCodeudor, 369, 872);
    pdf.text(datos.direccionCodeudor, 381, 888);
    pdf.text(datos.emailCodeudor, 363, 904);


    pdf.save('Pagare_'+numDoc+'.pdf');
    
    // se cierra el onload del image
}

async function descargarTablaAmortizacion(url, numDoc, fechaSolicitud, valor, cuotas, tasa, datos) {
    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'legal');
    pdf.addImage(image, 'PNG', 0, 0, 613, 1010);

    // Convertimos a numeros los valores de valor y cuotas
    let valorNumerica = parseFloat(valor);
    let cuotasNumerica = parseFloat(cuotas);
    // Remplazamos comas por puntos
    let tasaString = tasa.replace(',', '.');
    let tasaNumerica = parseFloat(tasaString);

    //Encabezados
    pdf.setFontSize(10);
    pdf.text('ARMENIA',111,130);

    var arrFechaHoy = fechaSolicitud.split("-")
    pdf.text('   /    /',325,130);
    pdf.text(arrFechaHoy[2], 321,130);
    pdf.text(arrFechaHoy[1], 336,130);
    pdf.text(arrFechaHoy[0], 351,130);

    pdf.setFontSize(12);
    pdf.text(datos.numCredito, 480,130);

    pdf.setFontSize(10);
    let nombreCompleto = datos.nombre + " " + datos.apellido
    let nombreCodeudor = datos.nombreCodeudor + " " + datos.apellidoCodeudor

    // Titular
    pdf.text(nombreCompleto, 53,256);
    pdf.text(datos.tipoDocumento, 268,256);
    pdf.text(datos.numDocumento, 361,256);
    pdf.text(datos.mpioDoc, 448,256);
    
    // Codeudor
    pdf.text(nombreCodeudor, 53,269);
    pdf.text(datos.tipoDocumentoCodeudor, 268,269);
    pdf.text(datos.numDocumentoCodeudor, 361,269);
    pdf.text(datos.mpioCodeudor, 448,269);

    // Renglon 1
    pdf.text(sumarMeses(fechaSolicitud, 0), 181,340);
    pdf.text(datos.lineaCredito, 345,340);
    // Renglon 2
    pdf.text(numeroALetras(valorNumerica), 60,355);
    pdf.text(formatearNumero(valor), 321,355);
    // Renglon 3
    let tasaPorcentaje = (tasaNumerica * 100).toFixed(1);
    pdf.text(tasaPorcentaje+'%', 341,384);
    // Renglon 4
    pdf.text(cuotas, 56,400);
    pdf.text(sumarMeses(fechaSolicitud, 1), 346,400)
    // Renglon 5
    pdf.text(sumarMeses(fechaSolicitud, cuotasNumerica), 111,415);
    pdf.text(formatearNumero(datos.valorCuota), 390,415);
    // Renglon 6
    pdf.text(datos.amortizacion, 88,430);
    pdf.text(formatearNumero(datos.totalCredito), 369,430);
    // Renglon 7
    pdf.text(datos.medioPago, 58,446);

    // Constancia
    console.log(arrFechaHoy[1]);
    pdf.text(arrFechaHoy[2], 95, 493);
    pdf.text(convertirMes(arrFechaHoy[1]), 275, 493);
    pdf.text(arrFechaHoy[0], 432, 493); 
    pdf.text('ARMENIA', 61, 506);
    
    // Firmas
    pdf.text(nombreCompleto, 159, 584);
    pdf.text(numDoc, 159, 598);
    pdf.text(datos.mpioDoc, 159, 611);

    pdf.text(nombreCodeudor, 159, 689);
    pdf.text(datos.numDocumentoCodeudor, 159, 702);
    pdf.text(datos.mpioCodeudor, 159, 715);

    /////////////////////////////////////////////////////////////////////////////////////////
    // Se añade Pagina 2 al documento
    pdf.addPage();
    const image3 = await loadImage('/static/img/Otorgamiento_Credito_page_0002.jpg');
    pdf.addImage(image3, 'PNG', 0, 0, 613, 1010);

    //Encabezados
    pdf.text('ARMENIA', 119, 134);
    pdf.text('   /    /',325,134);
    pdf.text(arrFechaHoy[2], 321,134);
    pdf.text(arrFechaHoy[1], 336,134);
    pdf.text(arrFechaHoy[0], 351,134);

    pdf.setFontSize(12);
    pdf.text(datos.numCredito, 480,134);
    pdf.setFontSize(10);

    // Deudores
    pdf.text(nombreCompleto, 182, 181);
    pdf.text(numDoc, 473, 181);
    pdf.text(nombreCodeudor, 182, 206);
    pdf.text(datos.numDocumentoCodeudor, 473, 206);

    // Informacion Credito
    pdf.text(sumarMeses(fechaSolicitud, 0), 231, 252);
    pdf.text(datos.lineaCredito, 231, 267);
    pdf.text(datos.amortizacion, 231, 283);
    pdf.text(formatearNumero(valor), 231, 299);
    pdf.text(cuotas, 231, 314);
    pdf.text(tasaPorcentaje+'%', 231, 329);
    pdf.text(sumarMeses(fechaSolicitud, cuotasNumerica), 231, 344);
    
    // Tabla Amortizacion

    let cuotaFija;
    if (tasaNumerica === 0) {
        cuotaFija = Math.ceil(valorNumerica / cuotasNumerica);
    } else {
        cuotaFija = ((valorNumerica * tasaNumerica * Math.pow(1 + tasaNumerica, cuotasNumerica)) / 
                    (Math.pow(1 + tasaNumerica, cuotasNumerica) - 1)).toFixed(0);
    }
    const fechas = generarFechas(cuotasNumerica, fechaSolicitud);
    
    let saldoRestante = parseFloat(valorNumerica);

    let fila = 415;
    for (let i = 0; i <= cuotasNumerica; i++) {
        if (i === 0) {
            pdf.text(String(i), 81, fila);
            pdf.text(fechas[i], 101, fila);
            pdf.text(formatearMoneda(saldoRestante), 156, fila);
            pdf.text(formatearMoneda(0), 225, fila);
            pdf.text(formatearMoneda(0), 290, fila);
            pdf.text(formatearMoneda(0), 347, fila);
            pdf.text(formatearMoneda(0), 392, fila);
            pdf.text(formatearMoneda(cuotaFija), 430, fila);
            pdf.text(formatearMoneda(saldoRestante), 493, fila);
            fila = fila + 15.5;
        } else {
            const intereses = (saldoRestante * tasaNumerica).toFixed(0);
            const abonoCapital = (cuotaFija - intereses).toFixed(0);
            
            // Si es la última fila, forzamos saldoRestante a 0
            if (i === cuotasNumerica) {
                saldoRestante = 0;
            } else {
                saldoRestante = (saldoRestante - abonoCapital).toFixed(0);
            }

            pdf.text(String(i), 81, fila);
            pdf.text(fechas[i], 101, fila);
            pdf.text(formatearMoneda(parseFloat(saldoRestante) + parseFloat(abonoCapital)), 156, fila);
            pdf.text(formatearMoneda(abonoCapital), 225, fila);
            pdf.text(formatearMoneda(intereses), 290, fila);
            pdf.text(formatearMoneda(0), 347, fila);
            pdf.text(formatearMoneda(0), 392, fila);
            pdf.text(formatearMoneda(cuotaFija), 430, fila);
            pdf.text(formatearMoneda(saldoRestante), 493, fila);
            fila = fila + 15.5;
        }
    }

    // Firma
    pdf.text(nombreCompleto, 157, 687);
    pdf.text(numDoc, 157, 702);
    pdf.text(datos.mpioDoc, 157, 717);

    pdf.save('Otorgamiento_Credito_'+numDoc+'.pdf');
}

function generarFechas(cuotas, fechaSolicitud) {
    const fechas = [];
    // Convertir la fecha inicial en un objeto Date sin UTC
    const [year, month, day] = fechaSolicitud.split("-").map(Number);
    const fechaInicio = new Date(year, month - 1, day); // Crear fecha local

    // Generar las fechas con base en el número de cuotas
    for (let i = 0; i <= cuotas; i++) {
        const fecha = new Date(fechaInicio); // Crear una copia de la fecha inicial
        fecha.setMonth(fecha.getMonth() + i); // Sumar meses en zona local
        fechas.push(
            fecha.toLocaleDateString("es-ES", {
                year: "numeric",month: "2-digit",day: "2-digit",
            })
        );
    }
    return fechas;
}

function formatearMoneda(valor) {
    return "$" + parseFloat(valor)
        .toLocaleString("es-CO", {
            style: "decimal", // Usar estilo decimal
            minimumFractionDigits: 0, // Eliminar decimales
            maximumFractionDigits: 0  // Eliminar decimales
    });
}