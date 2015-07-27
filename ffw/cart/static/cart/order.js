
$(document).ready(function() {

    cart.url =$('div#cart').data('url');
    
    var order = {
        'setProduct': function(data) {
            product = cart.products[data.product_pk];
            $('td#' + data.product_pk + '_sum').text(product.sum_ );
            order.setTotalData();
        },
        'setTotalData': function() {
            $('span#total').text('Всего товаров ' + cart.count + ' на сумму ' + cart.sum)
            $('input#id_total').val(cart.sum)
        },
     };


    $('button#remove').on('click', function() {
        var product_pk = this.value;
        cart.remove(product_pk, getProducts);
   });


   $(".quant").change( function() {
        var product_pk = this.id;
        var quant = this.value;
        test = true;
        order.product_pk = product_pk
        callback = order.setProduct
        callbackData = {'product_pk': product_pk}
        cart.set(product_pk, quant, test, callback, callbackData);
   });


   $('button#add').on('click', function() {
        var product_pk = this.value;
        quant = $('#'+product_pk).val();
        var test = true;
        cart.add(product_pk, quant, test, cartTest.getProducts);
   });


   $("button#get").on("click", function() {cart.get(cartTest.getProducts)});


   $("button#clear").on("click", function() {cart.clear(cartTest.getProducts)});
});
