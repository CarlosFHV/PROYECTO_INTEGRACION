$(function() {
    var sliderContainer = $("#slider-range");
    var izq = sliderContainer.data("izq");
    var der = sliderContainer.data("der");


    $("#slider-range").slider({
        range: true,
        min: 0,
        max: 1,
        step: 0.001,
        values: [izq,der],
        slide: function(event, ui) {
            $(".izqNegativo").val(ui.values[0]);
            $(".derPositivo").val(ui.values[1]);
            $(".izqNeutro").val(ui.values[0]);
            $(".derNeutro").val(ui.values[1]);
        }
    });
    $(".izqNegativo").val($("#slider-range").slider("values", 0));
    $(".derPositivo").val($("#slider-range").slider("values", 1));
    $(".izqNeutro").val($("#slider-range").slider("values", 0));
    $(".derNeutro").val($("#slider-range").slider("values", 1));

    $(".izqNegativo, .derPositivo").on("input", function() {
        var izqNegativoVal = parseFloat($(".izqNegativo").val());
        var derPositivoVal = parseFloat($(".derPositivo").val());
        
        $(".izqNeutro").val(izqNegativoVal);
        $(".derNeutro").val(derPositivoVal);

        if ( izqNegativoVal<=derPositivoVal ) {
            $("#slider-range").slider("values", [izqNegativoVal, derPositivoVal]);

        }else{
          // alert("Rango erroneo");
      
        }
    });

    $(".izqNeutro, .derNeutro").on("input", function() {
  
        var izqNeutroVal = parseFloat($(".izqNeutro").val());
        var derNeutroVal = parseFloat($(".derNeutro").val());

        $(".izqNegativo").val(izqNeutroVal);
        $(".derPositivo").val(derNeutroVal);

        if (izqNeutroVal <= derNeutroVal ) {
            $("#slider-range").slider("values", [izqNeutroVal, derNeutroVal]);

        }else{
            //alert("Rango erroneo");
        
        }
    });


});


$(function() {
    $("#modificar_rango").click(function() {
        var izqNeutroVal = parseFloat($(".izqNeutro").val());
        var derNeutroVal = parseFloat($(".derNeutro").val());
        var izqVal = parseFloat($("#slider-range").data("izq"));
        var derVal = parseFloat($("#slider-range").data("der"));

        if (izqNeutroVal >= derNeutroVal) {
            alert("El valor de Neutro izquierdo debe ser menor que el valor de Neutro derecho.");
            return;
        }

        $("#form-modificar-rango").submit();
    });
});

