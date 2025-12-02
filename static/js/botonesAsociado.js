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
        case "editar10":
            document.getElementById('aportePago').disabled = false;
            document.getElementById('btn_editar10').hidden = true;
            document.getElementById('btn_no_editar10').hidden = false;
        break
        case "no_editar10":
            document.getElementById('aportePago').disabled = true;
            document.getElementById('btn_editar10').hidden = false;
            document.getElementById('btn_no_editar10').hidden = true;
        break
        case "editar11":
            document.getElementById('bSocialPago').disabled = false;
            document.getElementById('btn_editar11').hidden = true;
            document.getElementById('btn_no_editar11').hidden = false;
        break
        case "no_editar11":
            document.getElementById('bSocialPago').disabled = true;
            document.getElementById('btn_editar11').hidden = false;
            document.getElementById('btn_no_editar11').hidden = true;
        break
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
                'convenioPago',
                'aportePago',
                'bSocialPago'
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


// Funcion que cambia la edicion de actualizacion de la seccion datos personales, VIEW VerAscociado
function editarInputActualizacion1(dato) {
    const campos = document.querySelectorAll('.editable1');
    const btnEditar = document.getElementById('btn-editar');
    const btnNoEditar = document.getElementById('btn-noeditar');
    const btnGuardar = document.getElementById('btn-guardar');

    const activar = dato === 'editar';

    btnEditar.hidden = activar;
    btnNoEditar.hidden = !activar;
    btnGuardar.disabled = !activar;

    campos.forEach(campo => campo.disabled = !activar);
}

// Funcion que cambia la edicion de actualizacion de la seccion laboral, VIEW VerAscociado
function editarInputActualizacion2(dato) {
    const campos = document.querySelectorAll('.editable2');
    const btnEditar = document.getElementById('btn-editar2');
    const btnNoEditar = document.getElementById('btn-noeditar2');
    const btnGuardar = document.getElementById('btn-guardar2');

    const activar = dato === 'editar';

    btnEditar.hidden = activar;
    btnNoEditar.hidden = !activar;
    btnGuardar.disabled = !activar;

    campos.forEach(campo => campo.disabled = !activar);
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