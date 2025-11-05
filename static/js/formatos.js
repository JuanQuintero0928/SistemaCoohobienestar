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
// async function llamarPDF(numFormato, url) {
//     // Obtenemos la informacion del model Asociado, del template formatos.html por medio de su id  
//     switch(numFormato){
//         // Formato Actualizacion y registro de asociado
//         case 1:
//             let actualizacion = document.getElementById('id_actualizacion').value;
//             let fechaHoy = document.getElementById('id_fechaActual').value;
//             let tPersona = document.getElementById('id_tPersona').value;
//             let nombre = document.getElementById('id_nombre').value;
//             let apellido = document.getElementById('id_apellido').value;
//             let tipoDocumento = document.getElementById('id_tipoDocumento').value;
//             let numDocumento = document.getElementById('id_numDocumento').value;
//             let fechaExpedicion = document.getElementById('id_fechaExpedicion').value;
//             let mpioDoc = document.getElementById('id_mpioDoc').value;
//             let nacionalidad = document.getElementById('id_nacionalidad').value;
//             let genero = document.getElementById('id_genero').value;
//             let estadoCivil = document.getElementById('id_estadoCivil').value;
//             let email = document.getElementById('id_email').value;
//             let numResidencia = document.getElementById('id_numResidencia').value;
//             let numCelular = document.getElementById('id_numCelular').value;
//             let envioInfoCorreo = document.getElementById('id_envioInfoCorreo').value;
//             let envioInfoMensaje = document.getElementById('id_envioInfoMensaje').value;
//             let envioInfoWhatsapp = document.getElementById('id_envioInfoWhatsapp').value;
//             let nivelEducativo = document.getElementById('id_nivelEducativo').value;
//             let tituloPregrado = document.getElementById('id_tituloPregrado').value;
//             let tituloPosgrado = document.getElementById('id_tituloPosgrado').value;
//             let fechaNacimiento = document.getElementById('id_fechaNacimiento').value;
//             let dtoNacimiento = document.getElementById('id_dtoNacimiento').value;
//             let mpioNacimiento = document.getElementById('id_mpioNacimiento').value;
//             let tipoVivienda = document.getElementById('id_tipoVivienda').value;
//             let estrato = document.getElementById('id_estrato').value;
//             let direccion = document.getElementById('id_direccion').value;
//             let barrio = document.getElementById('id_barrio').value;
//             let deptoResidencia = document.getElementById('id_deptoResidencia').value;
//             let mpioResidencia = document.getElementById('id_mpioResidencia').value;
//             // Obtenemos la informacion del model Laboral, del template formatos.html por medio de su id
//             let ocupacion = document.getElementById('id_ocupacion').value;
//             let nombreEmpresa = document.getElementById('id_nombreEmpresa').value;
//             let cargo = document.getElementById('id_cargo').value;
//             let nomRepresenLegal = document.getElementById('id_nomRepresenLegal').value;
//             let numDocRL = document.getElementById('id_numDocRL').value;
//             let fechaInicio = document.getElementById('id_fechaInicio').value;
//             let fechaTerminacion = document.getElementById('id_fechaTerminacion').value;
//             let direccionLab = document.getElementById('id_direccionLab').value;
//             let mpioTrabajo = document.getElementById('id_mpioTrabajo').value;
//             let dptoTrabajo = document.getElementById('id_dptoTrabajo').value;
//             let telefono = document.getElementById('id_telefono').value;
//             let admRP = document.getElementById('id_admRP').value;
//             let pep = document.getElementById('id_pep').value;
//             let activEcono = document.getElementById('id_activEcono').value;
//             let ciiu = document.getElementById('id_ciiu').value;
//             let banco = document.getElementById('id_banco').value;
//             let numCuenta = document.getElementById('id_numCuenta').value;
//             let tipoCuenta = document.getElementById('id_tipoCuenta').value;
//             let nombreRF = document.getElementById('id_nombreRF').value;
//             let parentesco = document.getElementById('id_parentesco').value;
//             let numContacto = document.getElementById('id_numContacto').value;
//             let autorizaciondcto = document.getElementById('id_autorizaciondcto').value;
//             let empresa = document.getElementById('id_empresa').value;
//             // Obtenemos la informacion del model Financiera, del template formatos.html por medio de su id
//             let ingresosActPrin = document.getElementById('id_ingresosActPrin').value;
//             let otroIngreso1 = document.getElementById('id_otroIngreso1').value;
//             let otroIngreso2 = document.getElementById('id_otroIngreso2').value;
//             let egresos = document.getElementById('id_egresos').value;
//             let activos = document.getElementById('id_activos').value;
//             let pasivos = document.getElementById('id_pasivos').value;
//             let patrimonio = document.getElementById('id_patrimonio').value;
//             // Obtenemos informacion del usuario que realiza la operacion
//             let usuario = document.getElementById('usuario').value;
//             generarPDF(url, nombre, apellido, tipoDocumento, numDocumento, fechaExpedicion, mpioDoc, nacionalidad, fechaNacimiento, genero, estadoCivil, email, numResidencia, numCelular,envioInfoCorreo, envioInfoMensaje, envioInfoWhatsapp, nivelEducativo, tituloPregrado, tituloPosgrado, dtoNacimiento, mpioNacimiento, tipoVivienda, estrato, direccion, barrio, deptoResidencia, mpioResidencia, ocupacion, nombreEmpresa, cargo, nomRepresenLegal, numDocRL, fechaInicio, fechaTerminacion, direccionLab, mpioTrabajo, dptoTrabajo, telefono, admRP, pep, activEcono, ciiu, banco, numCuenta, tipoCuenta, actualizacion, tPersona, fechaHoy, nombreRF, parentesco, numContacto, autorizaciondcto, empresa, ingresosActPrin, otroIngreso1, otroIngreso2, egresos, activos, pasivos, patrimonio, usuario);
//         break
//         // Formato Actualizacion servicios exequiales
//         case 2:
//             let actualizacionF2 = document.getElementById('id_actualizacion').value;
//             let tPersonaF2 = document.getElementById('id_tPersona').value;
//             let fechaHoyF2 = document.getElementById('id_fechaActual').value;
//             let nombreF2 = document.getElementById('id_nombre').value;
//             let apellidoF2 = document.getElementById('id_apellido').value;
//             let tipoDocumentoF2 = document.getElementById('id_tipoDocumento').value;
//             let numDocumentoF2 = document.getElementById('id_numDocumento').value;
//             let emailF2 = document.getElementById('id_email').value;
//             let numCelularF2 = document.getElementById('id_numCelular').value;
//             let envioInfoCorreoF2 = document.getElementById('id_envioInfoCorreo').value;
//             let envioInfoMensajeF2 = document.getElementById('id_envioInfoMensaje').value;
//             let envioInfoWhatsappF2 = document.getElementById('id_envioInfoWhatsapp').value;
//             let fechaNacimientoF2 = document.getElementById('id_fechaNacimiento').value;
//             let direccionF2 = document.getElementById('id_direccion').value;
//             let barrioF2 = document.getElementById('id_barrio').value;
//             let mpioResidenciaF2 = document.getElementById('id_mpioResidencia').value;
//             let numContactoF2 = document.getElementById('id_numContacto').value;
//             // Obtenemos la informacion del model Beneficiarios, del template formatos.html por medio de su id
//             let cuentaBeneficiarios = document.getElementById('id_cuentaBeneficiario').value;
//             let arrayBeneficiarios = [];
//             for(let i = 1; i <= cuentaBeneficiarios ; i++){
//                 let nombre = (document.getElementById('id_nombreBenef_'+i).value);
//                 let apellido = (document.getElementById('id_apellidoBenef_'+i).value);
//                 let numDocu = (document.getElementById('id_numDocume_'+i).value);
//                 let parentesco = (document.getElementById('id_parentesco_'+i).value);
//                 let nac = (document.getElementById('id_NacBen_'+i).value);
//                 let repatriacion = (document.getElementById('id_paisRepatriacion_'+i).value);
//                 let ciudadRepatriacion = (document.getElementById('id_ciudadRepatriacion_'+i).value);
//                 arrayBeneficiarios.push([nombre, apellido, numDocu, parentesco, nac, repatriacion, ciudadRepatriacion]);
//             }
//             // Obtenemos la informacion del model Mascota, del template formatos.html por medio de su id
//             let cuentaMascota = document.getElementById('id_cuentaMascota').value;
//             let arrayMascotas = [];
//             if(cuentaMascota > 0){
//                 for(let i = 1; i <= cuentaMascota ; i++){
//                     let nombreMasc = (document.getElementById('id_nombreMasc_'+i).value);
//                     let tipoMasc = (document.getElementById('id_tipoMasc_'+i).value);
//                     let raza = (document.getElementById('id_raza_'+i).value);
//                     let nacMasc = (document.getElementById('id_nacMasc_'+i).value);
//                     let vacunas = (document.getElementById('id_vacunas_'+i).value);
//                     arrayMascotas.push([nombreMasc, tipoMasc, raza, nacMasc, vacunas]);
//                 }
//             }
//             generarPDFf2(url, actualizacionF2, tPersonaF2, fechaHoyF2, nombreF2, apellidoF2, tipoDocumentoF2, numDocumentoF2, emailF2, numCelularF2, direccionF2, barrioF2, mpioResidenciaF2, numContactoF2, cuentaBeneficiarios, arrayBeneficiarios, arrayMascotas, envioInfoCorreoF2, envioInfoMensajeF2, envioInfoWhatsappF2)
//         break
//         // Formato Solicitud auxilio
//         case 3:
//             let fechaHoyF3 = document.getElementById('id_fechaActual').value;
//             let nombreF3 = document.getElementById('id_nombre').value;
//             let apellidoF3 = document.getElementById('id_apellido').value;
//             let tipoDocumentoF3 = document.getElementById('id_tipoDocumento').value;
//             let numDocumentoF3 = document.getElementById('id_numDocumento').value;
//             let fechaExpedicionF3 = document.getElementById('id_fechaExpedicion').value;
//             let mpioDocF3 = document.getElementById('id_mpioDoc').value;
//             let emailF3 = document.getElementById('id_email').value;
//             let numCelularF3 = document.getElementById('id_numCelular').value;
//             let envioInfoCorreoF3 = document.getElementById('id_envioInfoCorreo').value;
//             let envioInfoMensajeF3 = document.getElementById('id_envioInfoMensaje').value;
//             let envioInfoWhatsappF3 = document.getElementById('id_envioInfoWhatsapp').value;
//             let direccionF3 = document.getElementById('id_direccion').value;
//             let barrioF3 = document.getElementById('id_barrio').value;
//             let mpioResidenciaF3 = document.getElementById('id_mpioResidencia').value;
//             let fechaNacimientoF3 = document.getElementById('id_fechaNacimiento').value;
//             // Obtenemos la informacion del model Laboral, del template formatos.html por medio de su id
//             let nombreEmpresaF3 = document.getElementById('id_nombreEmpresa').value;
//             let cargoF3 = document.getElementById('id_cargo').value;
//             let telefonoF3 = document.getElementById('id_telefono').value;
//             // Obtenemos la informacion del model Financiera, del template formatos.html por medio de su id
//             let ingresosActPrinF3 = document.getElementById('id_ingresosActPrin').value;
//             let bancoF3 = document.getElementById('id_banco').value;
//             let numCuentaF3 = document.getElementById('id_numCuenta').value;
//             // Obtenemos la informacion del model HistoricoAuxilio, del template formatos.html por medio de su id
//             let tipoAuxilio = document.getElementById('id_tipoAuxilio').value;
//             let nombre2 = document.getElementById('id_nombre2').value;
//             let numDoc2 = document.getElementById('id_numDoc2').value;
//             let parentescoF3 = document.getElementById('id_parentesco').value;
//             let nivelEducativoF3 = document.getElementById('id_nivelEducativo').value;
//             let anexoOne = document.getElementById('id_anexoOne').value;
//             let anexoTwo = document.getElementById('id_anexoTwo').value;
//             let anexoThree = document.getElementById('id_anexoThree').value;
//             let anexoFour = document.getElementById('id_anexoFour').value;
//             let anexoFive = document.getElementById('id_anexoFive').value;
//             let anexoSix = document.getElementById('id_anexoSix').value;
//             let anexoSeven = document.getElementById('id_anexoSeven').value;
//             let anexoEight = document.getElementById('id_anexoEight').value;
//             generarPDFf3(url, fechaHoyF3, nombreF3, apellidoF3, tipoDocumentoF3, numDocumentoF3, fechaExpedicionF3, mpioDocF3, emailF3, numCelularF3, direccionF3, barrioF3, mpioResidenciaF3, fechaNacimientoF3, nombreEmpresaF3, cargoF3, telefonoF3, ingresosActPrinF3, bancoF3, numCuentaF3, nombre2, numDoc2, parentescoF3, nivelEducativoF3, anexoOne, anexoTwo, anexoThree, anexoFour, anexoFive, anexoSix, anexoSeven, anexoEight, envioInfoCorreoF3, envioInfoMensajeF3, envioInfoWhatsappF3, tipoAuxilio)
//         break
//         // Formato Extracto
//         case 4:
//             let fechaCorte = document.getElementById('id_fechaCorte').value;
//             let nombreF4 = document.getElementById('id_nombre').value;
//             let numDocF4 = document.getElementById('id_numDoc').value;
//             let mpioResidenciaF4 = document.getElementById('id_mpioResidencia').value;
//             let direccionF4 = document.getElementById('id_direccion').value;
//             let numCelularF4 = document.getElementById('id_numCelular').value;
//             let concepto1 = document.getElementById('id_concepto1').value;
//             let saldo = document.getElementById('id_saldo').value;
//             let cuotaVencida = document.getElementById('id_cuotaVencida').value;
//             let cuotaMes1 = document.getElementById('id_cuotaMes').value;
//             let totalConcepto1 = document.getElementById('id_totalConcepto1').value;

