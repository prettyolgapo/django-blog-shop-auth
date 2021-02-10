$(document).ready( function() {
console.log("ghgjjgjj");
    $("input[name='quantity']")./*change*/keyup( function(event) {
        console.log("123");
        var quantityVal;
        //$( "input[name='quantity']" ).each(function( i ) {
           quantityVal = $( this ).val();
           //alert(quantityVal[i]);
        //});
        //$(this).var("$11111");
        var token = document.cookie.split('=')[1];

        $.ajax({
        url: '../cart-update/',
        type: "POST",
        data: {'csrfmiddlewaretoken' : token, 'quantity': quantityVal},
        //data: JSON.stringify({'csrfmiddlewaretoken' : token, 'quantity': quantityVal }),
        //contentType: "application/json; charset=utf-8",
        //dataType: 'json',
        success: function (data) {
            alert(data.total);
            $("#span-sub-total").text("$"+data.total);
            //$(this).next('.total').text("$"+data.total);
        },
      });
    });
});

