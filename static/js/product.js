$(document).ready(function() {
 
    cart.fulling();

    $('button#product_add').on('click', function() {
        var product_code = this.value; 
        cart.cart_change(product_code,'add');  
               
    });
    
    $('button#go_cart').on('click', function() {
        document.location.href = "http://" + document.location.host + '/products/cart/cart/';
    });
    
});