//             let concepto2 = document.getElementById('id_concepto2').value;
//             let cuotaMes2 = document.getElementById('id_cuotaMes2').value;
//             let totalConcepto2 = document.getElementById('id_totalConcepto2').value;

//             let concepto3 = document.getElementById('id_concepto3').value;
//             let cuotaMes3 = document.getElementById('id_cuotaMes3').value;
//             let totalConcepto3 = document.getElementById('id_totalConcepto3').value;

//             let concepto4 = document.getElementById('id_concepto4').value;
//             let cuotaMes4 = document.getElementById('id_cuotaMes4').value;
//             let totalConcepto4 = document.getElementById('id_totalConcepto4').value;

//             let concepto5 = document.getElementById('id_concepto5').value;
//             let cuotaMes5 = document.getElementById('id_cuotaMes5').value;
//             let totalConcepto5 = document.getElementById('id_totalConcepto5').value;

//             let concepto6 = document.getElementById('id_concepto6').value;
//             let cuotaMes6 = document.getElementById('id_cuotaMes6').value;
//             let totalConcepto6 = document.getElementById('id_totalConcepto6').value;

//             // let concepto7 = document.getElementById('id_concepto7').value;
//             // let cuotaMes7 = document.getElementById('id_cuotaMes7').value;
//             // let totalConcepto7 = document.getElementById('id_totalConcepto7').value;
            
//             let arrayConveniosF4 = []
//             const convenios = document.querySelectorAll(".convenio");
//             convenios.forEach((c, index) => {
//                 const concepto = c.querySelector(".concepto").value;
//                 const cantidadMeses = c.querySelector(".cantidad_meses").value;
//                 const valorMes = c.querySelector(".cuota_mes").value;
//                 const total = c.querySelector(".valor_vencido_convenio").value;
//                 arrayConveniosF4.push({
//                     concepto: concepto,
//                     cantidadMeses: parseInt(cantidadMeses),
//                     valorMes: parseFloat(valorMes),
//                     total: parseFloat(total)
//                 });
//             });

//             let pagoTotal = document.getElementById('id_pagoTotal').value;
//             let mensaje = document.getElementById('id_mensaje').value;
//             // Obtenemos la informacion del model Beneficiarios, del template formatos.html por medio de su id
//             let cuentaBeneficiariosF4 = document.getElementById('id_cuentaBeneficiario').value;
//             let arrayBeneficiariosF4 = [];
//             for(let i = 1; i <= cuentaBeneficiariosF4 ; i++){
//                 let nombre = (document.getElementById('id_nombreBenef_'+i).value);
//                 let parentesco = (document.getElementById('id_parentesco_'+i).value);
//                 let repatriacion = (document.getElementById('id_paisRepatriacion_'+i).value);
//                 arrayBeneficiariosF4.push([nombre, parentesco, repatriacion]);
//             }
//             // Obtenemos la informacion del model Mascota, del template formatos.html por medio de su id
//             let cuentaMascotaF4 = document.getElementById('id_cuentaMascota').value;
//             let arrayMascotasF4 = [];
//             if(cuentaMascotaF4 > 0){
//                 for(let i = 1; i <= cuentaMascotaF4 ; i++){
//                     let nombreMasc = (document.getElementById('id_nombreMasc_'+i).value);
//                     arrayMascotasF4.push([nombreMasc]);
//                 }
//             }
//             let pdf = generarPDFf4(url, fechaCorte, nombreF4, numDocF4, mpioResidenciaF4, direccionF4, numCelularF4, concepto1, cuotaVencida, cuotaMes1, totalConcepto1, concepto2, cuotaMes2, totalConcepto2, concepto3, cuotaMes3, totalConcepto3, concepto4, cuotaMes4, totalConcepto4, concepto5, cuotaMes5, totalConcepto5, concepto6, cuotaMes6, totalConcepto6, arrayConveniosF4, pagoTotal, cuentaBeneficiariosF4, arrayBeneficiariosF4, arrayMascotasF4, saldo, mensaje)
//             return pdf;
//     }
// }

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

