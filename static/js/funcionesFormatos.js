function numeroALetras(num) {
    const unidades = ['cero', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve'];
    const decenas = ['diez', 'once', 'doce', 'trece', 'catorce', 'quince', 'dieciséis', 'diecisiete', 'dieciocho', 'diecinueve'];
    const decenas2 = ['veinte', 'treinta', 'cuarenta', 'cincuenta', 'sesenta', 'setenta', 'ochenta', 'noventa'];
    const centenas = ['cien', 'doscientos', 'trescientos', 'cuatrocientos', 'quinientos', 'seiscientos', 'setecientos', 'ochocientos', 'novecientos'];

    function convertirMillones(numero) {
        if (numero >= 1000000) {
            let millones = Math.floor(numero / 1000000);
            let resto = numero - (millones * 1000000);
            let textoMillones = millones === 1 ? 'un millón' : `${convertirCentenas(millones)} millones`;
            if (resto > 0) {
                return `${textoMillones} ${convertirMiles(resto)}`;
            }
            return textoMillones;
        }
        return convertirMiles(numero);
    }

    function convertirMiles(numero) {
        if (numero >= 1000) {
            let miles = Math.floor(numero / 1000);
            let resto = numero - (miles * 1000);
            let textoMiles = miles === 1 ? 'mil' : `${convertirCentenas(miles)} mil`;
            if (resto > 0) {
                return `${textoMiles} ${convertirCentenas(resto)}`;
            }
            return textoMiles;
        }
        return convertirCentenas(numero);
    }

    function convertirCentenas(numero) {
        if (numero >= 100) {
            let centenasIndex = Math.floor(numero / 100);
            let resto = numero - (centenasIndex * 100);
            if (numero === 100) return 'cien';
            let textoCentenas = centenas[centenasIndex - 1];
            if (resto > 0) {
                return `${textoCentenas} ${convertirDecenas(resto)}`;
            }
            return textoCentenas;
        }
        return convertirDecenas(numero);
    }

    function convertirDecenas(numero) {
        if (numero >= 10 && numero <= 19) {
            return decenas[numero - 10];
        } else if (numero >= 20) {
            let decenasIndex = Math.floor(numero / 10);
            let resto = numero - (decenasIndex * 10);
            let textoDecenas = decenas2[decenasIndex - 2];
            if (resto > 0) {
                return `${textoDecenas} y ${unidades[resto]}`;
            }
            return textoDecenas;
        }
        return convertirUnidades(numero);
    }

    function convertirUnidades(numero) {
        return unidades[numero];
    }

    return `${convertirMillones(num)} pesos`.trim();
}

function sumarMeses(fechaStr, meses) {
    let fecha = convertirFecha(fechaStr);
    fecha.setMonth(fecha.getMonth() + meses);
    return formatearFecha(fecha);
}

function convertirFecha(fechaStr) {
    let [año, mes, dia] = fechaStr.split("-").map(num => parseInt(num, 10));
    return new Date(año, mes - 1, dia); // Meses van de 0 a 11
}

function formatearFecha(fecha) {
    const meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ];

    let dia = fecha.getDate();
    let mes = meses[fecha.getMonth()];
    let año = fecha.getFullYear();

    return `${dia} de ${mes} de ${año}`;
}

function convertirMes(mes) {

    let meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ];

    return meses[mes-1];
}