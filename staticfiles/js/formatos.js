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


// Funcion para formato registro de asociado, guarda fecha actualizacion y redirige a la funcion que genera PDF
async function guardarFechaYGenerarPDF(asociadoId, urlImagen, tipoFormato) {
    const inputFecha = document.getElementById('id_fechaActualizacionDatos');
    const fecha = inputFecha.value;
    const btn = document.getElementById('btnDescargar');
    const btnText = document.getElementById('btnText');
    const btnSpinner = document.getElementById('btnSpinner');

    if (!fecha) {
        Swal.fire({
            icon: 'info',
            title: 'Información faltante',
            text: 'Por favor, seleccione una fecha valida para continuar.',
            confirmButtonText: 'Ok',
            confirmButtonColor: '#3085d6'
        });
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
        await llamarPDF(1, urlImagen, asociadoId, tipoFormato);

    } catch (error) {
        console.error("Error:", error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Ocurrio un error al guardar la fecha.',
            confirmButtonText: 'Ok',
            confirmButtonColor: '#3085d6'
        });
    }
}


// Obtener CSRF del cookie
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}


// Funcion mostrar Spinner en botones de descarga
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


// Funcion ocultar Spinner en botones de descarga
function ocultarSpinner(boton) {
    if (!boton) return;

    const btnText = boton.querySelector('.btnText');
    const btnSpinner = boton.querySelector('.btnSpinner');

    if (btnText && btnSpinner) {
        boton.disabled = false;
        btnSpinner.classList.add('d-none');
        btnText.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-filetype-pdf" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M14 4.5V14a2 2 0 0 1-2 2h-1v-1h1a1 1 0 0 0 1-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5zM1.6 11.85H0v3.999h.791v-1.342h.803q.43 0 .732-.173.305-.175.463-.474a1.4 1.4 0 0 0 .161-.677q0-.375-.158-.677a1.2 1.2 0 0 0-.46-.477q-.3-.18-.732-.179m.545 1.333a.8.8 0 0 1-.085.38.57.57 0 0 1-.238.241.8.8 0 0 1-.375.082H.788V12.48h.66q.327 0 .512.181.185.183.185.522m1.217-1.333v3.999h1.46q.602 0 .998-.237a1.45 1.45 0 0 0 .595-.689q.196-.45.196-1.084 0-.63-.196-1.075a1.43 1.43 0 0 0-.589-.68q-.396-.234-1.005-.234zm.791.645h.563q.371 0 .609.152a.9.9 0 0 1 .354.454q.118.302.118.753a2.3 2.3 0 0 1-.068.592 1.1 1.1 0 0 1-.196.422.8.8 0 0 1-.334.252 1.3 1.3 0 0 1-.483.082h-.563zm3.743 1.763v1.591h-.79V11.85h2.548v.653H7.896v1.117h1.606v.638z"/>
            </svg>
        `;
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


// Funcion para obtener la informacion del formato de solicitud de crédito
async function cargarDatosFormatoCredito(asociadoId, tipoFormato, creditoId) {
    const response = await fetch(`/api/obtener_datos_solicitud_credito/${asociadoId}/${tipoFormato}/${creditoId}/`);
    const datos = await response.json();
    return datos;
}


// Funcion global de los formatos
async function llamarPDF(formato, url, asociadoId, tipoFormato, opciones = {}, boton = null) {
    try {

        if ([2, 3, 5, 6, 7, 8, 9].includes(formato)){
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
        // Formato Solicitud Crédito
        else if (formato == 5) {
            const creditoId = opciones.id_credito ?? null;
            const datos = await cargarDatosFormatoCredito(asociadoId, tipoFormato, creditoId);
            await generarPDFSolicitudCredito(url, datos)
        }
        // Pagare Persona Natural
        else if (formato == 6) {
            await generarPDFPagare(url)
        }
        // Otorgamiento de crédito
        else if (formato == 7) {
            const creditoId = opciones.id_credito ?? null;
            const datos = await cargarDatosFormatoCredito(asociadoId, tipoFormato, creditoId);
            await generarPDFOtorgamientoCredito(url, datos)
        }
        // Tabla de amortización
        else if (formato == 8) {
            const creditoId = opciones.id_credito ?? null;
            const datos = await cargarDatosFormatoCredito(asociadoId, tipoFormato, creditoId);
            await generarPDFTablaAmortizacion(url, datos)
        }
        // Formato retiro de asociado
        else if (formato == 9) {
            const datos = await cargarDatosFormatoRegistro(asociadoId, tipoFormato);
            await generarPDFRetiroAsociado(url, datos)
        }
    }
    catch (error) {
        const detalleTecnico = error instanceof Error ? error.stack : String(error);
    
        console.error("Error en la generación del PDF:", detalleTecnico);

        Swal.fire({
            icon: 'error',
            title: 'Ha ocurrido un error',
            text: 'Hubo un problema generando el PDF. Por favor intente nuevamente o contacte a soporte.',
            confirmButtonText: 'Ok',
            confirmButtonColor: '#3085d6'
        });

        return;
    } finally {
        if ([2, 3, 5, 6, 7, 8, 9].includes(formato)){
            ocultarSpinner(boton);
        }
    }
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

    const ingresosMap = [
        { valor: datos.ingrSalario, texto: "Salario" },
        { valor: datos.ingrHorasExtras, texto: "Horas extras" },
        { valor: datos.ingrPension, texto: "Pensión" },
        { valor: datos.ingrCompensacion, texto: "Compensación" },
        { valor: datos.ingrHonorarios, texto: "Honorarios" },
        { valor: datos.ingrVentas, texto: "Ventas" },
        { valor: datos.ingrIntereses, texto: "Intereses" },
        { valor: datos.ingrGiros, texto: "Giros" },
        { valor: datos.ingrArrendamientos, texto: "Arrendamientos" },
        { valor: datos.ingrOtros, texto: "Otros" },
    ];

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
    pdf.text("5", 287.5, 228.8);

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
    writeText(pdf, datos.numResidencia, 385, 489.5);
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
    writeText(pdf, datos.numDocRL, 461, 730.6);

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
        pdf.text("2.5", 502.5, 806.5);
    }

    // /////////////////////////////////////////////////////////////////////////////////////////
    // Se añade Pagina 3 al documento
    pdf.addPage();
    const image3 = await loadImage('/static/img/Registro_Asociados_2025_page_0003.jpg');
    pdf.addImage(image3, 'PNG', 0, 0, 613, 1010);

    pdf.text(nombreCompleto, 150.4, 877.2);
    pdf.text(datos.numDocumento, 150.4, 903.2);

    // /////////////////////////////////////////////////////////////////////////////////////////
    // Se añade Pagina 4 al documento
    pdf.addPage();
    const image4 = await loadImage('/static/img/Registro_Asociados_2025_page_0004.jpg');
    pdf.addImage(image4, 'PNG', 0, 0, 613, 1010);

    const listaIngresos = ingresosMap
        .filter(item => Number(item.valor) > 0)
        .map(item => item.texto)
        .join(", ");

    writeText(pdf, listaIngresos ? `${listaIngresos}` : "Sin ingresos", 49.1, 569.4);

    pdf.text(convertirDias(arrFechaHoy[0]), 299.1, 659.4);
    pdf.text(convertirMes(arrFechaHoy[1]), 469, 659.4);
    pdf.text(arrFechaHoy[2], 22.5, 670);
    pdf.text("Armenia", 147.8,669.4);

    pdf.text(nombreCompleto, 151.8, 742.7);
    pdf.text(datos.numDocumento, 151.8, 766);

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
    pdf.text(datos.barrio, 19, 249.2);
    pdf.text(datos.mpioResidencia, 190, 249.2);
    pdf.text(datos.numCelular, 323, 249.2);
    pdf.text(datos.numContacto, 471, 249.2);

    // renglon 4
    pdf.text(datos.email, 19,281);

    //  renglon 5
    if(datos.envioInfoCorreo){
        pdf.text("X", 105,312);
    }
    if(datos.envioInfoMensaje){
        pdf.text("X", 228,312);
    }
    if(datos.envioInfoWhatsapp){
        pdf.text("X", 329,312);
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
    pdf.setFontSize(9);
    pdf.text(convertirDias(arrFechaHoy[0]), 290, 861);
    pdf.text(convertirMes(arrFechaHoy[1]), 435, 861);
    pdf.text(arrFechaHoy[2], 541, 861);
    pdf.text("Armenia", 72,871);

    // // Firma
    pdf.text(nombreCompleto, 155 ,941);
    pdf.text(datos.numDocumento, 155 ,967);

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
    pdf.text(convertirDias(arrFechaHoy[0]), 292, 618);
    pdf.text(convertirMes(arrFechaHoy[1]), 432, 618);
    pdf.text(arrFechaHoy[2], 539, 618)
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

    // Variable eje y valores variables
    let y = 285

    // renglon 1
    pdf.text(extractoData.nombre, 16,138.5);
    pdf.text(extractoData.numDocumento, 244,138.5);
    pdf.text(extractoData.mpioResidencia, 339, 138.5)
    pdf.text(fechaFormateada, 486, 138.5)

    // renglon 2
    pdf.text(extractoData.direccion, 91,157.8);
    pdf.text(extractoData.numCelular, 486,157.8);

    // tabla valores a pagar
    pdf.setFontSize(9);

    extractoData.conceptos_detallados.forEach((concepto) => {
        // Si el texto supera los 24 caracteres, lo corta y agrega "..."
        let textoConcepto = concepto.concepto;
        if (textoConcepto.length > 24) {
            textoConcepto = textoConcepto.substring(0, 24) + '...';
        }

        pdf.text(textoConcepto, 17, y);
        if (concepto.saldo < 0 || concepto.saldo > 0) {
            pdf.text(formatearNumero(concepto.saldo), 245, y);
        }
        pdf.text(fechaFormateada, 166, y);
        writeText(pdf, concepto.cuotas_vencidas.toString(), 329, y);
        pdf.text(formatearNumero(concepto.cuota_mes), 385, y);
        pdf.text(formatearNumero(concepto.total_a_pagar), 531, y);
        y += 15;
    });

    // valor total a pagar
    pdf.setTextColor(255,255,255);
    pdf.setFont(undefined, "bold");
    pdf.setFontSize(12);
    pdf.text(formatearNumero(extractoData.pagoTotal), 523,526.7);

    // observaciones
    pdf.setTextColor(0,0,0);
    pdf.setFontSize(10);
    pdf.setFont("verdana", "normal");
    // pdf.text(extractoData.mensaje, 30,460);

    pdf.setFontSize(9);

    // variables tabla beneficiarios
    let count_benef = 0;
    let x_benef_nombre = 17;
    let x_benef_repatriacion = 161;
    let x_benef_mascota = 245;
    let y_benef = 621.3;
    
    // funcion que actualiza valores para la segunda columna de la tabla
    function actualizarPosicionBeneficiarios() {
        if (count_benef === 8) {
            x_benef_nombre = 301;
            x_benef_repatriacion = 452;
            x_benef_mascota = 539;
            y_benef = 621.3;
        }
    }

    // tabla beneficiarios
    extractoData.beneficiarios.forEach((concepto) => {
        // Si el texto supera los 22 caracteres, lo corta y agrega "..."
        let textoConcepto = concepto.nombre;
        if (textoConcepto.length > 22) {
            textoConcepto = textoConcepto.substring(0, 22) + '...';
        }
        pdf.text(textoConcepto, x_benef_nombre, y_benef);
        pdf.text(concepto.paisRepatriacion, x_benef_repatriacion, y_benef);
        y_benef += 17;
        count_benef += 1;
        actualizarPosicionBeneficiarios()
    });

    // mascotas
    extractoData.mascotas.forEach((concepto) => {
        pdf.text(concepto.nombre, x_benef_nombre, y_benef);
        pdf.text(concepto.tipo, x_benef_mascota, y_benef);
        y_benef += 17;
        count_benef += 1;
        actualizarPosicionBeneficiarios()
    })

    // pago pse
    pdf.textWithLink('                ', 430, 875, {url:"https://bit.ly/3XBQdEE"});
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

    pdf.save('Formato_Extracto_'+extractoData.numDocumento+'.pdf');
}


// Formato Extracto Masivo
async function generarPDFExtractoMasivo(urlImagen, extractosData) {
    // Cargar imagen una sola vez
    const image = await loadImage(urlImagen);
    
    // Crear un solo PDF
    const pdf = new jsPDF('p', 'pt', 'legal');
    
    const totalExtractos = extractosData.length;
    const progressElement = document.getElementById('progress');
    
    // Iterar sobre cada extracto
    for (let i = 0; i < extractosData.length; i++) {
        const extractoData = extractosData[i];
        
        // Actualizar progreso
        if (progressElement) {
            progressElement.textContent = `${i + 1} de ${totalExtractos} asociados`;
        }
        
        // Si no es el primer extracto, agregar nueva página
        if (i > 0) {
            pdf.addPage('legal', 'portrait');
        }
        
        // Agregar imagen de fondo
        pdf.addImage(image, 'PNG', 0, 0, 613, 1010);
        
        // Generar contenido del extracto (reutilizar lógica)
        generarContenidoExtracto(pdf, extractoData);
        
        console.log(`Extracto ${i + 1}/${totalExtractos} generado: ${extractoData.nombre}`);
    }
    
    // Guardar PDF único con todos los extractos
    const nombreMes = extractosData[0]?.mes || 'Extractos';
    pdf.save(`Extractos_${nombreMes}_${new Date().getTime()}.pdf`);
    
    console.log('PDF masivo generado exitosamente');
}


// Genera el contenido de un extracto en la página actual del PDF
function generarContenidoExtracto(pdf, extractoData) {
    // Globales
    pdf.setFontSize(10);
    pdf.setFont("verdana", "normal");

    // Variables
    const fecha = extractoData.fechaCorte.split("-");
    const fechaFormateada = `${fecha[2]}/${fecha[1]}/${fecha[0]}`;

    // Variable eje y valores variables
    let y = 285;

    // Renglon 1
    pdf.text(extractoData.nombre, 16, 138.5);
    pdf.text(extractoData.numDocumento, 244, 138.5);
    pdf.text(extractoData.mpioResidencia, 339, 138.5);
    pdf.text(fechaFormateada, 486, 138.5);

    // Renglon 2
    pdf.text(extractoData.direccion, 91, 157.8);
    pdf.text(extractoData.numCelular, 486, 157.8);

    // Tabla valores a pagar
    pdf.setFontSize(9);
    let count_detalle = true;

    extractoData.conceptos_detallados.forEach((concepto) => {
        let textoConcepto = concepto.concepto;
        if (textoConcepto.length > 24) {
            textoConcepto = textoConcepto.substring(0, 24) + '...';
        }

        pdf.text(textoConcepto, 17, y);
        if (count_detalle) {
            pdf.text(formatearNumero(extractoData.saldoDiferencia), 245, y);
            count_detalle = false;
        }
        pdf.text(fechaFormateada, 166, y);
        writeText(pdf, concepto.cuotas_vencidas.toString(), 329, y);
        pdf.text(formatearNumero(concepto.cuota_mes), 385, y);
        pdf.text(formatearNumero(concepto.total), 531, y);
        y += 15;
    });

    // Valor total a pagar
    pdf.setTextColor(255, 255, 255);
    pdf.setFont(undefined, "bold");
    pdf.setFontSize(12);
    pdf.text(formatearNumero(extractoData.pagoTotal), 523, 526.7);

    // Observaciones
    pdf.setTextColor(0, 0, 0);
    pdf.setFontSize(10);
    pdf.setFont("verdana", "normal");

    pdf.setFontSize(9);

    // Variables tabla beneficiarios
    let count_benef = 0;
    let x_benef_nombre = 17;
    let x_benef_repatriacion = 161;
    let x_benef_mascota = 245;
    let y_benef = 621.3;
    
    function actualizarPosicionBeneficiarios() {
        if (count_benef === 8) {
            x_benef_nombre = 301;
            x_benef_repatriacion = 452;
            x_benef_mascota = 539;
            y_benef = 621.3;
        }
    }

    // Tabla beneficiarios
    extractoData.beneficiarios.forEach((concepto) => {
        let textoConcepto = concepto.nombre;
        if (textoConcepto.length > 22) {
            textoConcepto = textoConcepto.substring(0, 22) + '...';
        }
        pdf.text(textoConcepto, x_benef_nombre, y_benef);
        pdf.text(concepto.paisRepatriacion, x_benef_repatriacion, y_benef);
        y_benef += 17;
        count_benef += 1;
        actualizarPosicionBeneficiarios();
    });

    // Mascotas
    extractoData.mascotas.forEach((concepto) => {
        pdf.text(concepto.nombre, x_benef_nombre, y_benef);
        pdf.text(concepto.tipo, x_benef_mascota, y_benef);
        y_benef += 17;
        count_benef += 1;
        actualizarPosicionBeneficiarios();
    });

    // Links (PSE, WhatsApp, etc.)
    pdf.textWithLink('                ', 430, 875, {url: "https://bit.ly/3XBQdEE"});
    pdf.textWithLink('                  ', 283, 941, {url: "https://maps.app.goo.gl/VbPt5H2EJ6nTxU6Q6"});
    pdf.textWithLink('                  ', 131, 941, {url: "https://api.whatsapp.com/send/?phone=573135600507"});
    pdf.textWithLink('                  ', 201, 941, {url: "mailto:contacto@coohobienestar.org"});
    pdf.textWithLink('                  ', 443, 941, {url: "https://www.instagram.com/coohobienestar/"});
    pdf.textWithLink('                  ', 364, 941, {url: "https://www.facebook.com/ccoohobienestar/"});
}


// Formato 5
// Formato Solicitud de Crédito
async function generarPDFSolicitudCredito(url, datos) {

    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'legal');
    pdf.addImage(image, 'PNG', 0, 0, 613, 1010);

    // Globales
    pdf.setFontSize(9);
    pdf.setFont("verdana", "normal");

    const coordenadas = {
        tipoPersona : {
            "PERSONA NATURAL": { x: 22.4, y: 142 },
            "PERSONA JURIDICA": { x: 223, y: 142 },
            "ACTUALIZACION": { x: 414.5, y: 142 }
        },
        lineaCredito : {
            "ANTICIPO NOMINA" : { x: 106.5, y: 273.4 },
            "SOLUCION INMEDIATA" : { x: 217.2, y: 273.4 },
            "CREDILIBRE" : { x: 282.5, y: 273.4 },
            "CREDICONTIGO" : { x: 365, y: 273.4 },
            "KUPI" : { x: 282.5, y: 273.4 },
            "CREDISEGURO" : { x: 282.5, y: 273.4 },
            "CREDITO SOAT" : { x: 282.5, y: 273.4 },
        },
        formaDesembolso : {
            "TRANSFERENCIA ELECTRONICA" : { x: 387.8, y: 308 },
            "CHEQUE" : { x: 327.8, y: 308 },
            "CUENTA AHORROS" : { x: 548.5, y: 308 },
        },
        tipoDocumento : {
            "REGISTRO CIVIL": { x: 19.7, y: 426 },
            "TARJETA IDENTIDAD" : { x: 40.4, y: 426 },
            "CEDULA" : { x: 62.4, y: 426 },
            "CEDULA EXTRANJERA" : { x: 82.4, y: 426 },
            "PASAPORTE" : { x: 105.1, y: 426 }
        },
        genero : {
            "FEMENINO": {x: 505.7, y: 472},
            "MASCULINO": {x: 560.4, y: 472},
        },
        estadoCivil : {
            "SOLTERO(A)": {x: 29, y: 500},
            "CASADO(A)": {x: 71.7, y: 500},
            "UNION LIBRE": {x: 115.7, y: 500},
            "SEPARADO(A)": {x: 159, y: 500},
            "DIVORCIADO(A)": {x: 209.7, y: 500},
            "VIUDO(A)": {x: 256, y: 500},
        },
        tipoVivienda : {
            "PROPIA": {x: 291.7, y: 500},
            "FAMILIAR": {x: 345, y: 500},
            "ARRENDADA": {x: 401.7, y: 500},
        },
        estrato : {
            1 : {x: 22.4, y: 529.4},
            2 : {x: 42.4, y: 529.4},
            3 : {x: 63.7, y: 529.4},
            4 : {x: 85.7, y: 529.4},
            5 : {x: 108.4, y: 529.4},
            6 : {x: 130.4, y: 529.4},
        },
        nivelEducativo : {
            "PRIMARIA": {x: 31.7, y: 649.5},
            "SECUNDARIA": {x: 71, y: 649.5},
            "TECNICO": {x: 117.7, y: 649.5},
            "TECNOLOGICO": {x: 174.4, y: 649.5},
            "PREGRADO": {x: 240.4, y: 649.5},
            "ESPECIALIZACION": {x: 304.4, y: 649.5},
            "MAESTRIA": {x: 361.7, y: 649.5},
            "DOCTORADO":{x: 400, y: 649.5},
        },
        ocupacion : {
            "ESTUDIANTE": {x: 40.4, y: 735.3}, 
            "EMPLEADO": {x: 93.7, y: 735.3},
            "PENSIONADO": {x: 147, y: 735.3},
            "INDEPENDIENTE": {x: 223.7, y: 735.3},
            "COMERCIANTE": {x: 305, y: 735.3},
            "HOGAR": {x: 361.7, y: 735.3},
            "CESANTE": {x: 402.4, y: 735.3},
        },
        tipoEmpresa : {
            "PUBLICA": {x: 33, y: 764},
            "PRIVADA": {x: 72.4, y: 764},
            "MIXTA": {x: 118, y: 764},
        },
        tipoContrato: {
            "INDEFINIDO": {x: 292.4, y: 794.7},
            "TERMINO FIJO": {x: 346, y: 794.7},
            "OBRA O LABOR": {x: 401, y: 794.7},
            "PRESTACION SERVICIOS": {x: 469, y: 794.7},
            "HONORARIOS": {x: 551, y: 794.7},
        }
    }

    var nombreCompleto = datos.nombre + ' ' + datos.apellido;
    var nombreCodeudor = (datos.codeudor?.nombre || '') + ' ' + (datos.codeudor?.apellido || '');
    var arrFechaHoy = datos.fechaFormateada.split("/")
    
    // Tipo persona y actualizacion y radicado
    pdf.text(datos.fechaFormateada, 275, 119.8);
    pdf.setFontSize(8);
    pdf.text(datos.numeroRadicado, 401.5, 118.5);
    pdf.setFontSize(9);
    const coordTipoPersona = coordenadas.tipoPersona[datos.tPersona] || coordenadas.tipoPersona["OTRO"];
    writeBoldText(pdf, "X", coordTipoPersona.x, coordTipoPersona.y, 10);

    // Tipo solicitante
    writeBoldText(pdf, "X", 61.5, 181, 10);
    writeBoldText(pdf, "X", 437.5, 181, 10);
    pdf.text(nombreCompleto, 18, 202);
    writeText(pdf, nombreCodeudor, 299.8, 202);

    // Conficiones financieras
    // renglon 1
    const coordLineaCredito = coordenadas.lineaCredito[datos.credito.lineaCredito];
    writeBoldText(pdf, "X", coordLineaCredito.x, coordLineaCredito.y, 10);
    pdf.text(formatearNumero(datos.credito.valor), 408.5, 276.7);
    writeText(pdf, datos.credito.cuotas, 531.1, 276.7);

    // renglon 2
    if (datos.credito.medioPago === "NOMINA" ) {
        writeBoldText(pdf, "X", 266.5, 307.4, 10);
    }else {
        writeBoldText(pdf, "X", 209.8, 307.4, 10);
    }
    const coordFormaDesembolso = coordenadas.formaDesembolso[datos.credito.formaDesembolso];
    writeBoldText(pdf, "X", coordFormaDesembolso.x, coordFormaDesembolso.y, 10);

    // renglon 3
    writeText(pdf, datos.credito.banco, 19.1, 342);
    writeText(pdf, datos.credito.tipoCuenta, 343.8, 342);
    writeText(pdf, datos.credito.numCuenta, 483.8, 342); 

    // Datos personales
    // renglon 1
    pdf.text(datos.nombre, 21.7,398);
    pdf.text(datos.apellido, 325.7, 398);

    // renglon 2
    const coordTipoDocumento = coordenadas.tipoDocumento[datos.tipoDocumento];
    writeBoldText(pdf, "X", coordTipoDocumento.x, coordTipoDocumento.y, 10);
    pdf.text(datos.numDocumento, 177.7, 427.4);
    var arrFechaExp = datos.fechaExpedicion.split("-")
    pdf.text(arrFechaExp[2], 327, 427.4);
    pdf.text(arrFechaExp[1], 358, 427.4);
    pdf.text(arrFechaExp[0], 391, 427.4);
    pdf.text(datos.mpioDoc, 435.7, 427.4);

    // renglon 3
    pdf.text(datos.nacionalidad, 21.7, 472);
    var arrFechaNac = datos.fechaNacimiento.split("-")
    pdf.text(arrFechaNac[2], 159, 472);
    pdf.text(arrFechaNac[1], 195, 472);
    pdf.text(arrFechaNac[0], 239, 472);
    pdf.text(datos.dtoNacimiento, 277, 472);
    pdf.text(datos.mpioNacimiento, 384.5, 472);
    const coordGenero = coordenadas.genero[datos.genero]
    pdf.text("X", coordGenero.x, coordGenero.y);

    // renglon 4
    const coordEstadoCivil = coordenadas.estadoCivil[datos.estadoCivil]
    pdf.text("X", coordEstadoCivil.x, coordEstadoCivil.y);
    const coordTipoVivienda = coordenadas.tipoVivienda[datos.tipoVivienda]
    pdf.text("X", coordTipoVivienda.x, coordTipoVivienda.y);
    if (datos.zonaUbicacion === "RURAL") {
        pdf.text("X", 491, 500);
    } else {
        pdf.text("X", 568, 500);
    }

    // renglon 5
    const coordEstrato = coordenadas.estrato[datos.estrato]
    pdf.text("X", coordEstrato.x, coordEstrato.y);
    if (datos.tAsociado === "COOHOBIENESTAR"){
        pdf.text("X", 187.7, 529.4);
    }else {
        pdf.text("X", 253.7, 529.4);
    }
    pdf.text(String(datos.nPersonasCargo), 325.7, 530.4);
    pdf.text(String(datos.nHijos), 399, 530.4);
    if (datos.cabezaFamilia === "SI"){
        pdf.text("X", 475.7, 530.4);
    } else {
        pdf.text("X", 552, 530.4);
    }

    // renglon 6
    pdf.text(datos.direccion, 21.7, 559);
    pdf.text(datos.barrio, 278.4, 559);
    pdf.text(datos.mpioResidencia, 463, 559);

    // renglon 7
    pdf.text(datos.deptoResidencia, 21.7, 589.5);
    pdf.text(datos.email, 125.7, 589.5);
    writeText(pdf, datos.numResidencia, 385, 589.5);
    pdf.text(datos.numCelular, 492.4, 589.5);

    // renglon 8
    if (datos.envioInfoCorreo){
        pdf.text("X", 105.7, 618.1);
    }
    if (datos.envioInfoMensaje){
        pdf.text("X", 226.4, 618.1);
    }
    if (datos.envioInfoWhatsapp){
        pdf.text("X", 329, 618.1);
    }

    // renglon 9
    const coordNivelEducativo = coordenadas.nivelEducativo[datos.nivelEducativo];
    pdf.text("X", coordNivelEducativo.x, coordNivelEducativo.y);

    // renglon 10
    writeText(pdf, datos.tituloPregrado, 21.7, 679.6);
    writeText(pdf, datos.tituloPosgrado, 322, 679.6);

    // Informacion laboral
    // renglon 1
    if (datos.ocupacion === "OTRO"){
        writeText(pdf, datos.ocupacionEspecifica || "", 463, 735.2);
    }else if (datos.ocupacion && coordenadas.ocupacion[datos.ocupacion] ){
        const coordOcupacion = coordenadas.ocupacion[datos.ocupacion];
        pdf.text("X", coordOcupacion.x, coordOcupacion.y);
    }

    // renglon 2
    if (datos.tipoEmpresa === "OTRO"){
        writeText(pdf, datos.tipoEmpresaEspecifica || "", 180.4, 764.6);
    } else if(datos.tipoEmpresa && coordenadas.tipoEmpresa[datos.tipoEmpresa]){
        const coordTipoEmpresa = coordenadas.tipoEmpresa[datos.tipoEmpresa];
        pdf.text("X", coordTipoEmpresa.x, coordTipoEmpresa.y);
    }
    writeText(pdf, datos.nombreEmpresa, 324.4, 765.9);

    // renglon 3
    writeText(pdf, datos.cargo, 21.7, 795.6);
    if (datos.tipoContrato && coordenadas.tipoContrato[datos.tipoContrato]){
        const coordTipoContrato = coordenadas.tipoContrato[datos.tipoContrato];
        pdf.text("X", coordTipoContrato.x, coordTipoContrato.y);
    }

    // renglon 4
    if (datos.fechaInicio){
        var arrFechaInicio = datos.fechaInicio.split("-")
        pdf.text(arrFechaInicio[2], 19.7, 830.6);
        pdf.text(arrFechaInicio[1], 39, 830.6);
        pdf.text(arrFechaInicio[0], 69, 830.6);
    }
    if (datos.fechaTerminacion){
        var arrFechaTerminacion = datos.fechaTerminacion.split("-")
        pdf.text(arrFechaTerminacion[2], 104.4, 830.6);
        pdf.text(arrFechaTerminacion[1], 127, 830.6);
        pdf.text(arrFechaTerminacion[0], 157, 830.6);
    }
    writeText(pdf, datos.nomRepresenLegal, 189, 830.6);
    writeText(pdf, datos.numDocRL, 461, 830.6);

    // renglon 5
    writeText(pdf, datos.nomJefeInmediato, 21.7, 861.2);
    writeText(pdf, datos.telefonoJefeInmediato, 279.7, 861.2);
    writeText(pdf, datos.direccionLaboral, 385.2, 861.2);

    // renglon 6
    writeText(pdf, datos.municipioLaboral, 21.7, 890);
    writeText(pdf, datos.dptoLaboral, 149.7, 890);
    writeText(pdf, datos.telefonoLaboral, 291.7, 890);
    writeText(pdf, datos.correoLaboral, 387, 890);

    // renglon 7
    if (datos.admRP === "SI"){
        pdf.text("X", 53, 923.9);
    } else {
        pdf.text("X", 102.4, 923.9);
    }
    if (datos.pep === "SI"){
        pdf.text("X", 191.7, 923.9);
    } else {
        pdf.text("X", 260.4, 923.9);
    }
    writeText(pdf, datos.activEcono, 323, 923.9);
    writeText(pdf, datos.ciiu, 552, 923.9);

    // renglon 8
    if (datos.declaraRenta === "SI"){
        pdf.text("X", 53, 952);
    } else {
        pdf.text("X", 102.4, 952);
    }
    if (datos.responsableIVA === "SI"){
        pdf.text("X", 191.7, 952);
    } else {
        pdf.text("X", 260.4, 952);
    }
    writeText(pdf, datos.regimenTributario, 323, 954.6);

    // Se añade Pagina 2 al documento
    pdf.addPage();
    const image2 = await loadImage('/static/img/Solicitud_Credito_2025_page_0002.jpg');
    pdf.addImage(image2, 'PNG', 0, 0, 613, 1010);

    // Referencia personal
    pdf.text(datos.nombreRF, 19.8, 130.7);
    pdf.text(datos.parentesco, 237.1, 130.7);
    pdf.text(datos.numContacto, 394.5, 130.7);

    // Informacion ingresos y egresos
    writeText(pdf, formatearMoneda(datos.ingrSalario), 193.7, 206);
    writeText(pdf, formatearMoneda(datos.ingrHorasExtras), 193.7, 219.4);
    writeText(pdf, formatearMoneda(datos.ingrPension), 193.7, 232.7);
    writeText(pdf, formatearMoneda(datos.ingrCompensacion), 193.7, 244.7);
    writeText(pdf, formatearMoneda(datos.ingrHonorarios), 193.7, 259.6);
    writeText(pdf, formatearMoneda(datos.ingrVentas), 193.7, 270.7);
    writeText(pdf, formatearMoneda(datos.ingrIntereses), 193.7, 284);
    writeText(pdf, formatearMoneda(datos.ingrGiros), 193.7, 297.4);
    writeText(pdf, formatearMoneda(datos.ingrArrendamientos), 193.7, 311.4);
    writeText(pdf, formatearMoneda(datos.ingrOtros), 193.7, 323.4);
    writeText(pdf, datos.ingrDescripcionOtros, 139, 338);

    writeText(pdf, formatearMoneda(datos.egrArrendamiento), 469, 206);
    writeText(pdf, formatearMoneda(datos.egrServiciosPublicos), 469, 219.4);
    writeText(pdf, formatearMoneda(datos.egrAportesSalud), 469, 232.7);
    writeText(pdf, formatearMoneda(datos.egrTransporte), 469, 244.7);
    writeText(pdf, formatearMoneda(datos.egrAlimentacion), 469, 259.6);
    writeText(pdf, formatearMoneda(datos.egrObligaciones), 469, 270.7);
    writeText(pdf, formatearMoneda(datos.egrTarjetas), 469, 284);
    writeText(pdf, formatearMoneda(datos.egrCostos), 469, 297.4);
    writeText(pdf, formatearMoneda(datos.egrEmbargos), 469, 311.4);
    writeText(pdf, formatearMoneda(datos.egrOtros), 469, 323.4);
    writeText(pdf, datos.egrDescripcionOtros, 399, 338);

    pdf.setFont("verdana", "bold");
    pdf.setTextColor(255, 255, 255);
    writeText(pdf, formatearMoneda(datos.total_ingresos), 195, 364.6);
    writeText(pdf, formatearMoneda(datos.total_egresos), 470.4, 364.6);

    pdf.setFont("verdana", "normal");
    pdf.setTextColor(0, 0, 0);
    writeText(pdf, formatearMoneda(datos.total_ingresos), 307.7, 377);
    writeText(pdf, formatearMoneda(datos.total_egresos), 307.7, 390.4);
    writeText(pdf, formatearMoneda(datos.total_patrimonio), 307.7, 403);

    // renglon 1
    writeText(pdf, nombreCompleto, 21.7, 446.7);
    writeText(pdf, datos.numDocumento, 239, 446.7);
    pdf.text(arrFechaHoy[0], 342, 446.7);
    pdf.text(arrFechaHoy[1], 399.4, 446.7);
    pdf.text(arrFechaHoy[2], 450, 446.7);
    if (datos.declaraRenta){
        pdf.text("X", 511.9, 445.7);
    }else {
        pdf.text("X", 564.9, 445.7);
    }

    // Operacion en moneda extranjera
    // renglon 1
    if (datos.operacionesMonedaExtranjera === "SI"){
        pdf.text("X", 78.4, 506.7);
        writeText(pdf, datos.operacionesMonedaCuales, 221, 508.7);

        // renglon 2
        writeText(pdf, datos.operacionesMonedaTipo, 21.7, 541.4);
        writeText(pdf, "$" + formatearMoneda(datos.operacionesMonedaMonto), 222.4, 541.4);
        writeText(pdf, datos.operacionesMoneda, 410.4, 541.4);
    } else {
        pdf.text("X", 179, 506.7);
    }

    // renglon 3
    if (datos.poseeCuentasMonedaExtranjera === "SI"){
        pdf.text("X", 78.4, 572.7);
        writeText(pdf, datos.poseeCuentasBanco, 221, 574);
        writeText(pdf, datos.poseeCuentasCuenta, 411, 574);
    
        // renglon 4
        writeText(pdf, datos.poseeCuentasMoneda, 21.7, 607.4);
        writeText(pdf, datos.poseeCuentasCiudad, 221, 607.4);
        writeText(pdf, datos.poseeCuentasPais, 411, 607.4);
    } else {
        pdf.text("X", 179, 572.7);
    }

    // Firma
    pdf.text(nombreCompleto, 150, 702);
    pdf.text(datos.numDocumento, 150, 728);

    // Autorizacion de descuento por nomina
    if (datos.autorizaciondcto){
        pdf.text(nombreCompleto, 42.4, 876.7);
        pdf.text(datos.numDocumento, 23.7, 886);
        pdf.text(datos.mpioDoc, 183, 886);
    }

    // /////////////////////////////////////////////////////////////////////////////////////////
    // Se añade Pagina 3 al documento
    pdf.addPage();
    const image3 = await loadImage('/static/img/Solicitud_Credito_2025_page_0003.jpg');
    pdf.addImage(image3, 'PNG', 0, 0, 613, 1010);

    //firma y huella
    console.log(arrFechaHoy[2]);
    pdf.text(convertirDias(arrFechaHoy[0]), 291.8, 355);
    pdf.text(convertirMes(arrFechaHoy[1]), 470.5, 355);
    pdf.text(arrFechaHoy[2], 17.8, 366.7);
    pdf.text('ARMENIA', 148.7, 366.7); 

    // deudor
    pdf.text(nombreCompleto, 78, 434.7);
    pdf.text(datos.numDocumento, 88.5, 448);
    pdf.text(datos.mpioDoc, 88.5, 461.4);
    // codeudor
    pdf.text(nombreCodeudor, 347, 434.7);
    pdf.text(datos.codeudor?.numDocumento || '', 355, 448);
    pdf.text(datos.codeudor?.mpioDoc__nombre || '', 355, 461.4);

    pdf.save('Formato_Solicitud_Credito_'+datos.numDocumento+'.pdf');
}


// Formato 6
// Formato Pagare Persona Natural
async function generarPDFPagare(url) {

    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'letter');
    pdf.addImage(image, 'PNG', 0, 0, 612, 792);

    /////////////////////////////////////////////////////////////////////////////////////////
    // Se añade Pagina 2 al documento
    pdf.addPage();
    const image2 = await loadImage('/static/img/PagarePersonaNatural_2025_page_0002.jpg');
    pdf.addImage(image2, 'PNG', 0, 0, 612, 792);

    /////////////////////////////////////////////////////////////////////////////////////////
    // Se añade Pagina 3 al documento
    pdf.addPage();
    const image3 = await loadImage('/static/img/PagarePersonaNatural_2025_page_0003.jpg');
    pdf.addImage(image3, 'PNG', 0, 0, 612, 792);

    /////////////////////////////////////////////////////////////////////////////////////////
    // Se añade Pagina 4 al documento
    pdf.addPage();
    const image4 = await loadImage('/static/img/PagarePersonaNatural_2025_page_0004.jpg');
    pdf.addImage(image4, 'PNG', 0, 0, 612, 792);

    /////////////////////////////////////////////////////////////////////////////////////////
    // Se añade Pagina 5 al documento
    pdf.addPage();
    const image5 = await loadImage('/static/img/PagarePersonaNatural_2025_page_0005.jpg');
    pdf.addImage(image5, 'PNG', 0, 0, 612, 792);

    pdf.save('Pagare_Persona_Natural.pdf');
}


// Formato 7
// Formato Otorgamiento de Credito
async function generarPDFOtorgamientoCredito(url, datos) {
    
    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'legal');
    pdf.addImage(image, 'PNG', 0, 0, 613, 1010);

    // Globales
    pdf.setFontSize(9);
    pdf.setFont("verdana", "normal");

    // Encabezados
    pdf.text(datos.fechaFormateada, 275.8, 119.4);
    pdf.setFontSize(8);
    pdf.text(datos.numeroRadicado, 401.1, 118);
    pdf.setFontSize(9);

    // variables
    let fecha = datos.credito.fechaSolicitud.split("-");
    let tasa = parseFloat(datos.credito.tasaInteres__porcentaje);
    let tasaPorcentaje = (tasa * 100).toFixed(2);

    // Deudores
    let nombreCompleto = datos.nombre + " " + datos.apellido
    let nombreCodeudor = (datos.codeudor?.nombre || '') + " " + (datos.codeudor?.apellido || '')

    // tabla deudores
    // deudor
    pdf.text(nombreCompleto, 19, 287.4);
    pdf.text(datos.tipoDocumento, 304, 287.4);
    pdf.text(String(datos.numDocumento), 407.1, 287.4);
    pdf.text(datos.mpioDoc, 491.1, 287.4);
    // codeudor
    pdf.text(nombreCodeudor, 19, 303.4);
    pdf.text(datos.codeudor?.tipoDocumento || '', 304, 303.4);
    pdf.text(String(datos.codeudor?.numDocumento || ''), 407.1, 303.4);
    pdf.text(datos.codeudor?.mpioDoc__nombre || '', 491.1, 303.4);

    // renglon 1
    pdf.text(convertirDias(fecha[2]), 133.1, 401.4);
    pdf.text(convertirMes(fecha[1]), 301.1, 401.4);

    // renglon 2
    pdf.text(numeroALetras(datos.credito.valor), 18.5, 412.6);
    pdf.text(formatearNumero(datos.credito.valor), 249, 412.6);

    // renglon 3
    pdf.text(tasaPorcentaje+'%', 117.8, 436);
    pdf.text(String(datos.credito.cuotas), 323.8, 436);

    // renglon 4
    console.log(datos.credito.fechaSolicitud);
    pdf.text(formatearFechaTexto(datos.credito.fechaPrimerCobro), 49.1, 448);
    pdf.text(formatearFechaTexto(datos.credito.fechaPrimerCobro, datos.credito.cuotas - 1), 323.1, 448);
    
    // renglon 5
    pdf.text(formatearNumero(datos.credito.valorCuota), 18.5, 459);
    pdf.text(datos.credito.lineaCredito, 273.1, 459);

    // renglon 6
    pdf.text(formatearNumero(datos.credito.totalCredito), 18.5, 471);
    pdf.text(datos.credito.medioPago, 246.5, 471);

    // Constancia
    pdf.text(convertirDias(fecha[2]), 18.5, 533.4);
    pdf.text(convertirMes(fecha[1]), 243.1, 533.4);
    pdf.text(fecha[0], 439.8, 533.4);
    pdf.text('ARMENIA', 18.5, 545);   

    // firmas deudores
    pdf.text(nombreCompleto, 169, 660);
    pdf.text(String(datos.numDocumento), 169, 685.4);
    pdf.text(datos.mpioDoc, 169, 712);
    pdf.text(nombreCodeudor, 169, 806.7);
    pdf.text(String(datos.codeudor?.numDocumento || ''), 169, 832.7);
    pdf.text(datos.codeudor?.mpioDoc__nombre || '', 169, 858.7);

    pdf.save('Otorgamiento_Credito_'+datos.numDocumento+'.pdf');
}


// Formato 8
// Formato Tabla de Amortización
async function generarPDFTablaAmortizacion(url, datos) {
    console.log(datos);

    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'legal');
    pdf.addImage(image, 'PNG', 0, 0, 613, 1010);

    // Globales
    pdf.setFontSize(9);
    pdf.setFont("verdana", "normal");

    // variables
    const fechaSolicitudCredito = datos.credito.fechaSolicitud;
    const fechaPrimerCobro = datos.credito.fechaPrimerCobro;

    const fechaArray = fechaSolicitudCredito.split("-");
    const tasa = parseFloat(datos.credito.tasaInteres__porcentaje);
    const tasaPorcentaje = (tasa * 100).toFixed(2);
    
    // Deudores
    let nombreCompleto = datos.nombre + " " + datos.apellido
    let nombreCodeudor = (datos.codeudor?.nombre || '') + ' ' + (datos.codeudor?.apellido || '')

    // Encabezados
    pdf.text(datos.fechaFormateada, 270.5, 120);
    pdf.setFontSize(8);
    pdf.text(datos.numeroRadicado, 401.8, 122);
    pdf.setFontSize(9);

    // tabla deudores
    // deudor
    pdf.text(nombreCompleto, 19, 166);
    pdf.text(datos.tipoDocumento, 304, 166);
    pdf.text(String(datos.numDocumento), 407.1, 166);
    pdf.text(datos.mpioDoc, 491.1, 166);
    // codeudor
    pdf.text(nombreCodeudor, 19, 182);
    pdf.text(datos.codeudor?.tipoDocumento || '', 304, 182);
    pdf.text(String(datos.codeudor?.numDocumento || ''), 407.1, 182);
    pdf.text(datos.codeudor?.mpioDoc__nombre || '', 491.1, 182);

    //tabla informacion
    pdf.text(formatearFechaTexto(datos.credito.fechaSolicitud), 281.1, 252.7);
    pdf.text(datos.credito.lineaCredito, 281.1, 268);
    pdf.text(datos.credito.amortizacion, 281.1, 282);
    pdf.text(formatearNumeroSinSimbolo(datos.credito.valor), 307.1, 295.4);
    pdf.text(String(datos.credito.cuotas), 281.1, 311);
    pdf.text(tasaPorcentaje, 411, 324.4);
    pdf.text(formatearFechaTexto(datos.credito.fechaPrimerCobro, datos.credito.cuotas - 1), 281.1, 340);

    // variables de inicializacion tabla de amortizacion
    const valorNumerica = parseFloat(datos.credito.valor);
    const cuotasNumerica = parseInt(datos.credito.cuotas);
    const tasaNumerica = parseFloat(datos.credito.tasaInteres__porcentaje);

    //Calcular cuota fija
    let cuotaFija;
    if (tasaNumerica === 0) {
        cuotaFija = Math.ceil(valorNumerica / cuotasNumerica);
    } else {
        cuotaFija = (
            (valorNumerica * tasaNumerica * Math.pow(1 + tasaNumerica, cuotasNumerica)) /
            (Math.pow(1 + tasaNumerica, cuotasNumerica) - 1)
        ).toFixed(0);
    }

    // Generar fechas
    
    const fechas = generarFechas(cuotasNumerica, fechaPrimerCobro);

    // Tabla de amortización
    let saldoRestante = valorNumerica;
    let fila = 390.7;

    for (let i = 0; i <= cuotasNumerica; i++) {
        if (i === 0) {
            // Fila inicial (sin pago)
            // pdf.text(String(i), 81, fila);
            writeTextSize(pdf, formatearFecha(fechaSolicitudCredito), 58.2, fila, 8);
            pdf.text(formatearNumero(saldoRestante), 119.5, fila);
            pdf.text(formatearMoneda(0), 208.1, fila);
            pdf.text(formatearMoneda(0), 293.2, fila);
            pdf.text(formatearMoneda(0), 375.1, fila);
            pdf.text(formatearMoneda(0), 427.1, fila);
            pdf.text(formatearMoneda(0), 467.5, fila);
            pdf.text(formatearNumero(saldoRestante), 528.1, fila);
        } else {
            // Cálculos por cuota
            const intereses = (saldoRestante * tasaNumerica).toFixed(0);
            const abonoCapital = (cuotaFija - intereses).toFixed(0);

            // Última cuota: saldo 0
            if (i === cuotasNumerica) {
                saldoRestante = 0;
            } else {
                saldoRestante = (saldoRestante - abonoCapital).toFixed(0);
            }

            // Pintar fila
            // pdf.text(String(i), 81, fila);
            writeTextSize(pdf, fechas[i-1], 58.2, fila, 8);
            pdf.text(formatearNumero(parseFloat(saldoRestante) + parseFloat(abonoCapital)), 119.5, fila);
            pdf.text(formatearNumero(abonoCapital), 208.1, fila);
            pdf.text(formatearNumero(intereses), 293.2, fila);
            pdf.text(formatearMoneda(0), 375.1, fila);
            pdf.text(formatearMoneda(0), 427.1, fila);
            pdf.text(formatearNumero(cuotaFija), 467.5, fila);
            pdf.text(formatearNumero(saldoRestante), 528.1, fila);
        }
        fila += 16.4;
    }

    // Constancia
    pdf.text(convertirDias(fechaArray[2]), 480, 612);
    pdf.text(convertirMes(fechaArray[1]), 57.8, 623.4);
    pdf.text(fechaArray[0], 205, 623.4);
    pdf.text('ARMENIA', 330.5, 623.4); 

    // firmas deudores
    pdf.text(nombreCompleto, 159, 718);
    pdf.text(String(datos.numDocumento), 159, 744);
    pdf.text(datos.mpioDoc, 159, 770);
    pdf.text(nombreCodeudor, 159, 862);
    pdf.text(String(datos.codeudor?.numDocumento || ''), 159, 888);
    pdf.text(datos.codeudor?.mpioDoc__nombre || '', 159, 914);

    pdf.save('Tabla_Amortizacion_'+datos.numDocumento+'.pdf');
}


// Formato 9
// Formato Retiro de Asociado
async function generarPDFRetiroAsociado(url, datos) {

    const image = await loadImage(url);
    const pdf = new jsPDF('p', 'pt', 'legal');
    pdf.addImage(image, 'PNG', 0, 0, 613, 1010);

    // Globales
    pdf.setFontSize(9);
    pdf.setFont("verdana", "normal");

    // Variables
    var nombreCompleto = datos.nombre + ' ' + datos.apellido
    var arrFechaHoy = datos.fechaFormateada.split('/')
    
    // Encabezados
    pdf.text(datos.fechaFormateada, 268, 120);
    writeTextSize(pdf, datos.numeroRadicado, 459.5, 119.4, 8);

    // Texto
    pdf.text(nombreCompleto, 38.5, 264);
    pdf.text(datos.numDocumento, 71.8, 274.7);
    pdf.text(datos.mpioDoc, 291.8, 274.7);
    pdf.text(datos.mpioResidencia, 17.1, 285.4);
    
    // Constancia
    pdf.text(convertirDias(arrFechaHoy[0]), 448.5, 594);
    pdf.text(convertirMes(arrFechaHoy[1]), 21.8, 605.4);
    pdf.text(arrFechaHoy[2], 172.5, 605.4);
    pdf.text('ARMENIA', 294.5, 605.4)

    // Firmas
    pdf.text(nombreCompleto, 149.1, 682.7);
    pdf.text(datos.numDocumento, 149.1, 706.7);
    pdf.text(datos.numCelular, 149.1, 729.4);
    pdf.text(datos.email, 195.1, 752);

    pdf.save('Formato_Retiro_Asociado.pdf');
}


// Formato Texto Plano
async function generarTxtMasivo(extractosData) {
    // Encabezados del CSV
    const encabezados = [
        "Cédula",
        "Nombre",
        "Municipio",
        "Dirección",
        "Celular",
        "Mes",
        "Cuota Periódica",
        "Cuota Coohop",
        "Valor Vencido",
        "Saldo",
        "Pago Total"
    ].join(',');
    
    // Construir líneas de datos para TODOS los extractos
    const lineas = extractosData.map(extractoData => {
        return [
            extractoData.numDocumento || '',
            `"${extractoData.nombre}"`,
            `"${extractoData.mpioResidencia}"`,
            `"${extractoData.direccion}"`,
            extractoData.numCelular || '',
            `"${extractoData.mes}"`,
            extractoData.cuotaPeriodica || 0,
            extractoData.cuotaCoohop || 0,
            extractoData.valorVencido || 0,
            extractoData.saldo || 0,
            extractoData.pagoTotal || 0
        ].join(',');
    });
    
    // Unir encabezados y todas las líneas
    const texto = `${encabezados}\n${lineas.join('\n')}`;
    
    // Crear un Blob con el contenido
    const blob = new Blob([texto], { type: "text/plain;charset=utf-8" });
    
    // Crear un enlace temporal para la descarga
    const enlace = document.createElement("a");
    enlace.href = URL.createObjectURL(blob);
    const nombreMes = extractosData[0]?.mes || 'Extractos';
    enlace.download = `Extractos_${nombreMes}_${new Date().getTime()}.txt`;
    
    // Simular un clic para descargar el archivo
    enlace.click();
    
    // Limpiar el URL Object creado
    URL.revokeObjectURL(enlace.href);
    
    console.log('TXT masivo generado exitosamente');
}