async function guardarFechaYGenerarPDF(asociadoId, urlImagen, tipoFormato) {
    const inputFecha = document.getElementById('id_fechaActualizacionDatos');
    const fecha = inputFecha.value;
    const btn = document.getElementById('btnDescargar');
    const btnText = document.getElementById('btnText');
    const btnSpinner = document.getElementById('btnSpinner');

    if (!fecha) {
        alert("Por favor selecciona una fecha antes de continuar.");
        return;
    }

    try {
        // Guardar la nueva fecha en el backend
        const response = await fetch(`/informacion/actualizarFechaActualizacion/${asociadoId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({ fechaActualizacionDatos: fecha })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error || "Error al guardar la fecha");
            return;
        }

        // Si se guarda correctamente, generar el PDF
        console.log("llega aca y llama funcion llamarPDF")
        await llamarPDF(1, urlImagen, asociadoId, tipoFormato);

    } catch (error) {
        console.error("Error:", error);
        alert("Ocurrió un error al guardar la fecha");
    }
}


// Obtener CSRF del cookie
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}


function mostrarSpinner(boton) {
    if (!boton) return;
    const btnText = boton.querySelector('.btnText');
    const btnSpinner = boton.querySelector('.btnSpinner');

    if (btnText && btnSpinner) {
        boton.disabled = true;
        btnText.textContent = "";
        btnSpinner.classList.remove('d-none');
    }
}

function ocultarSpinner(boton) {
    if (!boton) return;
    const btnText = boton.querySelector('.btnText');
    const btnSpinner = boton.querySelector('.btnSpinner');

    if (btnText && btnSpinner) {
        boton.disabled = false;
        btnText.textContent = "";
        btnSpinner.classList.add('d-none');
        btnText.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-filetype-pdf" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M14 4.5V14a2 2 0 0 1-2 2h-1v-1h1a1 1 0 0 0 1-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5zM1.6 11.85H0v3.999h.791v-1.342h.803q.43 0 .732-.173.305-.175.463-.474a1.4 1.4 0 0 0 .161-.677q0-.375-.158-.677a1.2 1.2 0 0 0-.46-.477q-.3-.18-.732-.179m.545 1.333a.8.8 0 0 1-.085.38.57.57 0 0 1-.238.241.8.8 0 0 1-.375.082H.788V12.48h.66q.327 0 .512.181.185.183.185.522m1.217-1.333v3.999h1.46q.602 0 .998-.237a1.45 1.45 0 0 0 .595-.689q.196-.45.196-1.084 0-.63-.196-1.075a1.43 1.43 0 0 0-.589-.68q-.396-.234-1.005-.234zm.791.645h.563q.371 0 .609.152a.9.9 0 0 1 .354.454q.118.302.118.753a2.3 2.3 0 0 1-.068.592 1.1 1.1 0 0 1-.196.422.8.8 0 0 1-.334.252 1.3 1.3 0 0 1-.483.082h-.563zm3.743 1.763v1.591h-.79V11.85h2.548v.653H7.896v1.117h1.606v.638z"/>
            </svg>`;
    }
}


// Funcion para obtener la informacion del formato registro asociado
async function cargarDatosFormatoRegistro(asociadoId, tipoFormato) {
    const response = await fetch(`/api/obtener_datos_formato_registro/${asociadoId}/${tipoFormato}/`);
    const datos = await response.json();
    return datos;
}


// Funcion para obtener la informacion del formato de solicitud servicio exequial
async function cargarDatosFormatoServiciosExequiales(asociadoId, tipoFormato) {
    const response = await fetch(`/api/obtener_datos_servicios_exequiales/${asociadoId}/${tipoFormato}/`);
    const datos = await response.json();
    return datos;
}


// Funcion para obtener la informacion del formato de solicitud de auxilio economico
async function cargarDatosFormatoAuxilioEconomico(asociadoId, tipoFormato, auxilioId) {
    const response = await fetch(`/api/obtener_datos_auxilio_economico/${asociadoId}/${tipoFormato}/${auxilioId}/`);
    const datos = await response.json();
    return datos;
}


// Funcion global de los formatos
async function llamarPDF(formato, url, asociadoId, tipoFormato, opciones = {}, boton = null) {
    // try {

        if ([1, 2, 3].includes(formato)){
            mostrarSpinner(boton);
        }

        // Formato Registro y actualizacion de datos asociados
        if (formato == 1) {
            const datos = await cargarDatosFormatoRegistro(asociadoId, tipoFormato);
            await generarPDFRegistro(url, datos);
        } 
        // Formato Actualizacion servicios exequiales
        else if (formato == 2) {
            const datos = await cargarDatosFormatoServiciosExequiales(asociadoId, tipoFormato);
            await generarPDFServiciosExequiales(url, datos);
        }
        // Formato Solicitud Auxilio Economico
        else if  (formato == 3) {
            const auxilioId = opciones.id_auxilio ?? null;
            const datos = await cargarDatosFormatoAuxilioEconomico(asociadoId, tipoFormato, auxilioId);
            await generarPDFAuxilioEconomico(url, datos);
        }
        // Formato Extracto Individual
        else if (formato == 4) {
            const extractoData = JSON.parse(document.getElementById("extracto-data").textContent);
            await generarPDFExtractoIndividual(url, extractoData);
        }
    // }
    //  catch (error) {
    //     console.log(error);
    //     alert("Ocurrió un problema al generar el formato. Recargue la página e intente nuevamente. Si el error persiste comunicarse con el administrador.")
    // } finally {
    //     if ([1, 2, 3].includes(formato)){
    //         ocultarSpinner(boton);
    //     }
    // }
}

// Formato 1
// Formato de registro y actualizacion
async function generarPDFRegistro(url, datos) {

    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'legal');
    pdf.addImage(image, 'PNG', 0, 0, 613, 1010);

    // Globales
    pdf.setFontSize(9);
    pdf.setFont("verdana", "normal");

    const coordenadas = {
        tipoPersona : {
            "PERSONA NATURAL": { x: 22.4, y: 140.5 },
            "PERSONA JURIDICA": { x: 223, y: 140.5 },
            "ACTUALIZACION": { x: 411.7, y: 140.5 }
        },
        tipoDocumento : {
            "REGISTRO CIVIL": { x: 19.7, y: 326.4 },
            "TARJETA IDENTIDAD" : { x: 40.4, y: 326.4 },
            "CEDULA" : { x: 62.4, y: 326.4 },
            "CEDULA EXTRANJERA" : { x: 82.4, y: 326.4 },
            "PASAPORTE" : { x: 105.1, y: 326.4 }
        },
        genero : {
            "FEMENINO": {x: 505.7, y: 372.9},
            "MASCULINO": {x: 560.4, y: 372.9},
        },
        estadoCivil : {
            "SOLTERO(A)": {x: 29, y: 400.9},
            "CASADO(A)": {x: 71.7, y: 400.9},
            "UNION LIBRE": {x: 115.7, y: 400.9},
            "SEPARADO(A)": {x: 159, y: 400.9},
            "DIVORCIADO(A)": {x: 209.7, y: 400.9},
            "VIUDO(A)": {x: 256, y: 400.9},
        },
        tipoVivienda : {
            "PROPIA": {x: 291.7, y: 400.9},
            "FAMILIAR": {x: 345, y: 400.9},
            "ARRENDADA": {x: 401.7, y: 400.9},
        },
        estrato : {
            1 : {x: 22.4, y: 429.5},
            2 : {x: 42.4, y: 429.5},
            3 : {x: 63.7, y: 429.5},
            4 : {x: 85.7, y: 429.5},
            5 : {x: 108.4, y: 429.5},
            6 : {x: 130.4, y: 429.5},
        },
        nivelEducativo : {
            "PRIMARIA": {x: 31.7, y: 549.5},
            "SECUNDARIA": {x: 71, y: 549.5},
            "TECNICO": {x: 117.7, y: 549.5},
            "TECNOLOGICO": {x: 174.4, y: 549.5},
            "PREGRADO": {x: 240.4, y: 549.5},
            "ESPECIALIZACION": {x: 304.4, y: 549.5},
            "MAESTRIA": {x: 361.7, y: 549.5},
            "DOCTORADO":{x: 400, y: 549.5},
        },
        ocupacion : {
            "ESTUDIANTE": {x: 40.4, y: 635.3}, 
            "EMPLEADO": {x: 93.7, y: 635.3},
            "PENSIONADO": {x: 147, y: 635.3},
            "INDEPENDIENTE": {x: 223.7, y: 635.3},
            "COMERCIANTE": {x: 305, y: 635.3},
            "HOGAR": {x: 361.7, y: 635.3},
            "CESANTE": {x: 402.4, y: 635.3},
        },
        tipoEmpresa : {
            "PUBLICA": {x: 33, y: 664},
            "PRIVADA": {x: 72.4, y: 664},
            "MIXTA": {x: 118, y: 664},
        },
        tipoContrato: {
            "INDEFINIDO": {x: 292.4, y:694.7},
            "TERMINO FIJO": {x: 346, y:694.7},
            "OBRA O LABOR": {x: 401, y:694.7},
            "PRESTACION SERVICIOS": {x: 469, y:694.7},
            "HONORARIOS": {x: 551, y:694.7},
        }
    }

    var nombreCompleto = datos.nombre + ' ' + datos.apellido;
    var arrFechaHoy = datos.fechaFormateada.split("/")
    
    // Tipo persona y actualizacion y radicado
    pdf.text(datos.fechaFormateada, 285, 119.8);
    pdf.text(datos.numeroRadicado, 470, 119);
    const coordTipoPersona = coordenadas.tipoPersona[datos.tPersona] || coordenadas.tipoPersona["OTRO"];
    writeBoldText(pdf, "X", coordTipoPersona.x, coordTipoPersona.y, 10);

    // Vinculo estatutario
    pdf.text(nombreCompleto, 38.4, 181.1);
    pdf.text(datos.numDocumento, 486, 181.1);
    pdf.text(datos.mpioDoc, 21.7, 191.2);
    pdf.text("9.5", 285, 228.8);

    // Datos personales
    // renglon 1
    pdf.text(datos.nombre, 21.7,298.4);
    pdf.text(datos.apellido, 325.7, 298.4);

    // renglon 2
    const coordTipoDocumento = coordenadas.tipoDocumento[datos.tipoDocumento];
    writeBoldText(pdf, "X", coordTipoDocumento.x, coordTipoDocumento.y, 10);
    pdf.text(datos.numDocumento, 177.7, 326.4);
    var arrFechaExp = datos.fechaExpedicion.split("-")
    pdf.text(arrFechaExp[2], 327, 326.4);
    pdf.text(arrFechaExp[1], 358, 326.4);
    pdf.text(arrFechaExp[0], 391, 326.4);
    pdf.text(datos.mpioDoc, 435.7, 326.4);

    // renglon 3
    pdf.text(datos.nacionalidad, 21.7, 372.9);
    var arrFechaNac = datos.fechaNacimiento.split("-")
    pdf.text(arrFechaNac[2], 159, 372.9);
    pdf.text(arrFechaNac[1], 195, 372.9);
    pdf.text(arrFechaNac[0], 239, 372.9);
    pdf.text(datos.dtoNacimiento, 277, 372.9);
    pdf.text(datos.mpioNacimiento, 384.5, 372.9);
    const coordGenero = coordenadas.genero[datos.genero]
    pdf.text("X", coordGenero.x, coordGenero.y);

    // renglon 4
    const coordEstadoCivil = coordenadas.estadoCivil[datos.estadoCivil]
    pdf.text("X", coordEstadoCivil.x, coordEstadoCivil.y);
    const coordTipoVivienda = coordenadas.tipoVivienda[datos.tipoVivienda]
    pdf.text("X", coordTipoVivienda.x, coordTipoVivienda.y);
    if (datos.zonaUbicacion === "RURAL") {
        pdf.text("X", 491, 401.5);
    } else {
        pdf.text("X", 568, 401.5);
    }

    // renglon 5
    const coordEstrato = coordenadas.estrato[datos.estrato]
    pdf.text("X", coordEstrato.x, coordEstrato.y);
    if (datos.tAsociado === "COOHOBIENESTAR"){
        pdf.text("X", 187.7, 428.9);
    }else {
        pdf.text("X", 253.7, 428.9);
    }
    pdf.text(String(datos.nPersonasCargo), 325.7, 430.8);
    pdf.text(String(datos.nHijos), 399, 430.8);
    if (datos.cabezaFamilia === "SI"){
        pdf.text("X", 475.7, 429.9);
    } else {
        pdf.text("X", 552, 429.9);
    }

    // renglon 6
    pdf.text(datos.direccion, 21.7, 460.8);
    pdf.text(datos.barrio, 278.4, 460.8);
    pdf.text(datos.mpioResidencia, 463, 460.8);

    // renglon 7
    pdf.text(datos.deptoResidencia, 21.7, 489.5);
    pdf.text(datos.email, 125.7, 489.5);
    pdf.text(datos.numResidencia, 385, 489.5);
    pdf.text(datos.numCelular, 492.4, 489.5);

    // renglon 8
    if (datos.envioInfoCorreo){
        pdf.text("X", 105.7, 518.1);
    }
    if (datos.envioInfoMensaje){
        pdf.text("X", 226.4, 518.1);
    }
    if (datos.envioInfoWhatsapp){
        pdf.text("X", 329, 518.1);
    }

    // renglon 9
    const coordNivelEducativo = coordenadas.nivelEducativo[datos.nivelEducativo];
    pdf.text("X", coordNivelEducativo.x, coordNivelEducativo.y);

    // renglon 10
    writeText(pdf, datos.tituloPregrado, 21.7, 580.6);
    writeText(pdf, datos.tituloPosgrado, 322, 580.6);

    // Informacion laboral
    // renglon 1
    if (datos.ocupacion === "OTRO"){
        writeText(pdf, datos.ocupacionEspecifica || "", 463, 635.2);
    }else if (datos.ocupacion && coordenadas.ocupacion[datos.ocupacion] ){
        const coordOcupacion = coordenadas.ocupacion[datos.ocupacion];
        pdf.text("X", coordOcupacion.x, coordOcupacion.y);
    }

    // renglon 2
    if (datos.tipoEmpresa === "OTRO"){
        writeText(pdf, datos.tipoEmpresaEspecifica || "", 180.4, 664.6);
    } else if(datos.tipoEmpresa && coordenadas.tipoEmpresa[datos.tipoEmpresa]){
        const coordTipoEmpresa = coordenadas.tipoEmpresa[datos.tipoEmpresa];
        pdf.text("X", coordTipoEmpresa.x, coordTipoEmpresa.y);
    }
    writeText(pdf, datos.nombreEmpresa, 324.4, 665.9);

    // renglon 3
    writeText(pdf, datos.cargo, 21.7, 696.6);
    if (datos.tipoContrato && coordenadas.tipoContrato[datos.tipoContrato]){
        const coordTipoContrato = coordenadas.tipoContrato[datos.tipoContrato];
        pdf.text("X", coordTipoContrato.x, coordTipoContrato.y);
    }

    // renglon 4
    if (datos.fechaInicio){
        var arrFechaInicio = datos.fechaInicio.split("-")
        pdf.text(arrFechaInicio[2], 19.7, 730.6);
        pdf.text(arrFechaInicio[1], 39, 730.6);
        pdf.text(arrFechaInicio[0], 69, 730.6);
    }
    if (datos.fechaTerminacion){
        var arrFechaTerminacion = datos.fechaTerminacion.split("-")
        pdf.text(arrFechaTerminacion[2], 104.4, 730.6);
        pdf.text(arrFechaTerminacion[1], 127, 730.6);
        pdf.text(arrFechaTerminacion[0], 157, 730.6);
    }
    writeText(pdf, datos.nomRepresenLegal, 189, 730.6);
    writeText(pdf, String(datos.numDocRL), 461, 730.6);

    // renglon 5
    writeText(pdf, datos.nomJefeInmediato, 21.7, 761.2);
    writeText(pdf, datos.telefonoJefeInmediato, 279.7, 761.2);
    writeText(pdf, datos.direccionLaboral, 385.2, 761.2);

    // renglon 6
    writeText(pdf, datos.municipioLaboral, 21.7, 790);
    writeText(pdf, datos.dptoLaboral, 149.7, 790);
    writeText(pdf, datos.telefonoLaboral, 291.7, 790);
    writeText(pdf, datos.correoLaboral, 387, 790);

    // renglon 7
    if (datos.admRP === "SI"){
        pdf.text("X", 53, 823.9);
    } else {
        pdf.text("X", 102.4, 823.9);
    }
    if (datos.pep === "SI"){
        pdf.text("X", 191.7, 823.9);
    } else {
        pdf.text("X", 260.4, 823.9);
    }
    writeText(pdf, datos.activEcono, 323, 823.9);
    writeText(pdf, datos.ciiu, 552, 823.9);

    // renglon 8
    if (datos.declaraRenta === "SI"){
        pdf.text("X", 53, 852);
    } else {
        pdf.text("X", 102.4, 852);
    }
    if (datos.responsableIVA === "SI"){
        pdf.text("X", 191.7, 852);
    } else {
        pdf.text("X", 260.4, 852);
    }
    writeText(pdf, datos.regimenTributario, 323, 854.6);

    // renglon 9
    writeText(pdf, datos.banco, 21.7, 883.9);
    writeText(pdf, datos.tipoCuenta, 343, 883.9);
    writeText(pdf, datos.numCuenta, 489, 883.9);

    // Referencia Familiar
    // renglon 1
    pdf.text(datos.nombreRF, 21.7, 940.6);
    pdf.text(datos.parentesco, 319, 940.6);
    pdf.text(datos.numContacto, 472.4, 940.6);

    ///////////////////////////////////////////////////////////////////////////////////////////
    // Se añade Pagina 2 al documento
    pdf.addPage();
    const image2 = await loadImage('/static/img/Registro_Asociados_2025_page_0002.jpg');
    pdf.addImage(image2, 'PNG', 0, 0, 613, 1010);

    // Informacion ingresos y egresos
    writeText(pdf, formatearMoneda(datos.ingrSalario), 193.7, 134.5);
    writeText(pdf, formatearMoneda(datos.ingrHorasExtras), 193.7, 149.8);
    writeText(pdf, formatearMoneda(datos.ingrPension), 193.7, 165.1);
    writeText(pdf, formatearMoneda(datos.ingrCompensacion), 193.7, 179.8);
    writeText(pdf, formatearMoneda(datos.ingrHonorarios), 193.7, 195.2);
    writeText(pdf, formatearMoneda(datos.ingrVentas), 193.7, 210.5);
    writeText(pdf, formatearMoneda(datos.ingrIntereses), 193.7, 225.7);
    writeText(pdf, formatearMoneda(datos.ingrGiros), 193.7, 239.8);
    writeText(pdf, formatearMoneda(datos.ingrArrendamientos), 193.7, 254.9);
    writeText(pdf, formatearMoneda(datos.ingrOtros), 193.7, 269.7);
    writeText(pdf, datos.ingrDescripcionOtros, 139, 284.4);

    writeText(pdf, formatearMoneda(datos.egrArrendamiento), 469, 134.5);
    writeText(pdf, formatearMoneda(datos.egrServiciosPublicos), 469, 149.8);
    writeText(pdf, formatearMoneda(datos.egrAportesSalud), 469, 165.1);
    writeText(pdf, formatearMoneda(datos.egrTransporte), 469, 179.8);
    writeText(pdf, formatearMoneda(datos.egrAlimentacion), 469, 195.2);
    writeText(pdf, formatearMoneda(datos.egrObligaciones), 469, 210.5);
    writeText(pdf, formatearMoneda(datos.egrTarjetas), 469, 225.7);
    writeText(pdf, formatearMoneda(datos.egrCostos), 469, 239.8);
    writeText(pdf, formatearMoneda(datos.egrEmbargos), 469, 254.9);
    writeText(pdf, formatearMoneda(datos.egrOtros), 469, 269.7);
    writeText(pdf, datos.egrDescripcionOtros, 399, 284.4);

    pdf.setFont("verdana", "bold");
    pdf.setTextColor(255, 255, 255);
    writeText(pdf, formatearMoneda(datos.total_ingresos), 195, 314.3);
    writeText(pdf, formatearMoneda(datos.total_egresos), 470.4, 314.3);

    pdf.setFont("verdana", "normal");
    pdf.setTextColor(0, 0, 0);
    writeText(pdf, formatearMoneda(datos.total_ingresos), 307.7, 331.2);
    writeText(pdf, formatearMoneda(datos.total_egresos), 307.7, 347);
    writeText(pdf, formatearMoneda(datos.total_patrimonio), 307.7, 363.6);

    // renglon 1
    writeText(pdf, nombreCompleto, 21.7, 408.9);
    writeText(pdf, datos.numDocumento, 239, 408.9);
    pdf.text(arrFechaHoy[0], 342, 408.9);
    pdf.text(arrFechaHoy[1], 399.4, 408.9);
    pdf.text(arrFechaHoy[2], 450, 408.9);
    if (datos.declaraRenta){
        pdf.text("X", 511.9, 405.9);
    }else {
        pdf.text("X", 564.9, 405.9);
    }

    // Operacion en moneda extranjera
    // renglon 1
    if (datos.operacionesMonedaExtranjera === "SI"){
        pdf.text("X", 78.4, 464.8);
        writeText(pdf, datos.operacionesMonedaCuales, 221, 464.8);

        // renglon 2
        writeText(pdf, datos.operacionesMonedaTipo, 21.7, 497.4);
        writeText(pdf, "$" + formatearMoneda(datos.operacionesMonedaMonto), 222.4, 497.4);
        writeText(pdf, datos.operacionesMoneda, 410.4, 497.4);
    } else {
        pdf.text("X", 179, 464.8);
    }

    // renglon 3
    if (datos.poseeCuentasMonedaExtranjera === "SI"){
        pdf.text("X", 78.4, 527.4);
        writeText(pdf, datos.poseeCuentasBanco, 221, 527.4);
        writeText(pdf, datos.poseeCuentasCuenta, 411, 527.4);
    
        // renglon 4
        writeText(pdf, datos.poseeCuentasMoneda, 21.7, 561.2);
        writeText(pdf, datos.poseeCuentasCiudad, 221, 561.2);
        writeText(pdf, datos.poseeCuentasPais, 411, 561.2);
    } else {
        pdf.text("X", 179, 527.4);
    }

    // Firma
    pdf.text(nombreCompleto, 150, 651.2);
    pdf.text(datos.numDocumento, 150, 677.2);

    // Autorizacion de descuento por nomina
    if (datos.autorizaciondcto){
        pdf.text(nombreCompleto, 42.4, 750.6);
        pdf.text(datos.numDocumento, 23.7, 760.5);
        pdf.text(datos.mpioDoc, 183, 760.5);
        pdf.text("9.8", 502, 806.5);
    }

    // /////////////////////////////////////////////////////////////////////////////////////////
    // Se añade Pagina 3 al documento
    pdf.addPage();
    const image3 = await loadImage('/static/img/Registro_Asociados_2025_page_0003.jpg');
    pdf.addImage(image3, 'PNG', 0, 0, 613, 1010);

    pdf.text(nombreCompleto, 150.4, 877.2);
    pdf.text(datos.numDocumento, 150.4, 903.2);

    pdf.save('Formato_Registro_'+datos.numDocumento+'.pdf');
}


