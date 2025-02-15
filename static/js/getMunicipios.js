// Función para cargar los municipios en el select de Municipios
$(document).ready(function() {
    function cargarMunicipios(departamento_id, municipioSelect, municipioSeleccionado = null) {
        if (departamento_id) {
            $.ajax({
                url: '/departamento/getMunicipios/' + departamento_id + '/',
                method: 'GET',
                success: function(data) {
                    municipioSelect.empty(); // Vaciar el select de municipios
                    municipioSelect.append('<option value="">Seleccione un municipio</option>');

                    $.each(data, function(index, municipio) {
                        let selected = municipio.id == municipioSeleccionado ? 'selected' : '';
                        municipioSelect.append('<option value="' + municipio.id + '" ' + selected + '>' + municipio.nombre + '</option>');
                    });
                },
                error: function() {
                    alert("Error al cargar los municipios.");
                }
            });
        } else {
            municipioSelect.empty();
            municipioSelect.append('<option value="">Seleccione un municipio</option>');
        }
    }

    // Al cambiar el departamento, actualizar los municipios
    $('.departamento-select').change(function() {
        var departamento_id = $(this).val();
        var municipioSelect = $($(this).data('target'));
        cargarMunicipios(departamento_id, municipioSelect);
    });

    // Cargar municipios al iniciar la página si ya hay un departamento seleccionado
    var departamentoInicial = $('#id_dtoNacimiento').val();
    var municipioSelect = $('#id_mpioNacimiento');
    var municipioInicial = municipioSelect.val(); // Obtener el municipio que estaba seleccionado

    var departamentoInicial2 = $('#id_deptoResidencia').val();
    var municipioSelect2 = $('#id_mpioResidencia');
    var municipioInicial2 = municipioSelect2.val(); // Obtener el municipio que estaba seleccionado

    var departamentoInicial3 = $('#id_dptoTrabajo').val();
    var municipioSelect3 = $('#id_mpioTrabajo');
    var municipioInicial3 = municipioSelect3.val(); // Obtener el municipio que estaba seleccionado
    
    if (departamentoInicial) {
        cargarMunicipios(departamentoInicial, municipioSelect, municipioInicial);
        cargarMunicipios(departamentoInicial2, municipioSelect2, municipioInicial2);
        cargarMunicipios(departamentoInicial3, municipioSelect3, municipioInicial3);
    }

});

// Función para cargar los municipios con departamento en el input de municipio del documento
$(document).ready(function() {
    $("#id_mpioDoc").select2({
        theme: "bootstrap-5",
        placeholder: "Escriba para buscar un municipio",
        width: '100%',
        selectionCssClass: "form-control",
        ajax: {
            url: "/departamento/buscar-municipios/",  // La API que creamos en Django
            dataType: "json",
            delay: 250,
            data: function(params) {
                return { q: params.term };  // Envía el término de búsqueda
            },
            processResults: function(data) {
                return {
                    results: data.map(mcpio => ({
                        id: mcpio.id,
                        text: `${mcpio.nombre} - ${mcpio.departamento__nombre}`
                    }))
                };
            }
        },
        minimumInputLength: 2  // Espera hasta que el usuario escriba 2 caracteres
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const paisSeleccionado = document.getElementById("id_indicativo").getAttribute("data-pais-seleccionado");

    fetch("/departamento/obtener_paises/")
        .then(response => response.json())
        .then(data => {
            let select = document.getElementById("id_indicativo");
            select.innerHTML = ""; // Vaciar el select antes de llenarlo

            // SE Modifica la forma en que agregas las opciones en el select
            data.forEach(pais => {
                let option = document.createElement("option");
                option.value = pais.id;
                option.textContent = `${pais.nombre} (${pais.indicativo})`;
                option.setAttribute('data-img', pais.bandera);

                // Si el país es el seleccionado, se marca como "selected"
                if (pais.id == paisSeleccionado) {
                    option.selected = true;
                }

                select.appendChild(option);
            });

            // Inicializar Select2 después de llenar las opciones
            $(select).select2({
                templateResult: formatState,
                templateSelection: formatState
            });
        })
        .catch(error => console.error("Error cargando países:", error));

    // Función para dar formato a las opciones con la bandera y el texto
    function formatState(state) {
        if (!state.id) {
            return state.text; // Si no es un valor válido, solo mostrar el texto
        }

        var $state = $(
            `<span><img src="${$(state.element).data('img')}" width="30" height="20"> ${state.text}</span>`
        );
        return $state;
    }
});