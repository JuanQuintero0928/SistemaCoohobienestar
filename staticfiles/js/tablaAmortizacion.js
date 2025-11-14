function generarTablaAmortizacion(saldoInicial, tasaMensual, numCuotas, fechaSolicitud, fechaPrimerPago, tipo) {
    const tablaBody = document.querySelector("#tablaAmortizacion tbody");
    tablaBody.innerHTML = ""; // Limpiar tabla

    const fechas = generarFechas(numCuotas, fechaPrimerPago);
    let saldoRestante = saldoInicial;

    let cuotaFija;
    if (tasaMensual === 0) {
        cuotaFija = Math.ceil(saldoInicial / numCuotas);
    } else {
        cuotaFija = ((saldoInicial * tasaMensual * Math.pow(1 + tasaMensual, numCuotas)) / 
                    (Math.pow(1 + tasaMensual, numCuotas) - 1)).toFixed(0);
    }

    // Asignar valores a los campos ocultos
    document.getElementById("id_valorCuota").value = cuotaFija;
    document.getElementById("id_totalCredito").value = cuotaFija * numCuotas;

    for (let i = 0; i <= numCuotas; i++) {
        const fila = document.createElement("tr");

        if (i === 0) {
            fila.innerHTML = `
                <td>${i}</td>
                <td>${formatearFecha(fechaSolicitud)}</td>
                <td>${formatearMoneda(saldoRestante)}</td>
                <td>${formatearMoneda(0)}</td>
                <td>${formatearMoneda(0)}</td>
                <td>${formatearMoneda(cuotaFija)}</td>
                <td>${formatearMoneda(saldoRestante)}</td>
            `;
        } else {
            let abonoCapital, intereses;

            if (tasaMensual === 0) {
                intereses = 0;
                abonoCapital = cuotaFija;
            } else {
                intereses = (saldoRestante * tasaMensual).toFixed(0);
                abonoCapital = (cuotaFija - intereses).toFixed(0);
            }

            if (i === numCuotas) {
                saldoRestante = 0;
            } else {
                saldoRestante = (saldoRestante - abonoCapital).toFixed(0);
            }

            fila.innerHTML = `
                <td>${i}</td>
                <td>${fechas[i-1]}</td>
                <td>${formatearMoneda(parseFloat(saldoRestante) + parseFloat(abonoCapital))}</td>
                <td>${formatearMoneda(abonoCapital)}</td>
                <td>${formatearMoneda(intereses)}</td>
                <td>${formatearMoneda(cuotaFija)}</td>
                <td>${formatearMoneda(saldoRestante)}</td>
            `;
        }

        tablaBody.appendChild(fila);
    }
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


function calcularCapacidadEndeudamiento(pkAsociado) {
    fetch(`/api/obtener_total_tarifa/${pkAsociado}/`)
        .then(responde => responde.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                return;
            }
            let totalTarifa = data.total // Valor obtenido del API
            const ingresoPrincipal = parseFloat(document.getElementById("ingresosActPrin").value) || 0;
            const otroIngreso1 = parseFloat(document.getElementById("otroIngreso1").value) || 0;
            const otroIngreso2 = parseFloat(document.getElementById("otroIngreso2").value) || 0;
            const egresos = parseFloat(document.getElementById("egresos").value) || 0;
            let valorCuota = document.getElementById("id_valorCuota").value;
            
            let ingresosTotales = ingresoPrincipal + otroIngreso1 + otroIngreso2;
            let capacidadPago = ingresosTotales - egresos - totalTarifa;
            
            divAnalisis = document.getElementById("divAnalisis").classList.remove("d-none");
            divCapacidadPago = document.getElementById("divCapacidadPago").classList.remove("d-none");
            
            let inputAnalisis = document.getElementById("analisisCodeudor");
            let inputCapacidadPago = document.getElementById("analisisCapacidadPago");
            
            if ((ingresosTotales * 0.5) > valorCuota) {
                inputAnalisis.value = "Con capacidad de endeudamiento";
                inputAnalisis.style.color = "white";
                inputAnalisis.style.fontWeight = "bold";
                inputAnalisis.style.backgroundColor = "#6EB942";
            } else {
                inputAnalisis.value = "Sin capacidad de endeudamiento";
                inputAnalisis.style.color = "white";
                inputAnalisis.style.fontWeight = "bold";
                inputAnalisis.style.backgroundColor = "#F87171";
            }
            if (capacidadPago > valorCuota) {
                inputCapacidadPago.value = "Con capacidad de pago";
                inputCapacidadPago.style.color = "white";
                inputCapacidadPago.style.fontWeight = "bold";
                inputCapacidadPago.style.backgroundColor = "#6EB942";
            } else {
                inputCapacidadPago.value = "Sin capacidad de pago";
                inputCapacidadPago.style.color = "white";
                inputCapacidadPago.style.fontWeight = "bold";
                inputCapacidadPago.style.backgroundColor = "#F87171";
            }
        })
        .catch(error => { console.log("Error al obtener la tarifa", error); });
}


function formatearFecha(fecha) {
    const [y, m, d] = fecha.split("-");
    return `${d}/${m}/${y}`;
}