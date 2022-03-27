// variable que nos controla los request de la la data, en caso de saturacion, no permite realizar mas solicictudes 
$.xhrPool = [];
$.xhrPool.abortAll = function () {
    $(this).each(function (idx, jqXHR) {
        jqXHR.abort();
    });
    $.xhrPool.length = 0
};
var filter = {
    fechaInicio: "2022-01-01 00:00:00",
    FechaFin: "2022-02-01 00:00:00",
    nodo: "N000"
};

var table;

function RecargarTabla() {
    table.ajax.reload();
}

function CargarDatosTabla() {

    debugger;
    table = $('#example').DataTable({
        ajax: {
            url: '/Home/ObtenerEntradaDatobyFecha',
            type: 'GET',
            data: function (d) {
                if ($('#dateInicio').val() != '' && $('#TimeInicio').val() != '') {

                    filter.fechaInicio = $('#dateInicio').val() + ' ' + $('#TimeInicio').val() + ':00'
                }
                if ($('#dateFin').val() != '' && $('#TimeFin').val() != '') {

                    filter.FechaFin = $('#dateFin').val() + ' ' + $('#TimeFin').val() + ':00'
                }
                d.fechaInicio = filter.fechaInicio;
                d.FechaFin = filter.FechaFin;
                d.nodo = filter.nodo;
            },
            beforeSend: function (jqXHR) {
                $.xhrPool.push(jqXHR);
            },
            error: function (err) {
                console.log(err);
            },
            complete: function (jqXHR) {
                var index = $.xhrPool.indexOf(jqXHR);
                if (index > -1) {
                    $.xhrPool.splice(index, 1);
                }

            }
        },
        processing: true,
        columns: [
            { "data": "CodigoEntradaDato" },
            { "data": "CodigoNodo" },
            { "data": "Velocidad" },
            { "data": "SNR" },
            { "data": "HoraEntrada" }
        ],
        language: {
            "lengthMenu": "Mostrar _MENU_ registros",
            "zeroRecords": "No se encontraron resultados",
            "info": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
            "infoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
            "infoFiltered": "(filtrado de un total de _MAX_ registros)",
            "sSearch": "Buscar:",
            "oPaginate": {
                "sFirst": "Primero",
                "sLast": "Último",
                "sNext": "Siguiente",
                "sPrevious": "Anterior"
            },
            "sProcessing": "Procesando...",
        },
        //para usar los botones
        responsive: "true",
        dom: 'Bfrtilp',
        buttons: [
            {
                extend: 'excelHtml5',
                text: '<ion-icon name="document-text-outline"></ion-icon>',
                titleAttr: 'Exportar a Excel',
                className: 'btn btn-success'
            },
            {
                extend: 'print',
                text: '<ion-icon name="print-outline"></ion-icon> ',
                titleAttr: 'Imprimir',
                className: 'btn btn-info'
            },
        ]
    });
}
