// Funcion que cambia la edicion en el proceso de pago, VIEW CrearPagoAsociado
function editarCasillasPago(dato){
    switch(dato){
        case "editar1":
            document.getElementById('valorPago').disabled = false;
            document.getElementById('btn_editar').hidden = true;
            document.getElementById('btn_no_editar').hidden = false;
        break
        case "no_editar1":
            document.getElementById('valorPago').disabled = true;
            document.getElementById('btn_editar').hidden = false;
            document.getElementById('btn_no_editar').hidden = true;
        break
        case "editar2":
        document.getElementById('aportePago').disabled = false;
        document.getElementById('btn_editar2').hidden = true;
        document.getElementById('btn_no_editar2').hidden = false;
        break
        case "no_editar2":
            document.getElementById('aportePago').disabled = true;
            document.getElementById('btn_editar2').hidden = false;
            document.getElementById('btn_no_editar2').hidden = true;
        break
        case "editar3":
        document.getElementById('bSocialPago').disabled = false;
        document.getElementById('btn_editar3').hidden = true;
        document.getElementById('btn_no_editar3').hidden = false;
        break
        case "no_editar3":
            document.getElementById('bSocialPago').disabled = true;
            document.getElementById('btn_editar3').hidden = false;
            document.getElementById('btn_no_editar3').hidden = true;
        break
        case "editar4":
        document.getElementById('mascotaPago').disabled = false;
        document.getElementById('btn_editar4').hidden = true;
        document.getElementById('btn_no_editar4').hidden = false;
        break
        case "no_editar4":
            document.getElementById('mascotaPago').disabled = true;
            document.getElementById('btn_editar4').hidden = false;
            document.getElementById('btn_no_editar4').hidden = true;
        break
        case "editar5":
        document.getElementById('repatriacionPago').disabled = false;
        document.getElementById('btn_editar5').hidden = true;
        document.getElementById('btn_no_editar5').hidden = false;
        break
        case "no_editar5":
            document.getElementById('repatriacionPago').disabled = true;
            document.getElementById('btn_editar5').hidden = false;
            document.getElementById('btn_no_editar5').hidden = true;
        break
        case "editar6":
        document.getElementById('seguroVidaPago').disabled = false;
        document.getElementById('btn_editar6').hidden = true;
        document.getElementById('btn_no_editar6').hidden = false;
        break
        case "no_editar6":
            document.getElementById('seguroVidaPago').disabled = true;
            document.getElementById('btn_editar6').hidden = false;
            document.getElementById('btn_no_editar6').hidden = true;
        break
        case "editar7":
        document.getElementById('adicionalesPago').disabled = false;
        document.getElementById('btn_editar7').hidden = true;
        document.getElementById('btn_no_editar7').hidden = false;
        break
        case "no_editar7":
            document.getElementById('adicionalesPago').disabled = true;
            document.getElementById('btn_editar7').hidden = false;
            document.getElementById('btn_no_editar7').hidden = true;
        break
        case "editar8":
        document.getElementById('coohopAporte').disabled = false;
        document.getElementById('btn_editar8').hidden = true;
        document.getElementById('btn_no_editar8').hidden = false;
        break
        case "no_editar8":
            document.getElementById('coohopAporte').disabled = true;
            document.getElementById('btn_editar8').hidden = false;
            document.getElementById('btn_no_editar8').hidden = true;
        break
        case "editar9":
        document.getElementById('coohopBsocial').disabled = false;
        document.getElementById('btn_editar9').hidden = true;
        document.getElementById('btn_no_editar9').hidden = false;
        break
        case "no_editar9":
            document.getElementById('coohopBsocial').disabled = true;
            document.getElementById('btn_editar9').hidden = false;
            document.getElementById('btn_no_editar9').hidden = true;
        break
        case "editar10":
        document.getElementById('diferencia').disabled = false;
        document.getElementById('btn_editar10').hidden = true;
        document.getElementById('btn_no_editar10').hidden = false;
        break
        case "no_editar10":
            document.getElementById('diferencia').disabled = true;
            document.getElementById('btn_editar10').hidden = false;
            document.getElementById('btn_no_editar10').hidden = true;
        break
        case "habilitar":
            document.getElementById('valorPago').disabled = false;
            document.getElementById('aportePago').disabled = false;
            document.getElementById('bSocialPago').disabled = false;
            document.getElementById('mascotaPago').disabled = false;
            document.getElementById('repatriacionPago').disabled = false;
            document.getElementById('seguroVidaPago').disabled = false;
            document.getElementById('adicionalesPago').disabled = false;
            document.getElementById('coohopAporte').disabled = false;
            document.getElementById('coohopBsocial').disabled = false;
            document.getElementById('diferencia').disabled = false;   
        break
    }
}

