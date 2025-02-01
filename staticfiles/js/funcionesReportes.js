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