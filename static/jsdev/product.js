$(document).ready(function() {

    cart.fulling();

    $('button#buy').on('click', function() {
        var product_pk = this.value;
        cart.cart_change(product_pk,'add');
    });
});