// Funcion que cambia la edicion de actualizacion de la seccion personal, VIEW VerAscociado
function editarInputActualizacion(dato){
    switch(dato){
        case "editar":
            document.getElementById('btn-editar').hidden = true;
            document.getElementById('btn-noeditar').hidden = false;
            document.getElementById('id_tPersona').disabled = false;
            document.getElementById('id_tAsociado').disabled = false;
            document.getElementById('id_estadoAsociado').disabled = false;
            document.getElementById('id_fechaIngreso').disabled = false;
            document.getElementById('id_nombre').disabled = false;
            document.getElementById('id_apellido').disabled = false;
            document.getElementById('id_tipoDocumento').disabled = false;
            document.getElementById('id_numDocumento').disabled = false;
            document.getElementById('id_fechaExpedicion').disabled = false;
            document.getElementById('id_mpioDoc').disabled = false;
            document.getElementById('id_nacionalidad').disabled = false;
            document.getElementById('id_genero').disabled = false;
            document.getElementById('id_estadoCivil').disabled = false;
            document.getElementById('id_email').disabled = false;
            document.getElementById('id_numResidencia').disabled = false;
            document.getElementById('id_numCelular').disabled = false;
            document.getElementById('id_envioInfoCorreo').disabled = false;
            document.getElementById('id_envioInfoMensaje').disabled = false;
            document.getElementById('id_envioInfoWhatsapp').disabled = false;
            document.getElementById('id_nivelEducativo').disabled = false;
            document.getElementById('id_tituloPregrado').disabled = false;
            document.getElementById('id_tituloPosgrado').disabled = false;
            document.getElementById('id_fechaNacimiento').disabled = false;
            document.getElementById('id_dtoNacimiento').disabled = false;
            document.getElementById('id_mpioNacimiento').disabled = false;
            document.getElementById('id_tipoVivienda').disabled = false;
            document.getElementById('id_estrato').disabled = false;
            document.getElementById('id_direccion').disabled = false;
            document.getElementById('id_barrio').disabled = false;
            document.getElementById('id_deptoResidencia').disabled = false;
            document.getElementById('id_mpioResidencia').disabled = false;
            document.getElementById('id_nombreRF').disabled = false;
            document.getElementById('id_parentesco').disabled = false;
            document.getElementById('id_numContacto').disabled = false;
            document.getElementById('btn-guardar').hidden = false;
            document.getElementById('id_fechaRetiro').disabled = false;
        break
        case "no_editar":
            document.getElementById('btn-noeditar').hidden = true;
            document.getElementById('btn-editar').hidden = false;
            document.getElementById('id_tPersona').disabled = true;
            document.getElementById('id_tAsociado').disabled = true;
            document.getElementById('id_estadoAsociado').disabled = true;
            document.getElementById('id_fechaIngreso').disabled = true;
            document.getElementById('id_nombre').disabled = true;
            document.getElementById('id_apellido').disabled = true;
            document.getElementById('id_tipoDocumento').disabled = true;
            document.getElementById('id_numDocumento').disabled = true;
            document.getElementById('id_fechaExpedicion').disabled = true;
            document.getElementById('id_mpioDoc').disabled = true;
            document.getElementById('id_nacionalidad').disabled = true;
            document.getElementById('id_genero').disabled = true;
            document.getElementById('id_estadoCivil').disabled = true;
            document.getElementById('id_email').disabled = true;
            document.getElementById('id_numResidencia').disabled = true;
            document.getElementById('id_numCelular').disabled = true;
            document.getElementById('id_envioInfoCorreo').disabled = true;
            document.getElementById('id_envioInfoMensaje').disabled = true;
            document.getElementById('id_envioInfoWhatsapp').disabled = true;
            document.getElementById('id_nivelEducativo').disabled = true;
            document.getElementById('id_tituloPregrado').disabled = true;
            document.getElementById('id_tituloPosgrado').disabled = true;
            document.getElementById('id_fechaNacimiento').disabled = true;
            document.getElementById('id_dtoNacimiento').disabled = true;
            document.getElementById('id_mpioNacimiento').disabled = true;
            document.getElementById('id_tipoVivienda').disabled = true;
            document.getElementById('id_estrato').disabled = true;
            document.getElementById('id_direccion').disabled = true;
            document.getElementById('id_barrio').disabled = true;
            document.getElementById('id_deptoResidencia').disabled = true;
            document.getElementById('id_mpioResidencia').disabled = true;
            document.getElementById('id_nombreRF').disabled = true;
            document.getElementById('id_parentesco').disabled = true;
            document.getElementById('id_numContacto').disabled = true;
            document.getElementById('btn-guardar').hidden = true;
            document.getElementById('btn-fechaRetiro').hidden = true;
        break
    } 
}

