$(function() {

    $("#generate").click(function() {
        $("#clear-graph-label").removeClass('hidden');
        if($('#category-label').hasClass('active')) {
            $.ajax({
                type: "GET",
                url: $SCRIPT_ROOT + "/api/category/" + $('#categories').find('option:selected').attr('id') + '/',
                contentType: "application/json; charset=utf-8",
                data: {
                    start_date: $('input[name="daterange"]').val().split(' ')[0],
                    end_date: $('input[name="daterange"]').val().split(' ')[2]
                },
                success: function (data) {
                    $("#data-notes").text(data.note);
                    $("#data-website").attr('href', '').empty().addClass('hidden');
                    $("#data-sf").attr('href', '').empty().addClass('hidden');
                    $("#data-description").empty().addClass('hidden');
                    $("#data-display").removeClass('js-plotly-plot').empty();
                    Plotly.newPlot(document.getElementById('data-display'), data.data, data.layout);
                }
            });
        }else{
            $.ajax({
                type: "GET",
                url: $SCRIPT_ROOT + "/api/company/" + $('#companies').find('option:selected').attr('id') + '/',
                contentType: "application/json; charset=utf-8",
                success: function (data) {
                    $("#data-notes").text(data.note);
                    $("#data-website").attr('href', data.info.website).text('Website').removeClass('hidden');
                    $("#data-sf").attr('href', data.info.salesforce).text('Salesforce').removeClass('hidden');
                    $("#data-description").text(data.info.description).removeClass('hidden');
                    $("#data-display").removeClass('js-plotly-plot').empty();
                    Plotly.newPlot(document.getElementById('data-display'), data.data, data.layout);
                }
            });
        }
    });

    $("#clear-graph-label").click(function(){
        $("#data-display").removeClass('js-plotly-plot').empty();
        $("#data-website").empty().addClass('hidden');
        $("#data-sf").empty().addClass('hidden');
        $("#data-description").empty().addClass('hidden');
        $(this).addClass('hidden');
        $("#data-notes").empty();
    });


    $('#category-label').click(function(){
        $('#categories').removeClass('hidden');
        $('#companies').addClass('hidden');
        $('input[name="daterange"]').removeClass('hidden');
    });

    $('#company-label').click(function(){
        $('#companies').removeClass('hidden');
        $('#categories').addClass('hidden');
        $('input[name="daterange"]').addClass('hidden');
    });
    $('input[name="daterange"]').daterangepicker();
});