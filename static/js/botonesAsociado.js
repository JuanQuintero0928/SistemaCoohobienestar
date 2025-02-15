// Funcion que cambia la edicion en el proceso de pago, VIEW EditarPago, app Historico
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
            document.getElementById('diferencia').disabled = false;
            document.getElementById('btn_editar2').hidden = true;
            document.getElementById('btn_no_editar2').hidden = false;
        break
        case "no_editar2":
            document.getElementById('diferencia').disabled = true;
            document.getElementById('btn_editar2').hidden = false;
            document.getElementById('btn_no_editar2').hidden = true;
        break
        case "editar3":
            document.getElementById('mascotaPago').disabled = false;
            document.getElementById('btn_editar3').hidden = true;
            document.getElementById('btn_no_editar3').hidden = false;
        break
        case "no_editar3":
            document.getElementById('mascotaPago').disabled = true;
            document.getElementById('btn_editar3').hidden = false;
            document.getElementById('btn_no_editar3').hidden = true;
        break
        case "editar4":
            document.getElementById('repatriacionPago').disabled = false;
            document.getElementById('btn_editar4').hidden = true;
            document.getElementById('btn_no_editar4').hidden = false;
        break
        case "no_editar4":
            document.getElementById('repatriacionPago').disabled = true;
            document.getElementById('btn_editar4').hidden = false;
            document.getElementById('btn_no_editar4').hidden = true;
        break
        case "editar5":
            document.getElementById('seguroVidaPago').disabled = false;
            document.getElementById('btn_editar5').hidden = true;
            document.getElementById('btn_no_editar5').hidden = false;
        break
        case "no_editar5":
            document.getElementById('seguroVidaPago').disabled = true;
            document.getElementById('btn_editar5').hidden = false;
            document.getElementById('btn_no_editar5').hidden = true;
        break
        case "editar6":
            document.getElementById('adicionalesPago').disabled = false;
            document.getElementById('btn_editar6').hidden = true;
            document.getElementById('btn_no_editar6').hidden = false;
        break
        case "no_editar6":
            document.getElementById('adicionalesPago').disabled = true;
            document.getElementById('btn_editar6').hidden = false;
            document.getElementById('btn_no_editar6').hidden = true;
        break
        case "editar7":
            document.getElementById('coohopAporte').disabled = false;
            document.getElementById('btn_editar7').hidden = true;
            document.getElementById('btn_no_editar7').hidden = false;
        break
        case "no_editar7":
            document.getElementById('coohopAporte').disabled = true;
            document.getElementById('btn_editar7').hidden = false;
            document.getElementById('btn_no_editar7').hidden = true;
        break
        case "editar8":
            document.getElementById('coohopBsocial').disabled = false;
            document.getElementById('btn_editar8').hidden = true;
            document.getElementById('btn_no_editar8').hidden = false;
        break
        case "no_editar8":
            document.getElementById('coohopBsocial').disabled = true;
            document.getElementById('btn_editar8').hidden = false;
            document.getElementById('btn_no_editar8').hidden = true;
        break
        case "editar9":
            document.getElementById('convenioPago').disabled = false;
            document.getElementById('btn_editar9').hidden = true;
            document.getElementById('btn_no_editar9').hidden = false;
        break
        case "no_editar9":
            document.getElementById('convenioPago').disabled = true;
            document.getElementById('btn_editar9').hidden = false;
            document.getElementById('btn_no_editar9').hidden = true;
        break
        // case "editar10":
        // document.getElementById('diferencia').disabled = false;
        // document.getElementById('btn_editar10').hidden = true;
        // document.getElementById('btn_no_editar10').hidden = false;
        // break
        // case "no_editar10":
        //     document.getElementById('diferencia').disabled = true;
        //     document.getElementById('btn_editar10').hidden = false;
        //     document.getElementById('btn_no_editar10').hidden = true;
        // break
        case "habilitar":
            const inputs = [
                'valorPago', 
                'diferencia', 
                'mascotaPago', 
                'repatriacionPago', 
                'seguroVidaPago', 
                'adicionalesPago', 
                'coohopAporte', 
                'coohopBsocial', 
                'convenioPago'
            ];
            // Iterar sobre los IDs y habilitar solo los que existen
            inputs.forEach(id => {
                const input = document.getElementById(id);
                if (input) {  // Si el input existe
                    input.disabled = false;
                }
            });
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
            document.getElementById('id_indicativo').disabled = false;
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
            document.getElementById('btn-guardar').disabled = false;
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
            document.getElementById('id_indicativo').disabled = true;
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
            document.getElementById('btn-guardar').disabled = true;
            document.getElementById('id_fechaRetiro').disabled = true;
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
            document.getElementById('btn-guardar2').disabled = false;
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
            document.getElementById('btn-guardar2').disabled = true;
    }
}

// Funcion que cambia la edicion de actualizacion de la seccion configuracion, VIEW VerAscociado
function editarInputActualizacion3(dato){
    switch(dato){
        case "editar":
            document.getElementById('btn-editar3').hidden = true;
            document.getElementById('btn-noeditar3').hidden = false;
            document.getElementById('id_primerMes').disabled = false;
            document.getElementById('id_servFuneraria').disabled = false;
            document.getElementById('flexSwitchCheckChecked').disabled = false;
            document.getElementById('btn-guardar3').disabled = false;
            mostrarAutorizacion()

        break
        case "no_editar":
            document.getElementById('btn-editar3').hidden = false;
            document.getElementById('btn-noeditar3').hidden = true;
            document.getElementById('id_servFuneraria').disabled = true;
            document.getElementById('id_primerMes').disabled = true;
            document.getElementById('flexSwitchCheckChecked').disabled = true;
            document.getElementById('id_empresaDcto').disabled = true;
            document.getElementById('btn-guardar3').disabled = true;
        }
}

// Funcion que muestra y oculta el input de "Autorización Descuento de Nomina" seccion configuracion, VIEW VerAscociado
function mostrarAutorizacion(){
   let checkbox = document.getElementById('flexSwitchCheckChecked');
   let select = document.getElementById('id_empresaDcto');
   
   if(checkbox.checked){
       select.disabled = false;
   }else{
       select.disabled = true;
   }
}

document.addEventListener('DOMContentLoaded', function () {
    const estadoAsociado = document.getElementById('id_estadoAsociado');
    const retiroContainer = document.getElementById('retiroContainer');
    const fechaRetiro = document.getElementById('id_fechaRetiro');

    // Función para mostrar/ocultar y agregar/quitar required
    const actualizarEstadoRetiro = () => {
        if (estadoAsociado.value === 'RETIRO') {
            retiroContainer.hidden = false; // Muestra el campo
            fechaRetiro.setAttribute('required', 'required'); // Lo hace obligatorio
        } else {
            retiroContainer.hidden = true; // Oculta el campo
            fechaRetiro.removeAttribute('required'); // Lo vuelve opcional
        }
    };

    // Escuchar cambios en el select
    estadoAsociado.addEventListener('change', actualizarEstadoRetiro);

    // Verificar al cargar la página
    actualizarEstadoRetiro();
});