// Formato 2
// Formato Servicios Exequiales
async function generarPDFServiciosExequiales(url, datos) {

    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'legal');
    pdf.addImage(image, 'PNG', 0, 0, 613, 1010);

    // Globales
    pdf.setFontSize(9);
    pdf.setFont("verdana", "normal");

    const coordenadas = {
        tipoPersona : {
            "PERSONA NATURAL": { x: 20, y: 130 },
            "PERSONA JURIDICA": { x: 218, y: 130 },
            "ACTUALIZACION": { x: 417, y: 130 }
        },
        tipoDocumento : {
            "REGISTRO CIVIL": { x: 20, y: 215 },
            "CEDULA" : { x: 40, y: 215 },
            "TARJETA IDENTIDAD" : { x: 63, y: 215 },
            "CEDULA EXTRANJERA" : { x: 83, y: 215 },
            "PASAPORTE" : { x: 105, y: 215 }
        }
    }

    var arrFechaHoy = datos.fechaFormateada.split("/")
    var nombreCompleto = datos.nombre + ' ' + datos.apellido;

    // Fecha, radicado y tipo persona
    pdf.text(datos.fechaFormateada, 276, 111);
    pdf.text(datos.numeroRadicado, 470, 109.5);
    const coordTipoPersona = coordenadas.tipoPersona[datos.tPersona];
    writeBoldText(pdf, "X", coordTipoPersona.x, coordTipoPersona.y, 10);
    
    // Datos personales
    // renglon 1
    pdf.text(datos.nombre, 19,184);
    pdf.text(datos.apellido, 322,184);

    // renglon 2
    const coordTipoDocumento = coordenadas.tipoDocumento[datos.tipoDocumento];
    writeBoldText(pdf, "X", coordTipoDocumento.x, coordTipoDocumento.y, 10);
    pdf.text(datos.numDocumento, 133,216);
    pdf.text(datos.direccion, 324,216);

    // renglon 3
    pdf.text(datos.barrio, 19,248);
    pdf.text(datos.mpioResidencia, 190,248);
    pdf.text(datos.numCelular, 323,248);
    pdf.text(datos.numContacto, 471,248);

    // renglon 4
    pdf.text(datos.email, 19,281);

    //  renglon 5
    if(datos.envioInfoCorreo){
        pdf.text("X", 105,313);
    }
    if(datos.envioInfoMensaje){
        pdf.text("X", 228,313);
    }
    if(datos.envioInfoWhatsapp){
        pdf.text("X", 329,313);
    }

    // variables de inicio de tabla beneficiarios
    pdf.setFontSize(8);
    let fila = 401;
    let filaR = 598;
    
    //  Informacion grupo vinculado a servicios funerarios
    datos.beneficiarios.forEach(b => {
        pdf.text("X", 51,fila);
        pdf.text(`${b.nombre} ${b.apellido}`, 125, fila);

        const tipoDoc = {
            "CEDULA": "CC",
            "REGISTRO CIVIL": "RC",
            "TARJETA IDENTIDAD": "TI",
            "CEDULA EXTRANJERA": "CE",
            "PASAPORTE": "PA"
        }[b.tipoDocumento] || "";

        pdf.text(tipoDoc, 315, fila);
        pdf.text(b.numDocumento, 367, fila);
        pdf.text(b.parentesco__nombre, 451, fila);
        const fecha = b.fechaNacimiento.split("-");
        pdf.text(fecha[2], 530, fila);
        pdf.text(fecha[1], 552, fila);
        pdf.text(fecha[0], 574, fila);

        // cuadro de repatriacion
        if(b.repatriacion){
            pdf.text("X", 51, filaR);
            pdf.text(`${b.nombre} ${b.apellido}`,125, filaR);
            pdf.text(b.numDocumento, 299, filaR);
            pdf.text(b.ciudadRepatriacion, 393, filaR);
            pdf.text(b.paisRepatriacion__nombre, 499, filaR);
            filaR += 15
        }
        fila += 15;
    })

     // Se diligencia Cuadro de Mascota
    let filaM = 705;
    datos.mascotas.forEach(m => {
        pdf.text("X", 51, filaM);
        pdf.text(m.nombre, 125, filaM);
        if (m.tipo === "GATO"){
            pdf.text("X", 283, filaM);
        }else {
            pdf.text("X", 305, filaM);
        }
        pdf.text(m.raza, 321, filaM);
        const fecha = m.fechaNacimiento.split("-");
        pdf.text(fecha[2], 447, filaM);
        pdf.text(fecha[1], 474, filaM);
        pdf.text(fecha[0], 500, filaM);
        if (m.vacunasCompletas){
            pdf.text("X", 544, filaM);
        }else {
            pdf.text("X", 580 ,filaM);
        }
        filaM += 15;
    })

    // Firma y Huella
    pdf.text(arrFechaHoy[0], 299,861);
    pdf.text(arrFechaHoy[1], 444,861);
    pdf.text(arrFechaHoy[2], 541,861);
    pdf.text("Armenia", 72,871);

    // // Firma
    pdf.text(nombreCompleto, 155 ,929);
    pdf.text(datos.numDocumento, 155 ,952);

    pdf.save('Formato_Servicios_Exequiales_'+datos.numDocumento+'.pdf');
}


