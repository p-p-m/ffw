
$(document).ready(function() {

    cart.url =$('div#cart').data('url');
    $('input#id_quant').val(cart.count);
    $('input#id_sum').val(cart.sum);
    var order = {
        'setProduct': function(data) {
            product = cart.products[data.product_pk];
            $('td#' + data.product_pk + '_sum').text(product.sum_ );
            order.setTotalData();
        },
        'setTotalData': function() {
            $('input#id_quant').val(cart.count);
            $('input#id_sum').val(cart.sum)
        },
     };
    order.setTotalData()
    $('button#cart_create').on('click', function() {
        var i = 1;
        while (i <= 5) {alert(i)
            cart.set(i,1, alert, callbackData=i + " - pk");   
            i++;
        }       
    });
    
    $('button#remove').on('click', function() {
        var product_pk = this.value;
        cart.remove(product_pk, getProducts);
   });


   $(".quant").change( function() {
        var product_pk = this.id;
        var quant = this.value;
        order.product_pk = product_pk
        callback = order.setProduct
        callbackData = {'product_pk': product_pk}
        cart.set(product_pk, quant, callback, callbackData);
   });

});