// Funcion que cambia la edicion de actualizacion de la seccion laboral, VIEW VerAscociado
function editarInputActualizacion2(dato){
    switch(dato){
        case "editar":
            document.getElementById('btn-editar2').hidden = true;
            document.getElementById('btn-noeditar2').hidden = false;
            document.getElementById('id_ocupacion').disabled = false;
            document.getElementById('id_nombreEmpresa').disabled = false;
            document.getElementById('id_cargo').disabled = false;
            document.getElementById('id_nomRepresenLegal').disabled = false;
            document.getElementById('id_numDocRL').disabled = false;
            document.getElementById('id_fechaInicio').disabled = false;
            document.getElementById('id_fechaTerminacion').disabled = false;
            document.getElementById('id_direccion2').disabled = false;
            document.getElementById('id_mpioTrabajo').disabled = false;
            document.getElementById('id_dptoTrabajo').disabled = false;
            document.getElementById('id_telefono').disabled = false;
            document.getElementById('id_admRP').disabled = false;
            document.getElementById('id_pep').disabled = false;
            document.getElementById('id_activEcono').disabled = false;
            document.getElementById('id_ciiu').disabled = false;
            document.getElementById('id_banco').disabled = false;
            document.getElementById('id_numCuenta').disabled = false;
            document.getElementById('id_tipoCuenta').disabled = false;
            document.getElementById('id_ingresosActPrin').disabled = false;
            document.getElementById('id_otroIngreso1').disabled = false;
            document.getElementById('id_otroIngreso2').disabled = false;
            document.getElementById('id_egresos').disabled = false;
            document.getElementById('id_activos').disabled = false;
            document.getElementById('id_pasivos').disabled = false;
            document.getElementById('id_patrimonio').disabled = false;
            document.getElementById('btn-guardar2').hidden = false;
        break
        case "no_editar":
            document.getElementById('btn-noeditar2').hidden = true;
            document.getElementById('btn-editar2').hidden = false;
            document.getElementById('id_ocupacion').disabled = true;
            document.getElementById('id_nombreEmpresa').disabled = true;
            document.getElementById('id_cargo').disabled = true;
            document.getElementById('id_nomRepresenLegal').disabled = true;
            document.getElementById('id_numDocRL').disabled = true;
            document.getElementById('id_fechaInicio').disabled = true;
            document.getElementById('id_fechaTerminacion').disabled = true;
            document.getElementById('id_direccion2').disabled = true;
            document.getElementById('id_mpioTrabajo').disabled = true;
            document.getElementById('id_dptoTrabajo').disabled = true;
            document.getElementById('id_telefono').disabled = true;
            document.getElementById('id_admRP').disabled = true;
            document.getElementById('id_pep').disabled = true;
            document.getElementById('id_activEcono').disabled = true;
            document.getElementById('id_ciiu').disabled = true;
            document.getElementById('id_banco').disabled = true;
            document.getElementById('id_numCuenta').disabled = true;
            document.getElementById('id_tipoCuenta').disabled = true;
            document.getElementById('id_ingresosActPrin').disabled = true;
            document.getElementById('id_otroIngreso1').disabled = true;
            document.getElementById('id_otroIngreso2').disabled = true;
            document.getElementById('id_egresos').disabled = true;
            document.getElementById('id_activos').disabled = true;
            document.getElementById('id_pasivos').disabled = true;
            document.getElementById('id_patrimonio').disabled = true;
            document.getElementById('btn-guardar2').hidden = true;
    }
}

// Funcion que cambia la edicion de actualizacion de la seccion configuracion, VIEW VerAscociado
function editarInputActualizacion3(dato){
    switch(dato){
        case "editar":
            document.getElementById('btn-editar3').hidden = true;
            document.getElementById('btn-noeditar3').hidden = false;
            document.getElementById('id_empresaDcto').disabled = false;
            document.getElementById('id_primerMes').disabled = false;
            document.getElementById('id_servFuneraria').disabled = false;
            document.getElementById('flexSwitchCheckChecked').disabled = false;
            document.getElementById('flexSwitchCheckChecked_1').disabled = false;
            document.getElementById('btn-guardar3').hidden = false;
        break
        case "no_editar":
            document.getElementById('btn-editar3').hidden = false;
            document.getElementById('btn-noeditar3').hidden = true;
            document.getElementById('id_empresaDcto').disabled = true;
            document.getElementById('id_servFuneraria').disabled = true;
            document.getElementById('id_primerMes').disabled = true;
            document.getElementById('flexSwitchCheckChecked').disabled = true;
            document.getElementById('flexSwitchCheckChecked_1').disabled = true;
            document.getElementById('btn-guardar3').hidden = true;
        }
}