// Formato 3
// Formato Auxilios
async function generarPDFAuxilioEconomico(url, datos) {
    
    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'legal');
    pdf.addImage(image, 'PNG', 0, 0, 613, 1010);

    // Globales
    pdf.setFontSize(9);
    pdf.setFont("verdana", "normal");

    const coordenadas = {
        tipoDocumento : {
            "REGISTRO CIVIL": { x: 19, y: 190 },
            "CEDULA" : { x: 41, y: 190 },
            "TARJETA IDENTIDAD" : { x: 63, y: 190 },
            "CEDULA EXTRANJERA" : { x: 83, y: 190 },
            "PASAPORTE" : { x: 105, y: 190 }
        },
        auxilioSolicitado : {
            "AUXILIO OPTICO": { x: 40, y: 420},
            "AUXILIO INCAPACIDAD MEDICA": { x: 329, y: 403},
            "KIT DE MATERNIDAD": { x: 329, y: 349},
            "AUXILIO EDUCATIVO-UNIVERDAD": { x: 40, y: 384},
            "AUXILIO EDUCATIVO-MAESTRIA": { x: 40, y: 403},
            "AUXILIO EDUCATIVO-TECNICO": { x: 40, y: 349},
            "CALAMIDAD DOMESTICA-DESASTRE": { x: 329, y: 367},
            "CALAMIDAD DOMESTICA-MEDICO": { x: 329, y: 384},
            "AUXILIO EDUCATIVO-TECNOLOGIA": { x: 40, y: 367},
        }
    }

    var nombreCompleto = datos.nombre + ' ' + datos.apellido;
    var arrFechaHoy = datos.fechaFormateada.split("/")
    
    // Fecha encabezado
    pdf.text(datos.fechaFormateada, 274,110);
    pdf.text(datos.numeroRadicado, 470, 108.7);
    
    // renglon 1
    pdf.text(datos.nombre, 17,162);
    pdf.text(datos.apellido, 323,162);

    // renglon 2
    const coordTipoDocumento = coordenadas.tipoDocumento[datos.tipoDocumento];
    writeBoldText(pdf, "X", coordTipoDocumento.x, coordTipoDocumento.y, 10);
    pdf.text(datos.numDocumento, 137,190);
    pdf.text(datos.direccion, 323,190);

    // renglon 3
    pdf.text(datos.barrio, 17,219);
    pdf.text(datos.mpioResidencia, 187,219);
    pdf.text(datos.numCelular, 323,219);
    pdf.text(datos.numContacto, 465,219);

    // renglon 4
    pdf.text(datos.email, 17,247);

    // renglon 5
    writeText(pdf, datos.auxilio.entidadBancaria, 17, 276);
    writeText(pdf, datos.auxilio.numCuenta, 325, 276);

    // renglon 6
    if(datos.envioInfoCorreo){
        pdf.text("X", 107, 305);
    }
    if(datos.envioInfoMensaje){
        pdf.text("X", 227, 305);
    }
    if(datos.envioInfoWhatsapp){
        pdf.text("X", 329.7, 305);
    }

    // Auxilio solicitado
    const coordAuxilio = coordenadas.auxilioSolicitado[datos.auxilio.tipoAuxilio__nombre];
    writeBoldText(pdf, "X", coordAuxilio.x, coordAuxilio.y, 10);

    // Campo - se solicita para
    if(datos.auxilio.nombre){
        writeText(pdf, datos.auxilio.nombre, 17, 479);
        writeText(pdf, datos.auxilio.numDoc, 325, 479);
        writeText(pdf, datos.auxilio.parentesco__nombre, 480, 479);
        writeText(pdf, datos.auxilio.nivelEducativo, 127, 494);
    }

    // Anexos
    // Maximo 92 caracteres
    const maxCaracteres = 92;
    const texto = datos.auxilio.anexos_concat || "";

    // Divide el texto en líneas de máximo 82 caracteres
    const lineas = [];
    for (let i = 0; i < texto.length; i += maxCaracteres) {
        lineas.push(texto.substring(i, i + maxCaracteres));
    }

    // Ahora escribes cada línea en el PDF
    let y = 532;
    lineas.forEach((linea) => {
        writeText(pdf, linea, 36.5, y);
        y += 13;
    });

    // // Firma y Huella
    pdf.text(arrFechaHoy[0], 305,618);
    pdf.text(arrFechaHoy[1], 449,618);
    pdf.text(arrFechaHoy[2], 539,618);
    pdf.text("ARMENIA", 69,629);
    pdf.text(nombreCompleto, 153, 687);
    pdf.text(datos.numDocumento, 153, 710);

    pdf.save('Formato_Auxilios_'+datos.numDocumento+'.pdf');

}


