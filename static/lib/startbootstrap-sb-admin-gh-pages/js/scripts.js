/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {
    // Recuperamos el estado del sidebar
    const isSidebarToggled = localStorage.getItem('sb|sidebar-toggle') === 'true';

    // Aplicamos el estado del sidebar antes de que se vea la página
    if (isSidebarToggled) {
        document.body.classList.add('sb-sidenav-toggled');
    } else {
        document.body.classList.remove('sb-sidenav-toggled');
    }

    // Aseguramos que el contenido se vea solo después de aplicar el estado del sidebar
    document.body.classList.remove('d-none');

    // Funcionalidad del botón de toggle
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }
});