// Funcion que muestra y oculta el input de "Autorización Descuento de Nomina" seccion configuracion, VIEW VerAscociado
function mostrarAutorizacion(dato){
    switch(dato){
        case "cambio":
            document.getElementById('contenedorAutorizacion').style.display = "block";
            document.getElementById('contenedorAutorizacion2').style.display = "none";
            document.getElementById('flexSwitchCheckChecked').checked = true;
        break
        case "ocultar":
            document.getElementById('contenedorAutorizacion').style.display = "none";
            document.getElementById('contenedorAutorizacion2').style.display = "block";
            document.getElementById('flexSwitchCheckChecked_1').checked = false;
        case "ocultar2":
            document.getElementById('contenedorAutorizacion').style.display = "none";
            document.getElementById('contenedorAutorizacion2').style.display = "block";
            document.getElementById('flexSwitchCheckChecked_2').hidden = true;
            document.getElementById('flexSwitchCheckChecked_1').checked = false;
        
    }
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
            // Obtenemos la informacion del model Nacimiento, del template formatos.html por medio de su id
            let fechaNacimiento = document.getElementById('id_fechaNacimiento').value;
            let dtoNacimiento = document.getElementById('id_dtoNacimiento').value;
            let mpioNacimiento = document.getElementById('id_mpioNacimiento').value;
            // Obtenemos la informacion del model Residencia, del template formatos.html por medio de su id
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
            // Obtenemos la informacion del model Refencia Familiar, del template formatos.html por medio de su id
            let nombreRF = document.getElementById('id_nombreRF').value;
            let parentesco = document.getElementById('id_parentesco').value;
            let numContacto = document.getElementById('id_numContacto').value;
            // Obtenemos la informacion del model Parentesco Asociado, del template formatos.html por medio de su id
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
            generarPDF(url, nombre, apellido, tipoDocumento, numDocumento, fechaExpedicion, mpioDoc, nacionalidad, fechaNacimiento, genero, estadoCivil, email, numResidencia, numCelular,envioInfoCorreo, envioInfoMensaje, envioInfoWhatsapp, nivelEducativo, tituloPregrado, tituloPosgrado, dtoNacimiento, mpioNacimiento, tipoVivienda, estrato, direccion, barrio, deptoResidencia, mpioResidencia, ocupacion, nombreEmpresa, cargo, nomRepresenLegal, numDocRL, fechaInicio, fechaTerminacion, direccionLab, mpioTrabajo, dptoTrabajo, telefono, admRP, pep, activEcono, ciiu, banco, numCuenta, tipoCuenta, actualizacion, tPersona, fechaHoy, nombreRF, parentesco, numContacto, autorizaciondcto, empresa, ingresosActPrin, otroIngreso1, otroIngreso2, egresos, activos, pasivos, patrimonio);
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
            // Obtenemos la informacion del model Nacimiento, del template formatos.html por medio de su id
            let fechaNacimientoF2 = document.getElementById('id_fechaNacimiento').value;
            // Obtenemos la informacion del model Residencia, del template formatos.html por medio de su id
            let direccionF2 = document.getElementById('id_direccion').value;
            let barrioF2 = document.getElementById('id_barrio').value;
            let mpioResidenciaF2 = document.getElementById('id_mpioResidencia').value;
            // Obtenemos la informacion del model Refencia Familiar, del template formatos.html por medio de su id
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
                arrayBeneficiarios.push([nombre, apellido, numDocu, parentesco, nac, repatriacion]);
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
            // Obtenemos la informacion del model Residencia, del template formatos.html por medio de su id
            let direccionF3 = document.getElementById('id_direccion').value;
            let barrioF3 = document.getElementById('id_barrio').value;
            let mpioResidenciaF3 = document.getElementById('id_mpioResidencia').value;
            // Obtenemos la informacion del model Nacimiento, del template formatos.html por medio de su id
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
            console.log(arrayBeneficiariosF4)
            // Obtenemos la informacion del model Mascota, del template formatos.html por medio de su id
            let cuentaMascotaF4 = document.getElementById('id_cuentaMascota').value;
            let arrayMascotasF4 = [];
            if(cuentaMascotaF4 > 0){
                for(let i = 1; i <= cuentaMascotaF4 ; i++){
                    let nombreMasc = (document.getElementById('id_nombreMasc_'+i).value);
                    arrayMascotasF4.push([nombreMasc]);
                }
            }
            let pdf = generarPDFf4(url, fechaCorte, nombreF4, numDocF4, mpioResidenciaF4, direccionF4, numCelularF4, concepto1, cuotaVencida, cuotaMes1, totalConcepto1, concepto2, cuotaMes2, totalConcepto2, concepto3, cuotaMes3, totalConcepto3, concepto4, cuotaMes4, totalConcepto4, concepto5, cuotaMes5, totalConcepto5, concepto6, cuotaMes6, totalConcepto6, pagoTotal, cuentaBeneficiariosF4, arrayBeneficiariosF4, arrayMascotasF4, saldo, mensaje)
            return pdf;   
        }
}