// Formato 4
// Formato Extracto Individual
async function generarPDFExtractoIndividual(url, extractoData) {
    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'legal');
    pdf.addImage(image, 'PNG', 0, 0, 613, 1010);

    console.log("extractoData:", extractoData);
    
    // Globales
    pdf.setFontSize(10);
    pdf.setFont("verdana", "normal");

    // Variables
    var fecha = extractoData.fechaCorte.split("-")
    var fechaFormateada = fecha[2] + '/' + fecha[1] + '/' + fecha[0]

    // renglon 1
    pdf.text(extractoData.nombre, 16,138.5);
    pdf.text(extractoData.numDocumento, 244,138.5);
    pdf.text(extractoData.mpioResidencia, 339, 138.5)
    pdf.text(fechaFormateada, 486, 138.5)

    // renglon 2
    pdf.text(extractoData.direccion, 91,157.8);
    pdf.text(extractoData.numCelular, 486,157.8);

    // valores a pagar
    pdf.text(extractoData.mes, 17, 285);
    pdf.text(fechaFormateada, 166, 285);
    writeText(pdf, extractoData.cuotaVencida, 329, 285);
    pdf.text(formatearNumero(extractoData.cuotaPeriodica), 385,285);
    pdf.text(formatearNumero(extractoData.valorVencido), 531,285);

    pdf.save('Formato_Auxilios_'+extractoData.numDocumento+'.pdf');
}

