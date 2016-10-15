$(function() {
    $("#generate").click(function() {
         $.ajax({
            type: "GET",
            url: $SCRIPT_ROOT + "/api/"+$('#categories').find('option:selected').attr('id')+'/',
            contentType: "application/json; charset=utf-8",
             data: { start_date: $('input[name="daterange"]').val().split(' ')[0], end_date: $('input[name="daterange"]').val().split(' ')[2]},
            success: function(data) {
                console.log(data.note);
                $('#data-notes').text(data.note);
                Plotly.newPlot(document.getElementById('data-display'), data.data, data.layout);
            }
        });
    });
    $('input[name="daterange"]').daterangepicker();
});