// Formato 1
// Formato de registro y actualizacion
async function generarPDF(url, nombre, apellido, tipoDocumento, numDocumento, fechaExpedicion, mpioDoc, nacionalidad, fechaNacimiento, genero, estadoCivil, email, numResidencia, numCelular,envioInfoCorreo, envioInfoMensaje, envioInfoWhatsapp, nivelEducativo, tituloPregrado, tituloPosgrado, dtoNacimiento, mpioNacimiento, tipoVivienda, estrato, direccion, barrio, deptoResidencia, mpioResidencia, ocupacion, nombreEmpresa, cargo, nomRepresenLegal, numDocRL, fechaInicio, fechaTerminacion, direccionLab, mpioTrabajo, dptoTrabajo, telefono, admRP, pep, activEcono, ciiu, banco, numCuenta, tipoCuenta, actualizacion, tPersona, fechaHoy, nombreRF, parentesco, numContacto, autorizaciondcto, empresa, ingresosActPrin, otroIngreso1, otroIngreso2, egresos, activos, pasivos, patrimonio) {

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
    pdf.text(activEcono, 326, 638);
    pdf.text(ciiu, 550, 638);

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
    pdf.text(arrFechaHoy[2], 227,680);
    pdf.text(arrFechaHoy[1], 372,680);
    pdf.text(arrFechaHoy[0], 495,680);
    pdf.text("ARMENIA", 25, 690);

    // Ultima Fila
    pdf.text(nomCompleto, 165, 752);
    pdf.text(numDocumento, 165, 773);

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
    var arrFechaHoy = fechaHoyF2.split("-")
    pdf.text(arrFechaHoy[2], 253,110);
    pdf.text(arrFechaHoy[1], 292,110);
    pdf.text(arrFechaHoy[0], 338,110);

    // renglon 0
    if(actualizacionF2 == "True"){
        pdf.text("X", 411, 130);
    }else if(tPersonaF2 == "PERSONA NATURAL"){
        pdf.text("X", 24, 130);
    }else{
        pdf.text("X", 222, 130);
    }


    // Fila 1
    pdf.text(nombreF2, 26,184);
    pdf.text(apellidoF2, 327,184);

    // Fila 2
    if(tipoDocumentoF2 == 'REGISTRO CIVIL'){
        pdf.text("X", 23,216);
    }else if (tipoDocumentoF2 == 'CEDULA'){
        pdf.text("X", 43,216);
    }else if (tipoDocumentoF2 == 'TARJETA IDENTIDAD'){
        pdf.text("X", 66,216);
    }else if (tipoDocumentoF2 == 'CEDULA EXTRANJERIA'){
        pdf.text("X", 86,216);
    }else{
        pdf.text("X", 108,216);
    }

    pdf.text(numDocumentoF2, 133,216);
    pdf.text(direccionF2, 324,216);

    // Fila 3
    pdf.text(barrioF2, 26,247);
    pdf.text(mpioResidenciaF2, 190,247);
    pdf.text(numCelularF2, 323,247);
    pdf.text(numContactoF2, 462,247);

    // Fila 4
    pdf.text(emailF2, 26,278);

    // Fila 5
    if(envioInfoCorreoF2 == "True"){
        pdf.text("X", 108,312);
    }
    if(envioInfoMensajeF2 == "True"){
        pdf.text("X", 229,312);
    }
    if(envioInfoWhatsappF2 == "True"){
        pdf.text("X", 330,312);
    }
 
    //  Cuadro de beneficiarios
    pdf.setFontSize(9);
    let fila = 389;
    let filaR = 581;
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
        pdf.text(arrayBeneficiarios[i][2], 350 ,fila);
        pdf.text(arrayBeneficiarios[i][3], 438 ,fila);
        var fecha = arrayBeneficiarios[i][4].split("-");
        pdf.text(fecha[2], 519 ,fila);
        pdf.text(fecha[1], 542 ,fila);
        pdf.text(fecha[0], 566 ,fila);
        // se diligencia el cuadro de repatriacion
        if(arrayBeneficiarios[i][5] != 'None'){
            pdf.text("X", 51,filaR);
            pdf.setFontSize(8);
            pdf.text(arrayBeneficiarios[i][0], 125 ,filaR);
            pdf.text(arrayBeneficiarios[i][2], 299 ,filaR);
            pdf.text(arrayBeneficiarios[i][5], 493 ,filaR);
        }
        if(arrayBeneficiarios[i][5] != 'None'){
            filaR = filaR + 16;
        }
        fila = fila + 16;
    }

    // Se diligencia Cuadro de Mascota
    let filaM = 686;
    for(let i = 0; i < arrayMascotas.length; i++){
        pdf.text("X", 51,filaM);
        pdf.text(arrayMascotas[i][0], 125 ,filaM);
        if(arrayMascotas[i][1] == 'GATO'){
            pdf.text("X", 283 ,filaM);
        }else{
            pdf.text("X", 305 ,filaM);
        }
        pdf.text(arrayMascotas[i][2], 320 ,filaM);
        var fechaMasc = arrayMascotas[i][3].split("-");
        pdf.text(fechaMasc[2], 441 ,filaM);
        pdf.text(fechaMasc[1], 469 ,filaM);
        pdf.text(fechaMasc[0], 492 ,filaM);
        if(arrayMascotas[i][4] == 'True'){
            pdf.text("X", 534 ,filaM);
        }else{
            pdf.text("X", 575 ,filaM);
        }
        filaM = filaM + 16;    
    }

    // Firma y Huella
    pdf.setFontSize(12);
    pdf.text(arrFechaHoy[2], 240,844);
    pdf.text(arrFechaHoy[1], 390,844);
    pdf.text(arrFechaHoy[0], 485,844);
    pdf.text("Armenia", 25,855);

    // Firma
    var nomCompleto = nombreF2 + " " + apellidoF2
    pdf.text(nomCompleto, 160 ,912);
    pdf.text(numDocumentoF2, 160 ,935);

    pdf.save('Formato_Servicios_Exequiales_'+numDocumentoF2+'.pdf');

}

