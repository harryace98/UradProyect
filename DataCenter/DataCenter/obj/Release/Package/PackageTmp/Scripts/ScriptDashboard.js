// variable que nos controla los request de la la data, en caso de saturacion, no permite realizar mas solicictudes 
$.xhrPool = [];
$.xhrPool.abortAll = function () {
    $(this).each(function (idx, jqXHR) {
        jqXHR.abort();
    });
    $.xhrPool.length = 0
};
let chartdata;
let chartdataTransito;

const chart = document.getElementById("LinarBarchart");
const chartTransito = document.getElementById("transitBarchart");

function PantallaInicioInit() {
    
    CargarGraficoBarras();
    CargarTargetas();
    CargarGraficoTransito();

    setInterval(function () {
        CargarTargetas();
    }, 30000);
    setInterval(function () {
        RecargarGraficoBarras();
        RecargarGraficoTrafico();
    }, 60000);
}

function CargarTargetas() {

    var CardHora = document.getElementById("CardHora");
    var CardDia = document.getElementById("CardDia");
    var CardSemana = document.getElementById("CardSemana");
    var CardMes = document.getElementById("CardMes");

    var filter = { nodo: "N000" };
    if ($.xhrPool.length < 3) {
        $.ajax({
            url: '/Home/ObtenerDatosVelocidad',
            type: 'GET',
            data:filter,
            beforeSend: function (jqXHR) {
                $.xhrPool.push(jqXHR);
            },
            error: function (err) {
                console.log(err);
            },
            success: function (res) {
                CardDia.innerHTML = res[0].toFixed(2);
                CardHora.innerHTML = res[1].toFixed(2);
                CardSemana.innerHTML = res[2].toFixed(2);
                CardMes.innerHTML = res[3].toFixed(2);
            },
            complete: function (jqXHR) {
                var index = $.xhrPool.indexOf(jqXHR);
                if (index > -1) {
                    $.xhrPool.splice(index, 1);
                }

            }
        });
    }
}

function RecargarGraficoBarras() {
    var labels = [];
    var linearchartdata = [];
    var barchardataPos = [];
    var barchartdataNeg = [];

    if (chartdata != null) {
        chartdata.destroy();


        if ($.xhrPool.length < 3) {
            $.ajax({
                url: '/Home/ObtenerDatosConsolidadosGrafica',
                type: 'GET',
                beforeSend: function (jqXHR) {
                    $.xhrPool.push(jqXHR);
                },
                error: function (err) {
                    console.log(err);
                },
                success: function (res) {

                    for (let i = 0; i < res.length; i++) {
                        labels.push(res[i].Labels);
                        linearchartdata.push(res[i].LinearChartData);
                        barchardataPos.push(res[i].VelocidadPositiva);
                        barchartdataNeg.push(res[i].VelocidadNegativa);
                    }
                    data = {
                        labels: labels,
                        datasets: [
                            {
                                label: 'Sentido Este-Oeste',
                                data: barchardataPos,
                                order: 1,
                                backgroundColor: '#1ab394',
                                type: 'bar'
                            },
                            {
                                label: 'Sentido Oeste-Este',
                                data: barchartdataNeg,
                                backgroundColor: '#ED5565',
                                order: 2,
                                type: 'bar'
                            },
                            {
                                label: 'Promedio',
                                backgroundColor: '#f8ac59',
                                borderColor: '#f8ac59',
                                data: linearchartdata,
                                order: 0,
                            }
                        ]
                    };
                    var config = {
                        type: 'line',
                        data: data,
                        options: {
                            plugins: {
                                title: {
                                    display: true,
                                    text: 'Velocidad minuto a minuto'
                                }
                            }
                        },
                    };

                    chartdata = new Chart(chart, config)
                },
                complete: function (jqXHR) {
                    var index = $.xhrPool.indexOf(jqXHR);
                    if (index > -1) {
                        $.xhrPool.splice(index, 1);
                    }

                }
            });
        }
    }
}