// Formato 4
// Formato Extracto
// async function generarPDFf4(url, fechaCorte, nombreF4, numDocF4, mpioResidenciaF4, direccionF4, numCelularF4, concepto1, cuotaVencida, cuotaMes1, totalConcepto1, concepto2, cuotaMes2, totalConcepto2, concepto3, cuotaMes3, totalConcepto3, concepto4, cuotaMes4, totalConcepto4, concepto5, cuotaMes5, totalConcepto5, concepto6, cuotaMes6, totalConcepto6, arrayConveniosF4, pagoTotal, cuentaBeneficiariosF4, arrayBeneficiariosF4, arrayMascotasF4, saldo, mensaje) {
//     const image = await loadImage(url);
//     const pdf = new jsPDF('p', 'pt', 'legal');
//     pdf.addImage(image, 'PNG', 0, 0, 613, 1010);
//     pdf.setFont("helvetica", "normal");

//     // renglon 0
//     pdf.setFontSize(11);

//     if (nombreF4.length > 32) {
//             nombreF4 = nombreF4.substring(0, 31) + "."; 
//         }
//     pdf.text(nombreF4, 16,138.5);

//     // pdf.text(nombreF4, 16,138.5);
//     pdf.text(formatearNumeroSinSimbolo(numDocF4), 244, 138.5);
//     pdf.text(mpioResidenciaF4, 339,138.5);

//     var arrFechaCorte = fechaCorte.split("-");
//     const fecha = arrFechaCorte[2] + '/' + arrFechaCorte[1] + '/' + arrFechaCorte[0]
//     pdf.text(fecha, 486,138.5);

//     pdf.text(direccionF4, 91,157.8);
//     pdf.text(numCelularF4, 486,157.8);

//     // valores a pagar
//     pdf.setFontSize(9);
    
//     pdf.text(concepto1, 17,285);
//     pdf.text(fecha, 166,285);

//     if(saldo != 0){;
//         pdf.text(formatearNumero(saldo), 236,285);
//     }

//     pdf.text(cuotaVencida, 329,285);
//     pdf.text(formatearNumero(cuotaMes1), 385,285);
//     // pdf.text('0', 452,285); interes de mora
//     pdf.text(formatearNumero(totalConcepto1), 531,285);

//     let fila = 305
//     if(cuotaMes2 > 0){
//         pdf.text(concepto2, 17,fila);
//         pdf.text(fecha, 166,fila);
//         // pdf.text('saldo', 248,fila);
//         pdf.text(cuotaVencida, 329,fila);
//         pdf.text(formatearNumero(cuotaMes2), 385,fila);
//         // pdf.text('interes mora', 452,fila);
//         pdf.text(formatearNumero(totalConcepto2), 531,fila);
//         fila = fila + 20
//     }
//     if(cuotaMes3 > 0){
//         pdf.text(concepto3, 17,fila);
//         pdf.text(fecha, 166,fila);
//         // pdf.text('saldo', 248,fila);
//         pdf.text(cuotaVencida, 329,fila);
//         pdf.text(formatearNumero(cuotaMes3), 385,fila);
//         // pdf.text('interes mora', 452,fila);
//         pdf.text(formatearNumero(totalConcepto3), 531,fila);
//         fila = fila + 20
//     }
//     if(cuotaMes4 > 0){
//         pdf.text(concepto4, 17,fila);
//         pdf.text(fecha, 166,fila);
//         // pdf.text('saldo', 248,fila);
//         pdf.text(cuotaVencida, 329,fila);
//         pdf.text(formatearNumero(cuotaMes4), 385,fila);
//         // pdf.text('interes mora', 452,fila);
//         pdf.text(formatearNumero(totalConcepto4), 531,fila);
//         fila = fila + 20
//     }
//     if(cuotaMes5 > 0){
//         pdf.text(concepto5, 17,fila);
//         pdf.text(fecha, 166,fila);
//         // pdf.text('saldo', 248,fila);
//         pdf.text(cuotaVencida, 329,fila);
//         pdf.text(formatearNumero(cuotaMes5), 385,fila);
//         // pdf.text('interes mora', 452,fila);
//         pdf.text(formatearNumero(totalConcepto5), 531,fila);
//         fila = fila + 20
//     }
//     if(cuotaMes6 > 0){
//         pdf.text(concepto6, 17,fila);
//         pdf.text(fecha, 166,fila);
//         // pdf.text('saldo', 248,fila);
//         pdf.text(cuotaVencida, 329,fila);
//         pdf.text(formatearNumero(cuotaMes6), 385,fila);
//         // pdf.text('interes mora', 452,fila);
//         pdf.text(formatearNumero(totalConcepto6), 531,fila);
//         fila = fila + 20
//     }
//     // Listas Convenios del asociado
//     for (let i=0; i < arrayConveniosF4.length; i++){
//         const convenio = arrayConveniosF4[i];
//         pdf.text("CONVENIO -" + " " + convenio.concepto, 17,fila);
//         pdf.text(fecha, 166,fila);
//         pdf.text(convenio.cantidadMeses.toString(), 329,fila);
//         pdf.text(formatearNumero(convenio.valorMes), 385,fila);
//         pdf.text(formatearNumero(convenio.total), 531,fila);
//         fila = fila + 20
//     }
//     // if(cuotaMes7 > 0){
//     //     pdf.text(concepto7, 17,fila);
//     //     pdf.text(fecha, 166,fila);
//     //     // pdf.text('saldo', 248,fila);
//     //     pdf.text(cuotaVencida, 329,fila);
//     //     pdf.text(formatearNumero(cuotaMes7), 385,fila);
//     //     // pdf.text('interes mora', 452,fila);
//     //     pdf.text(formatearNumero(totalConcepto7), 531,fila);
//     //     fila = fila + 20
//     // }
    
//     // valor total a pagar
//     pdf.setTextColor(255,255,255)
//     pdf.setFont(undefined, "bold");
//     pdf.setFontSize(12)

//     pdf.text(formatearNumero(pagoTotal), 523,526.7);

//     // observaciones
//     pdf.setTextColor(0,0,0);
//     pdf.setFont(undefined, "normal");
//     // pdf.setFontSize(10)
//     // pdf.text(mensaje, 30,460);

//     pdf.setFontSize(8)
//     let filaB = 621.3;
//     let num_filas = 0
//     let columna_1 = 17;
//     let columna_2 = 181;
//     let columna_3 = 255;

//     // se lista beneficiarios
//     for(let i = 0;i < arrayBeneficiariosF4.length; i++){
//         let nombre = arrayBeneficiariosF4[i][0];

//         if (nombre.length > 27) {
//             nombre = nombre.substring(0, 25) + "..."; 
//         }
//         pdf.text(nombre, columna_1,filaB);

//         if(arrayBeneficiariosF4[i][2] != 'None'){
//             // pdf.text(arrayBeneficiariosF4[i][2], 332,filaB);  NOMBRE DEL PAIS
//             pdf.text("SI", columna_2,filaB);
//             pdf.text("NO", columna_3,filaB);
//         }else{
//             pdf.text("NO", columna_2,filaB);
//             pdf.text("NO", columna_3,filaB);
//         }
//         // pdf.text(arrayBeneficiariosF4[i][1], 515,filaB); PARENTESCO
//         filaB = filaB + 17;
//         num_filas += 1;
//         if (num_filas == 8){
//             columna_1 = 301;
//             columna_2 = 472;
//             columna_3 = 549;
//             filaB = 621.3;
//         }
//     }

//     // se lista mascotas
//     for(let i = 0;i < arrayMascotasF4.length; i++){
//         pdf.text(arrayMascotasF4[i][0], columna_1,filaB);
//         pdf.text("NO", columna_2,filaB);
//         pdf.text("SI", columna_3,filaB);
//         filaB += 17;
//         num_filas += 1;
//         if (num_filas == 8){
//             columna_1 = 301;
//             columna_2 = 472;
//             columna_3 = 549;
//             filaB = 621.3;
//         }
//     }

//     // pago pse
//     // pdf.textWithLink('                ', 430, 875, {url:"https://bit.ly/3XBQdEE"});
//     // sede google maps
//     pdf.textWithLink('                  ', 283, 941, {url:"https://maps.app.goo.gl/VbPt5H2EJ6nTxU6Q6"});
//     // WhatsApp
//     pdf.textWithLink('                  ', 131, 941, {url:"https://api.whatsapp.com/send/?phone=573135600507&text=Hola%2C+me+gustar%C3%ADa+obtener+m%C3%A1s+informaci%C3%B3n.&type=phone_number&app_absent=0"});
//     // contacto
//     pdf.textWithLink('                  ', 201, 941, {url:"mailto:contacto@coohobienestar.org"});
//     // icono instagram
//     pdf.textWithLink('                  ', 443, 941, {url:"https://www.instagram.com/coohobienestar/"});
//     // icono facebook
//     pdf.textWithLink('                  ', 364, 941, {url:"https://www.facebook.com/ccoohobienestar/"});

