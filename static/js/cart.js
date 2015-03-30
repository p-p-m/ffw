$(document).ready(function() {
 
    cart.fulling();

    $('button#remove').on('click', function() {
        var product_code = this.value; 
        cart.cart_change(product_code, 'remove');    
    });
    
    $('button#clear').on('click', function() {
        var product_code = this.value; 
        cart.cart_change(0, 'clear');    
    });
});


