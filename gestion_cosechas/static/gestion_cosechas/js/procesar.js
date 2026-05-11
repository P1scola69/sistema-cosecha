$(document).ready(function() {
    // 1. INDICADORES ECONÓMICOS (UF, UTM, EURO)
    $.ajax({
        url: 'https://mindicador.cl/api',
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            $('.infoUF').text('Seguro Agrícola (UF): $' + data.uf.valor);
            $('.infoUTM').text('Base Contratos (UTM): $' + data.utm.valor);
            $('.infoEuro').text('Exportación (EUR): $' + data.euro.valor);
        },
        error: function() {
            console.error("Error al cargar indicadores económicos.");
        }
    });


    $.ajax({
        url: 'https://api.open-meteo.com/v1/forecast?latitude=-37.46&longitude=-72.35&current_weather=true',
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            console.log("Datos clima recibidos:", data);
            
            if (data.current_weather) {
                var temp = data.current_weather.temperature;
                

                $('.temp-real').text(temp + '°C');


                if (temp > 20) {
                    $('.clima-msg').text('☀️ Condiciones óptimas para cosecha.');
                } else {
                    $('.clima-msg').text('☁️ Día fresco, ideal para trabajo de campo.');
                }
            }
        },
        error: function(xhr, status, error) {
            console.error("Error en API de clima:", error);
            $('.temp-real').text('Error');
            $('.clima-msg').text('No se pudo cargar el clima.');
        }
    });
})