// Formato 3
// Formato Auxilios
async function generarPDFf3(url, fechaHoyF3, nombreF3, apellidoF3, tipoDocumentoF3, numDocumentoF3, fechaExpedicionF3, mpioDocF3, emailF3, numCelularF3, direccionF3, barrioF3, mpioResidenciaF3, fechaNacimientoF3, nombreEmpresaF3, cargoF3, telefonoF3, ingresosActPrinF3, bancoF3, numCuentaF3, nombre2, numDoc2, parentescoF3, nivelEducativoF3, anexoOne, anexoTwo, anexoThree, anexoFour, anexoFive, anexoSix, anexoSeven, anexoEight, envioInfoCorreoF3, envioInfoMensajeF3, envioInfoWhatsappF3, tipoAuxilio) {
    console.log(url)
    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'legal');
    pdf.addImage(image, 'PNG', 0, 0, 613, 1010);

    pdf.setFontSize(9);

    // fecha encabezado
    var arrFechaHoy = fechaHoyF3.split("-");
    pdf.text(arrFechaHoy[2], 250,105);
    pdf.text(arrFechaHoy[1], 274,105);
    pdf.text(arrFechaHoy[0], 295,105);
    
    pdf.setFontSize(12);
    // renglon 0
    pdf.text(nombreF3, 70,174);
    pdf.text(apellidoF3, 300,174);

    // // renglon 1
    pdf.text("X", 67,222);
    pdf.text("X", 83,222);
    pdf.text("X", 100,222);
    pdf.text("X", 124,222);
    pdf.text(numDocumentoF3, 161,222);

    var arrFechaExp = fechaExpedicionF3.split("-");
    pdf.text(arrFechaExp[2], 296,222);
    pdf.text(arrFechaExp[1], 321,222);
    pdf.text(arrFechaExp[0], 343,222);
    pdf.setFontSize(8);
    pdf.text(mpioDocF3, 381,222);
    pdf.setFontSize(12);

    var arrFechaNac = fechaNacimientoF3.split("-");
    pdf.text(arrFechaNac[2], 460, 222);
    pdf.text(arrFechaNac[1], 488, 222);
    pdf.text(arrFechaNac[0], 519, 222);

    // // renglon 2
    pdf.text(direccionF3, 70,255);
    pdf.setFontSize(8);
    pdf.text(barrioF3, 295,255);
    pdf.text(mpioResidenciaF3, 381,255);
    pdf.setFontSize(12);
    pdf.text(numCelularF3, 462,255);

    // // renglon 3
    pdf.text(emailF3, 182,269);

    // // renglon 4
    pdf.text(nombreEmpresaF3, 70,302);
    pdf.setFontSize(8);
    pdf.text(cargoF3, 295,302);
    pdf.setFontSize(12);
    pdf.text(ingresosActPrinF3, 383,302);
    pdf.text(telefonoF3, 462,302);

    // // renglon 5
    pdf.text(bancoF3, 70,334);
    pdf.text(numCuentaF3, 300,334);

    // Tipos Auxilios
    // optico
    if(tipoAuxilio == '1'){
        pdf.text("X", 323,435);
    }// incapacidad medica
    else if(tipoAuxilio == '2'){
        pdf.text("X", 323,415);
    }// auxilio educativo-u
    else if(tipoAuxilio == '3'){
        pdf.text("X", 82,379);
    }// kit maternidad
    else if(tipoAuxilio == '4'){
        pdf.text("X", 82,415);
    }//auxilio educativo-maestria
    else if(tipoAuxilio == '5'){
        pdf.text("X", 82,396);
    }//servicio exequial
    else if(tipoAuxilio == '6'){
        pdf.text("X", 82,435);
    }//calamidad domestica
    else if(tipoAuxilio == '7'){
        pdf.text("X", 323,377);
    }//calamidad domestica-medica
    else if(tipoAuxilio == '8'){
        pdf.text("X", 323,395);
    }

    // Campo - se solicita para
    if(tipoAuxilio == '3' || tipoAuxilio == '5'){
        pdf.text(nombre2, 70, 495);
        pdf.text(numDoc2, 300, 495);
        pdf.text(parentescoF3, 436, 495);
        pdf.text(nivelEducativoF3, 175, 511);
    }

    // Campo - Anexos
    pdf.setFontSize(10);
    if(anexoOne != 'None'){
        pdf.text(anexoOne, 100, 552);
    }
    if(anexoTwo != 'None'){
        pdf.text(anexoTwo, 100, 571);
    }
    if(anexoThree != 'None'){
        pdf.text(anexoThree, 100, 590);
    }
    if(anexoFour != 'None'){
        pdf.text(anexoFour, 100, 609);
    }
    if(anexoFive != 'None'){
        pdf.text(anexoFive, 343, 552);   
    }
    if(anexoSix != 'None'){
        pdf.text(anexoSix, 343, 571);
    }
    if(anexoSeven != 'None'){
        pdf.text(anexoSeven, 343, 590);
    }
    if(anexoEight != 'None'){
        pdf.text(anexoEight, 343, 609);
    }

    // campo autorizacion envio informacion
    if(envioInfoCorreoF3 == 'True'){
        pdf.text("X", 347, 672);
    }else{
        pdf.text("X", 363, 672);
    }

    if(envioInfoMensajeF3 == 'True'){
        pdf.text("X", 347, 687);
    }else{
        pdf.text("X", 363, 687);
    }

    if(envioInfoWhatsappF3 == 'True'){
        pdf.text("X", 347, 703);
    }else{
        pdf.text("X", 363, 703);
    } 
    // facebook e instragram
    pdf.text("X", 502, 672);
    pdf.text("X", 502, 687);

    pdf.save('Formato_Auxilios_'+numDocumentoF3+'.pdf');

}