//     pdf.save('Formato_Extracto_'+numDocF4+'.pdf');

// }

// Formato 5
// Formato Extracto TODOS
async function generarPDFf5(url, arrayExtracto, mes) {
    
    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'legal');
    pdf.addImage(image, 'PNG', 0, 0, 613, 1010);

    for(let i = 0; i < arrayExtracto.length ; i++){
        
        // renglon 0
        pdf.setFontSize(11);
        pdf.text(arrayExtracto[i][0], 18,138.5);
        pdf.text(formatearNumeroSinSimbolo(arrayExtracto[i][1]), 244,138.5);
        pdf.text(arrayExtracto[i][3], 339,138.5);

        var arrFechaCorte = arrayExtracto[i][2].split("-");
        const fecha = arrFechaCorte[2] + '/' + arrFechaCorte[1] + '/' + arrFechaCorte[0]
        pdf.text(fecha, 486,138.5);

        pdf.text(arrayExtracto[i][5], 91,157.8);
        pdf.text(arrayExtracto[i][4], 486,157.8);

        // valores a pagar
        pdf.setFontSize(9);
        
        // inicia posicion 8
        // concepto
        pdf.text(arrayExtracto[i][8], 17,285);
        pdf.text(fecha, 166,285);

        // validacion saldo
        if(arrayExtracto[i][9] != 0){
            pdf.text(formatearNumero(arrayExtracto[i][9]), 236,285);
        }
        //cuota vencida 
        pdf.text(arrayExtracto[i][10], 329,285);
        // cuota Mes
        pdf.text(formatearNumero(arrayExtracto[i][11]), 385,285);
        // pdf.text('0', 452,285); interes de mora
        pdf.text(formatearNumero(arrayExtracto[i][12]), 531,285);

        let fila = 305
        // inicia posicion 13
        if(arrayExtracto[i][14] > 0){
            pdf.text(arrayExtracto[i][13], 17,fila);
            pdf.text(fecha, 166,fila);
            // pdf.text('saldo', 248,fila);
            pdf.text(arrayExtracto[i][10], 329,fila);
            pdf.text(formatearNumero(arrayExtracto[i][14]), 385,fila);
            // pdf.text('interes mora', 452,fila);
            pdf.text(formatearNumero(arrayExtracto[i][15]), 531,fila);
            fila = fila + 20
        }
        // inicia posicion 16
        if(arrayExtracto[i][17] > 0){
            pdf.text(arrayExtracto[i][16], 17,fila);
            pdf.text(fecha, 166,fila);

            // pdf.text('saldo', 248,fila);
            pdf.text(arrayExtracto[i][10], 329,fila);
            pdf.text(formatearNumero(arrayExtracto[i][17]), 385,fila);
            // pdf.text('interes mora', 452,fila);
            pdf.text(formatearNumero(arrayExtracto[i][18]), 531,fila);
            fila = fila + 20
        }
        // inicia posicion 19
        if(arrayExtracto[i][20] > 0){
            pdf.text(arrayExtracto[i][19], 17,fila);
            pdf.text(fecha, 166,fila);

            // pdf.text('saldo', 248,fila);
            pdf.text(arrayExtracto[i][10], 329,fila);
            pdf.text(formatearNumero(arrayExtracto[i][20]), 385,fila);
            // pdf.text('interes mora', 452,fila);
            pdf.text(formatearNumero(arrayExtracto[i][21]), 531,fila);
            fila = fila + 20
        }
        // inicia posicion 22
        if(arrayExtracto[i][23] > 0){
            pdf.text(arrayExtracto[i][22], 17,fila);
            pdf.text(fecha, 166,fila);

            // pdf.text('saldo', 248,fila);
            pdf.text(arrayExtracto[i][10], 329,fila);
            pdf.text(formatearNumero(arrayExtracto[i][23]), 385,fila);
            // pdf.text('interes mora', 452,fila);
            pdf.text(formatearNumero(arrayExtracto[i][24]), 531,fila);
            fila = fila + 20
        }
        // inicia posicion 25
        if(arrayExtracto[i][26] > 0){
            pdf.text(arrayExtracto[i][25], 17,fila);
            pdf.text(fecha, 166,fila);

            // pdf.text('saldo', 248,fila);
            pdf.text(arrayExtracto[i][10], 329,fila);
            pdf.text(formatearNumero(arrayExtracto[i][26]), 385,fila);
            // pdf.text('interes mora', 452,fila);
            pdf.text(formatearNumero(arrayExtracto[i][27]), 531,fila);
            fila = fila + 20
        }

        // inicia posicion 28
        // if(arrayExtracto[i][29] > 0){
        //     pdf.text(arrayExtracto[i][28], 17,fila);
        //     pdf.text(fecha, 166,fila);

        //     // pdf.text('saldo', 248,fila);
        //     pdf.text(arrayExtracto[i][10], 329,fila);
        //     pdf.text(formatearNumero(arrayExtracto[i][29]), 385,fila);
        //     // pdf.text('interes mora', 452,fila);
        //     pdf.text(formatearNumero(arrayExtracto[i][30]), 531,fila);
        //     fila = fila + 20
        // }
        for (let j = 0; j < arrayExtracto[i][30].length; j++) {
            const convenio = arrayExtracto[i][30][j];
            pdf.text("CONVENIO -" + " " + convenio.concepto, 17, fila);
            pdf.text(fecha, 166, fila);
            pdf.text(convenio.cantidadMeses.toString(), 329, fila);
            pdf.text(formatearNumero(convenio.valorMes), 385, fila);
            pdf.text(formatearNumero(convenio.total), 531, fila);
            fila += 20;
        }

        // valor total a pagar
        pdf.setTextColor(255,255,255)
        pdf.setFont(undefined, "bold");
        pdf.setFontSize(12)
        // inicia posicion 31
        pdf.text(formatearNumero(arrayExtracto[i][28]), 523,526.7);

        // observaciones
        pdf.setTextColor(0,0,0);
        pdf.setFont(undefined, "normal");

        pdf.setFontSize(8)
        let filaB = 621.3;
        let num_filas = 0
        let columna_1 = 17;
        let columna_2 = 181;
        let columna_3 = 255;
        
        // se lista beneficiarios, inicia posicion 6
        for(let j = 0;j < arrayExtracto[i][6].length; j++){
            let nombre = arrayExtracto[i][6][j][0];

            if (nombre.length > 27) {
                nombre = nombre.substring(0, 25) + "..."; 
            }

            pdf.text(nombre, columna_1,filaB);

            if(arrayExtracto[i][6][j][2] != 'None'){
                pdf.text("SI", columna_2,filaB);
                pdf.text("NO", columna_3,filaB);
                // pdf.text(arrayExtracto[i][6][j][2], 332,filaB);
            } else {
                pdf.text("NO", columna_2,filaB);
                pdf.text("NO", columna_3,filaB);
            }

            filaB = filaB + 17;
            num_filas += 1;
            if (num_filas == 8){
                columna_1 = 301;
                columna_2 = 472;
                columna_3 = 549;
                filaB = 621.3;
            }            
        }

        // var perro = new Image()
        // perro.src = '/static/img/icons/huella.png';
        // perro.onload = () => {

        // se lista mascotas, inicia posicion 7
        for(let j = 0; j < arrayExtracto[i][7].length; j++){
            pdf.text(arrayExtracto[i][7][j][0], columna_1,filaB);
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
            // pdf.text(arrayExtracto[i][7][j][1], columna_2,filaB);
            // pdf.text('MASCOTA', 515,filaB);
            // filaB += 13;
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
        
        if(i+1 < arrayExtracto.length){
            pdf.addPage();
            const image2 = await loadImage('/static/img/Formato_ExtractoPago_2025_page_0001.jpg');
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
    if (valor == null || valor === "") return "";
    // return "$" + parseFloat(valor)
    return parseFloat(valor).toLocaleString("es-CO", {
            style: "decimal", // Usar estilo decimal
            minimumFractionDigits: 0, // Eliminar decimales
            maximumFractionDigits: 0  // Eliminar decimales
    });
}


// Funcion para escribir texto en el PDF con manejo de valores nulos
function writeText(pdf, value, x, y, options = {}) {
    pdf.text(String(value ?? ""), x, y, options);
}

// Función auxiliar para escribir texto en negrita con tamaño específico
function writeBoldText(pdf, text, x, y, size = 10) {
    pdf.setFont('verdana', 'normal');
    pdf.setFontSize(size);
    pdf.text(text, x, y);

    // Restaurar configuración anterior
    pdf.setFont('verdana', 'normal');
    pdf.setFontSize(9);
}
