
$(document).ready(function() {

    cart.url =$('div#cart').data('url');
    cart.get()
    var order = {
        'setProduct': function(data) {
            product = cart.products[data.productPk];
            var name = data.productPk + '_sum';
            $(order.selector_role(name)).text(product.sum_ );
            order.setTotalData();
        },
        'setTotalData': function() {
            $('[data-role="count"]').text(cart.count);
            $('[data-role="total"]').text(cart.total);
        },

        'selector_role': function(name) {
            return '[data-role=' + '"' + name  + '"'+ "]"
        }
     };

    $('[data-role="remove"]').on('click', function() {
        var productPk = this.value;
        if (confirm("Удалить товар из корзины?")) {
             //$(order.selector_role(productPk)).remove();
            var productPkList = [1,2];
            cart.remove(productPkList, callback=order.setTotalData);
        };
   });

   $('[data-role="set"]').on('click', function() {
        var productDict ={}
        for (productPk=1; productPk<4; productPk++) {
             productDict[productPk] = 2 + 2 * productPk
        };
        cart.set(productDict, callback=order.setTotalData);
   }) ;

    $('[data-role="quant"]').on('input', function() {
       var productPk = this.id;
       var quant = this.value;
       order.productPk = productPk;
       var  callback = order.setProduct.bind('context', {'productPk': productPk});
       var productDict = {};
       productDict[productPk]= quant;
       cart.set(productDict, callback);
    }) ;

    $('[data-role="add"]').on('click', function() {
        var productDict ={}
        for (productPk=1; productPk<4; productPk++) {
             productDict[productPk] =10
        };
        cart.add(productDict, callback=order.setTotalData);
    });

    $('[data-role="clear"]').on('click', function() {
        cart.clear(order.setTotalData);
    });
});
