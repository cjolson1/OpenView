$(function() {
    $("#generate").click(function() {
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
                    $('#data-notes').text(data.note);
                    Plotly.newPlot(document.getElementById('data-display'), data.data, data.layout);
                }
            });
        }else{
            $.ajax({
                type: "GET",
                url: $SCRIPT_ROOT + "/api/company/" + $('#companies').find('option:selected').attr('id') + '/',
                contentType: "application/json; charset=utf-8",
                success: function (data) {
                    Plotly.newPlot(document.getElementById('data-display'), data.data, data.layout);
                }
            });
        }
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