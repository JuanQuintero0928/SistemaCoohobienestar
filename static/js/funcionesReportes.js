function descargarExcel() {
    let fechaInicial = document.getElementById('id_fechaInicial').value;
    let fechaFinal = document.getElementById('id_fechaFinal').value;
    let urlBase = document.getElementById('id_descargarExcel').getAttribute('data-url');

    if (fechaInicial && fechaFinal) {
        let url = `${urlBase}?fechaInicial=${fechaInicial}&fechaFinal=${fechaFinal}`;
        window.location.href = url;
    } else {
        alert("Por favor, seleccione ambas fechas.");
    }
}

function descargarExcel2() {
    let fechaInicial = document.getElementById('id_fechaInicial').value;
    let fechaFinal = document.getElementById('id_fechaFinal').value;
    let banco = document.getElementById('id_banco').value;
    let urlBase = document.getElementById('id_descargarExcel').getAttribute('data-url');

    if (fechaInicial && fechaFinal) {
        let url = `${urlBase}?fechaInicial=${fechaInicial}&fechaFinal=${fechaFinal}&banco=${banco}`;
        window.location.href = url;
    } else {
        alert("Por favor, seleccione ambas fechas.");
    }
}