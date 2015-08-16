
$(document).ready(function() {

    cart.url =$('div#cart').data('url');
    cart.get()
    var order = {
        'setProduct': function(data) {
            product = cart.products[data.product_pk];
            $('td#' + data.product_pk + '_sum').text(product.sum_ );
            order.setTotalData();
        },
        'setTotalData': function() {
            $('input#id_quant').val(cart.count);
            $('input#id_summ').val(cart.total)
        },
     };

    $('button#remove').on('click', function() {
        var product_pk = this.value;
        if (confirm("Удалить товар из корзины?")) {
            $('tr#' + product_pk).remove();
            cart.remove(product_pk, callback=order.setTotalData);
        };
   });

   $('button#set').on('click', function() {
        for (product_pk=1; product_pk<3; product_pk++) {
             cart.set(+product_pk, 1, callback=order.setTotalData);
        };
   }) ;

   $(".quant").change( function() {
        var product_pk = this.id;
        var quant = this.value;
        order.product_pk = product_pk;
        cart.set(product_pk, quant, callback=order.setProduct, callbackData={'product_pk': product_pk});
    }) ;

    $('button#add').on('click', function() {
             cart.add(1, 5, callback=order.setTotalData);
        });

    $('button#clear').on('click', function() {
             cart.clear(callback=order.setTotalData);
        });
});
