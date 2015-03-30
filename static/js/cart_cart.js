$(document).ready(function() {
 
    cart.fulling();

    $('button#product_add').on('click', function() {
        var product_code = this.value; 
        cart.add(product_code);    
    });
    
    $('button#remove').on('click', function() {
        document.location.href = "http://" + document.location.host + '/products/cart/cart/'
    })

});


