


 $("#drop").change(function () {
        var end = this.value;
        var firstDropVal = $('#drop').find(":selected").attr("id");
        console.log(firstDropVal);
        if(firstDropVal!="DEF"){
       $.ajax({
        type: "GET",
        url: "/api/carreras/"+firstDropVal,
        dataType: "json",
        success: function(csv) {procesarCSV(csv);}
        });
        }
        else {
            $('#seleccion').empty();
        }
});

function procesarCSV(csv) {
    var codigos= [];
    var nombres= [];
    $('#seleccion').empty();
    $(csv.datos).each(function(i,item) {
        $("#seleccion").append('<li class="list-group-item">'+item.nombre+'</li>');
        codigos.push(item.materia);
        nombres.push(item.nombre);
    });

    $("#codigos").val(JSON.stringify(codigos));
    $("#nombres").val(JSON.stringify(nombres));

    $(function () {
    $('.list-group.checked-list-box .list-group-item').each(function () {
        
        // Settings
        var $widget = $(this),
            $checkbox = $('<input type="checkbox" class="hidden" />'),
            color = ($widget.data('color') ? $widget.data('color') : "primary"),
            style = ($widget.data('style') == "button" ? "btn-" : "list-group-item-"),
            settings = {
                on: {
                    icon: 'glyphicon glyphicon-check'
                },
                off: {
                    icon: 'glyphicon glyphicon-unchecked'
                }
            };
            
        $widget.css('cursor', 'pointer')
        $widget.append($checkbox);

        // Event Handlers
        $widget.on('click', function () {
            $checkbox.prop('checked', !$checkbox.is(':checked'));
            $checkbox.triggerHandler('change');
            updateDisplay();
        });
        $checkbox.on('change', function () {
            updateDisplay();
        });
          

        // Actions
        function updateDisplay() {
            var isChecked = $checkbox.is(':checked');

            // Set the button's state
            $widget.data('state', (isChecked) ? "on" : "off");

            // Set the button's icon
            $widget.find('.state-icon')
                .removeClass()
                .addClass('state-icon ' + settings[$widget.data('state')].icon);

            // Update the button's color
            if (isChecked) {
                $widget.addClass(style + color + ' active');
            } else {
                $widget.removeClass(style + color + ' active');
            }
        }

        // Initialization
        function init() {
            
            if ($widget.data('checked') == true) {
                $checkbox.prop('checked', !$checkbox.is(':checked'));
            }
            
            updateDisplay();

            // Inject the icon if applicable
            if ($widget.find('.state-icon').length == 0) {
                $widget.prepend('<span class="state-icon ' + settings[$widget.data('state')].icon + '"></span>');
            }
        }
        init();
    });
    
    $('#get-checked-data').on('click', function(event) {
        event.preventDefault(); 
        var checkedItems = {}, counter = 0;
        $("#check-list-box li.active").each(function(idx, li) {
            checkedItems[counter] = $(li).text();
            counter++;
        });
        $('#display-json').html(JSON.stringify(checkedItems, null, '\t'));
    });
});
}

function enviarDatos(){
    var escogidas=[];
    var nombres= JSON.parse($("#nombres").val());
    var disponibilidad= $('#tiempo').find(":selected").attr("id");
    var firstDropVal = $('#drop').find(":selected").attr("id");

    if(firstDropVal!="DEF"){

     $('#seleccion').find('li').each(function(){
        if($(this).attr('class')=="list-group-item list-group-item-primary active"){
            escogidas.push(1);
        } else{
            escogidas.push(0);
        }
     });

     var envio={carrera_id: firstDropVal, materias: JSON.parse($("#codigos").val()), estado: escogidas};
     console.log(envio);

     $.ajax({
        type: "POST",
        url: "/api/recomendacion",
        data: JSON.stringify(envio),
        dataType: "json",
        success: function(response) {
            var codigos= JSON.parse($("#codigos").val());
            var dif0= {materias: [], codigos: []};
            var dif1= {materias: [], codigos: []};
            var dif2= {materias: [], codigos: []};
            var dif3= {materias: [], codigos: []};
            var dif4= {materias: [], codigos: []};
            var recomendaciones= {materias: [], codigos: []};
            var cont=0;
            console.log(response);

            $(response.datos.materias_disponibles).each(function(i,item) {
                if(item==1){
                    
                    switch(response.datos.dificultad[cont]) {
                        case 0:
                            dif0.materias.push(nombres[i]);
                            dif0.codigos.push(codigos[i]);
                            break;
                        case 1:
                            dif1.materias.push(nombres[i]);
                            dif1.codigos.push(codigos[i]);
                            break;
                        case 2:
                            dif2.materias.push(nombres[i]);
                            dif2.codigos.push(codigos[i]);
                            break;
                        case 3:
                            dif3.materias.push(nombres[i]);
                            dif3.codigos.push(codigos[i]);
                            break;
                        case 4:
                            dif4.materias.push(nombres[i]);
                            dif4.codigos.push(codigos[i]);
                            break;            
                    }
                cont++;
                }
            });

            /*
            console.log(dif0);
            console.log(dif1);
            console.log(dif2);
            console.log(dif3);
            console.log(dif4);*/

            

            //$("#recomendaciones").append('<h3>'+nombres[i]+'</h3>');


            $('#myModal').modal('toggle');
        }
        });
     

    

    }
}