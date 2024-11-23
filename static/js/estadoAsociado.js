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