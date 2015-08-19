
$(document).ready(function() {

    cart.url =$('div#cart').data('url');
    cart.get()
    var order = {
        'setProduct': function(data) {
            product = cart.products[data.product_pk];
            var name = data.product_pk + '_sum';
            $(order.selector_role(name)).text(product.sum_ );
            order.setTotalData();
        },
        'setTotalData': function() {
            $('input#id_quant').val(cart.count);
            $('input#id_total').val(cart.total)
        },

        'selector_role': function(name) {
            return '[data-role=' + '"' + name  + '"'+ "]"
        }
     };

    $('[data-role = "remove"]').on('click', function() {
        var product_pk = this.value;
        if (confirm("Удалить товар из корзины?")) {
             $(order.selector_role(product_pk)).remove();
            cart.remove(product_pk, callback=order.setTotalData);
        };
   });

   $('[data-role = "set"]').on('click', function() {
        for (product_pk=1; product_pk<3; product_pk++) {
             cart.set(+product_pk, 1, callback=order.setTotalData);
        };
   }) ;

   $('[data-role = "quant"]').change( function() {
       var product_pk = this.id;
       var quant = this.value;
       order.product_pk = product_pk;
       var  callback = order.setProduct.bind('context', {'product_pk': product_pk});
       cart.set(+product_pk, quant, callback);
    }) ;

    $('[data-role = "add"]').on('click', function() {
        cart.add(1, 5, callback=order.setTotalData);
    });

    $('[data-role = "clear"]').on('click', function() {
        cart.clear(callback=order.setTotalData);
    });
});