function CargarGraficoBarras() {

    var labels = [];
    var linearchartdata = [];
    var barchardataPos = [];
    var barchartdataNeg = [];
    var data;

    if ($.xhrPool.length < 3) {
        $.ajax({
            url: '/Home/ObtenerDatosConsolidadosGrafica',
            type: 'GET',
            beforeSend: function (jqXHR) {
                $.xhrPool.push(jqXHR);
            },
            error: function (err) {
                console.log(err);
            },
            success: function (res) {

                for (let i = 0; i < res.length; i++) {
                    labels.push(res[i].Labels);
                    linearchartdata.push(res[i].LinearChartData);
                    barchardataPos.push(res[i].VelocidadPositiva);
                    barchartdataNeg.push(res[i].VelocidadNegativa);
                }
                data = {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Sentido Este-Oeste',
                            data: barchardataPos,
                            order: 1,
                            backgroundColor: '#1ab394',
                            type: 'bar'
                        },
                        {
                            label: 'Sentido Oeste-Este',
                            data: barchartdataNeg,
                            backgroundColor: '#ED5565',
                            order: 2,
                            type: 'bar'
                        },
                        {
                            label: 'Promedio',
                            backgroundColor: '#f8ac59',
                            borderColor: '#f8ac59',
                            data: linearchartdata,
                            order: 0,
                        }
                    ]
                };
                var config = {
                    type: 'line',
                    data: data,
                    options: {
                        plugins: {
                            title: {
                                display: true,
                                text: 'Velocidad minuto a minuto'
                            }
                        }
                    },
                };
                chartdata = new Chart(chart, config)
            },
            complete: function (jqXHR) {
                var index = $.xhrPool.indexOf(jqXHR);
                if (index > -1) {
                    $.xhrPool.splice(index, 1);
                }

            }
        });
    }
}

function CargarGraficoTransito() {

    var labels = [];
    var linearchartdata = [];
    var barchardataPos = [];
    var barchartdataNeg = [];
    var data;

    if ($.xhrPool.length < 3) {
        $.ajax({
            url: '/Home/ObtenerDatosTransitoConsolidados',
            type: 'GET',
            beforeSend: function (jqXHR) {
                $.xhrPool.push(jqXHR);
            },
            error: function (err) {
                console.log(err);
            },
            success: function (res) {

                for (let i = 0; i < res.length; i++) {
                    labels.push(res[i].Labels);
                    linearchartdata.push(res[i].LinearChartData);
                    barchardataPos.push(res[i].VelocidadPositiva);
                    barchartdataNeg.push(res[i].VelocidadNegativa);
                }
                data = {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Sentido Este-Oeste',
                            data: barchardataPos,
                            order: 1,
                            backgroundColor: '#1ab394',
                            type: 'bar'
                        },
                        {
                            label: 'Sentido Oeste-Este',
                            data: barchartdataNeg,
                            backgroundColor: '#ED5565',
                            order: 2,
                            type: 'bar'
                        },
                        {
                            label: 'Promedio',
                            backgroundColor: '#f8ac59',
                            borderColor: '#f8ac59',
                            data: linearchartdata,
                            order: 0,
                        }
                    ]
                };
                var config = {
                    type: 'line',
                    data: data,
                    options: {
                        plugins: {
                            title: {
                                display: true,
                                text: 'Transito minuto a minuto'
                            }
                        }
                    },
                };
                chartdataTransito = new Chart(chartTransito, config);
            },
            complete: function (jqXHR) {
                var index = $.xhrPool.indexOf(jqXHR);
                if (index > -1) {
                    $.xhrPool.splice(index, 1);
                }

            }
        });
    }
}


function RecargarGraficoTrafico() {
    var labels = [];
    var linearchartdata = [];
    var barchardataPos = [];
    var barchartdataNeg = [];

    if (chartdata != null) {
        chartdata.destroy();


        if ($.xhrPool.length < 3) {
            $.ajax({
                url: '/Home/ObtenerDatosTransitoConsolidados',
                type: 'GET',
                beforeSend: function (jqXHR) {
                    $.xhrPool.push(jqXHR);
                },
                error: function (err) {
                    console.log(err);
                },
                success: function (res) {

                    for (let i = 0; i < res.length; i++) {
                        labels.push(res[i].Labels);
                        linearchartdata.push(res[i].LinearChartData);
                        barchardataPos.push(res[i].VelocidadPositiva);
                        barchartdataNeg.push(res[i].VelocidadNegativa);
                    }
                    data = {
                        labels: labels,
                        datasets: [
                            {
                                label: 'Sentido Este-Oeste',
                                data: barchardataPos,
                                order: 1,
                                backgroundColor: '#1ab394',
                                type: 'bar'
                            },
                            {
                                label: 'Sentido Oeste-Este',
                                data: barchartdataNeg,
                                backgroundColor: '#ED5565',
                                order: 2,
                                type: 'bar'
                            },
                            {
                                label: 'Promedio',
                                backgroundColor: '#f8ac59',
                                borderColor: '#f8ac59',
                                data: linearchartdata,
                                order: 0,
                            }
                        ]
                    };
                    var config = {
                        type: 'line',
                        data: data,
                        options: {
                            plugins: {
                                title: {
                                    display: true,
                                    text: 'Transito minuto a minuto'
                                }
                            }
                        },
                    };
                    chartdataTransito = new Chart(chartTransito, config);
                },
                complete: function (jqXHR) {
                    var index = $.xhrPool.indexOf(jqXHR);
                    if (index > -1) {
                        $.xhrPool.splice(index, 1);
                    }

                }
            });
        }
    }
}