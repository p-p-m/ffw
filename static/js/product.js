$(document).ready(function() {

    cart.fulling();
    
    $('button#buy').on('click', function() {
        var product_code = this.value;
        cart.cart_change(product_code,'add');
    });
});