// Formato 4
// Formato Extracto
async function generarPDFf4(url, fechaCorte, nombreF4, numDocF4, mpioResidenciaF4, direccionF4, numCelularF4, concepto1, cuotaVencida, cuotaMes1, totalConcepto1, concepto2, cuotaMes2, totalConcepto2, concepto3, cuotaMes3, totalConcepto3, concepto4, cuotaMes4, totalConcepto4, concepto5, cuotaMes5, totalConcepto5, concepto6, cuotaMes6, totalConcepto6, pagoTotal, cuentaBeneficiariosF4, arrayBeneficiariosF4, arrayMascotasF4, saldo, mensaje) {
    console.log(url)
    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'legal');
    pdf.addImage(image, 'PNG', 0, 0, 613, 1010);

  
    // renglon 0
    pdf.setFontSize(9);
    pdf.text(nombreF4, 29,151);
    pdf.text(numDocF4, 239,151);
    pdf.text(mpioResidenciaF4, 335,151);

    var arrFechaCorte = fechaCorte.split("-");
    pdf.text(arrFechaCorte[2]+'/', 471,151);
    pdf.text(arrFechaCorte[1]+'/', 486,151);
    pdf.text(arrFechaCorte[0], 502,151);

    pdf.text(direccionF4, 105,172);
    pdf.text(numCelularF4, 437,172);

    // valores a pagar
    pdf.setFontSize(9);
    
    pdf.text(concepto1, 30,285);
    pdf.text(arrFechaCorte[2]+'/', 177,285);
    pdf.text(arrFechaCorte[1]+'/', 190,285);
    pdf.text(arrFechaCorte[0], 204,285);
    if(saldo != 0){
        console.log(saldo);
        const saldoFormateado = saldo.toLocaleString('es-ES'); 
        pdf.text(saldoFormateado, 252,285);
        console.log(saldoFormateado);
    }

    pdf.text(cuotaVencida, 324,285);
    pdf.text(cuotaMes1, 382,285);
    // pdf.text('0', 452,285); interes de mora
    pdf.text(totalConcepto1, 520,285);

    let fila = 305
    if(cuotaMes2 > 0){
        pdf.text(concepto2, 30,fila);
        pdf.text(arrFechaCorte[2]+'/', 177,fila);
        pdf.text(arrFechaCorte[1]+'/', 190,fila);
        pdf.text(arrFechaCorte[0], 204,fila);
        // pdf.text('saldo', 248,fila);
        pdf.text(cuotaVencida, 324,fila);
        pdf.text(cuotaMes2, 382,fila);
        // pdf.text('interes mora', 452,fila);
        pdf.text(totalConcepto2, 520,fila);
        fila = fila + 20
    }
    if(cuotaMes3 > 0){
        pdf.text(concepto3, 30,fila);
        pdf.text(arrFechaCorte[2]+'/', 177,fila);
        pdf.text(arrFechaCorte[1]+'/', 190,fila);
        pdf.text(arrFechaCorte[0], 204,fila);
        // pdf.text('saldo', 248,fila);
        pdf.text(cuotaVencida, 324,fila);
        pdf.text(cuotaMes3, 382,fila);
        // pdf.text('interes mora', 452,fila);
        pdf.text(totalConcepto3, 520,fila);
        fila = fila + 20
    }
    if(cuotaMes4 > 0){
        pdf.text(concepto4, 30,fila);
        pdf.text(arrFechaCorte[2]+'/', 177,fila);
        pdf.text(arrFechaCorte[1]+'/', 190,fila);
        pdf.text(arrFechaCorte[0], 204,fila);
        // pdf.text('saldo', 248,fila);
        pdf.text(cuotaVencida, 324,fila);
        pdf.text(cuotaMes4, 382,fila);
        // pdf.text('interes mora', 452,fila);
        pdf.text(totalConcepto4, 520,fila);
        fila = fila + 20
    }
    if(cuotaMes5 > 0){
        pdf.text(concepto5, 30,fila);
        pdf.text(arrFechaCorte[2]+'/', 177,fila);
        pdf.text(arrFechaCorte[1]+'/', 190,fila);
        pdf.text(arrFechaCorte[0], 204,fila);
        // pdf.text('saldo', 248,fila);
        pdf.text(cuotaVencida, 324,fila);
        pdf.text(cuotaMes5, 382,fila);
        // pdf.text('interes mora', 452,fila);
        pdf.text(totalConcepto5, 520,fila);
        fila = fila + 20
    }
    if(cuotaMes6 > 0){
        pdf.text(concepto6, 30,fila);
        pdf.text(arrFechaCorte[2]+'/', 177,fila);
        pdf.text(arrFechaCorte[1]+'/', 190,fila);
        pdf.text(arrFechaCorte[0], 204,fila);
        // pdf.text('saldo', 248,fila);
        pdf.text(cuotaVencida, 324,fila);
        pdf.text(cuotaMes6, 382,fila);
        // pdf.text('interes mora', 452,fila);
        pdf.text(totalConcepto6, 520,fila);
        fila = fila + 20
    }
    
    // valor total a pagar
    pdf.setTextColor(255,255,255)
    pdf.setFont(undefined, "bold");
    pdf.setFontSize(12)
    pdf.text(pagoTotal, 523,439);
    // observaciones
    pdf.setTextColor(0,0,0);
    pdf.setFont(undefined, "normal");

    pdf.setFontSize(10)
    pdf.text(mensaje, 30,460);

    pdf.setFontSize(8)
    let filaB = 567;
    // se lista beneficiarios
    for(let i = 0;i < arrayBeneficiariosF4.length; i++){
        pdf.text(arrayBeneficiariosF4[i][0], 30,filaB);
        if(arrayBeneficiariosF4[i][2] != 'None'){
            pdf.text(arrayBeneficiariosF4[i][2], 332,filaB);
        }
        pdf.text(arrayBeneficiariosF4[i][1], 515,filaB);
        filaB = filaB + 13;
    }

    var perro = new Image()
    perro.src = '/static/img/icons/huella.png';
    perro.onload = () => {

    // se lista mascotas
    for(let i = 0;i < arrayMascotasF4.length; i++){
        pdf.text(arrayMascotasF4[i][0], 30,filaB);
        pdf.addImage(perro, 'PNG', 462,filaB-18, 23,23);
        filaB += 20;
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

    pdf.save('Formato_Extracto_'+numDocF4+'.pdf');
    
    // se cierra el onload del image
    };
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
        pdf.text(arrayExtracto[i][1], 239,151);
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
            pdf.text(arrayExtracto[i][9], 252,285);
        }
        //cuota vencida 
        pdf.text(arrayExtracto[i][10], 324,285);
        // cuota Mes
        pdf.text(arrayExtracto[i][11], 382,285);
        // pdf.text('0', 452,285); interes de mora
        pdf.text(arrayExtracto[i][12], 520,285);

        let fila = 305
        // inicia posicion 13
        if(arrayExtracto[i][14] > 0){
            pdf.text(arrayExtracto[i][13], 30,fila);
            pdf.text(arrFechaCorte[2]+'/', 177,fila);
            pdf.text(arrFechaCorte[1]+'/', 190,fila);
            pdf.text(arrFechaCorte[0], 204,fila);
            // pdf.text('saldo', 248,fila);
            pdf.text(arrayExtracto[i][10], 324,fila);
            pdf.text(arrayExtracto[i][14], 382,fila);
            // pdf.text('interes mora', 452,fila);
            pdf.text(arrayExtracto[i][15], 520,fila);
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
            pdf.text(arrayExtracto[i][17], 382,fila);
            // pdf.text('interes mora', 452,fila);
            pdf.text(arrayExtracto[i][18], 520,fila);
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
            pdf.text(arrayExtracto[i][20], 382,fila);
            // pdf.text('interes mora', 452,fila);
            pdf.text(arrayExtracto[i][21], 520,fila);
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
            pdf.text(arrayExtracto[i][23], 382,fila);
            // pdf.text('interes mora', 452,fila);
            pdf.text(arrayExtracto[i][24], 520,fila);
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
            pdf.text(arrayExtracto[i][26], 382,fila);
            // pdf.text('interes mora', 452,fila);
            pdf.text(arrayExtracto[i][27], 520,fila);
            fila = fila + 20
        }
    

        // valor total a pagar
        pdf.setTextColor(255,255,255)
        pdf.setFont(undefined, "bold");
        pdf.setFontSize(12)
        // inicia posicion 28
        pdf.text(arrayExtracto[i][28], 523,439);
        // observaciones
        pdf.setTextColor(0,0,0);
        pdf.setFont(undefined, "normal");

        pdf.setFontSize(10)
        pdf.text(arrayExtracto[i][29], 30,460);

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
            filaB += 20;
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


