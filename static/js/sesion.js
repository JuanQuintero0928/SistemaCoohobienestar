// Tiempo de sesión en milisegundos
const sessionTimeout = sessionTimeouDjango * 1000;
const warningTime = 60 * 5 * 1000 // 5 minutos en milisegundos

// Función para mostrar la alerta
setTimeout(function() {
    function obtenerHoraActual() {
        const ahora = new Date();
        const horas = agregarCero(ahora.getHours());
        const minutos = agregarCero(ahora.getMinutes());
        const segundos = agregarCero(ahora.getSeconds());
    
        return `${horas}:${minutos}:${segundos}`;
    }
    
    function agregarCero(num) {
        return num < 10 ? '0' + num : num;
    }
    alert(`Hemos notado un tiempo de inactividad prolongado. \n Recarga la pagina o tu sesión se cerrara en 5 minutos. \n Hora del mensaje: ${obtenerHoraActual()}`);
}, sessionTimeout - warningTime); // Restar el tiempo de advertencia del tiempo de sesión


// Redirige al usuario al inicio de sesión después de que expire la sesión
setTimeout(function() {
    alert("La sesión ha expirado. Serás redirigido al inicio de sesión.");
    window.location.href = "/accounts/login/"; 
}, sessionTimeout);