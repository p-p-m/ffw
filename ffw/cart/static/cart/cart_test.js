
$(document).ready(function() {

    cart.url =$('div#cart').data('url');

    var cartTest = {
        'getProducts': function() {
             var str = "Товаров: " + cart.count + " на сумму " + cart.sum + "грн" + '<br>'
                 for (product in cart.products) {
                     str += product + ": "+ cart.products[product].name  + " " + cart.products[product].product_code
                         + " " + cart.products[product].quant  +"шт"+ "*" + cart.products[product].price + "грн" + "=" + cart.products[product].sum_  + "грн" + '<br>';
                 };
              $("div#products").html(str);
              $("div#dict").text("products - " + cart.products.toSource());
        },
     };


    $('button#remove').on('click', function() {
        var product_pk = this.value;
        cart.remove(product_pk, cartTest.getProducts);
   });


   $('button#buy').on('click', function() {
        var product_pk = this.value;
        quant = $('#'+product_pk).val();
        var test = true;
        cart.set(product_pk, quant, test, cartTest.getProducts);
   });


   $('button#add').on('click', function() {
        var product_pk = this.value;
        quant = $('#'+product_pk).val();
        cart.add(product_pk, quant, cartTest.getProducts);
   });


   $("button#get").on("click", function() {cart.get(cartTest.getProducts)});


   $("button#clear").on("click", function() {cart.clear(cartTest.getProducts)});
});
