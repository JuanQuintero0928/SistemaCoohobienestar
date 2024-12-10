document.addEventListener('DOMContentLoaded', event => {
    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        // Inicializar DataTable
        const table = new simpleDatatables.DataTable(datatablesSimple, {
            labels: {
                placeholder: "Buscar...", // Placeholder del cuadro de búsqueda
                perPage: "registros por página", // Selector de registros por página
                noRows: "No se encontraron registros", // Texto cuando no hay registros
                info: "Mostrando {start} a {end} de {rows} registros", // Información sobre la paginación
            },
        });

        // Esperar a que la tabla esté completamente cargada
        table.on('datatable.init', function () {
            // console.log('La tabla ha sido completamente inicializada.');

            // Obtener el input de búsqueda
            const searchInput = document.querySelector('.datatable-input');
            if (searchInput) {
                searchInput.addEventListener('input', function () {
                    const searchValue = searchInput.value.toLowerCase().trim(); // Cadena de búsqueda
                    console.log('Buscando:', searchValue);
                    // Filtrar filas de la tabla
                    table.search(searchValue); // Utilizar la función de búsqueda del DataTable
                });
            } else {
                // console.warn('No se encontró el input de búsqueda.');
            }
        });
    } else {
        // console.warn('No se encontró la tabla con ID "datatablesSimple".');
    }
});
