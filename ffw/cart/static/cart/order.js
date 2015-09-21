
$(document).ready(function() {

    var order = {
        'setProduct': function(data) {
            product = cart.products[data.productPk];
            var name = data.productPk + '_sum';
            $(order.selectorRole(name)).text(product.sum_);
            order.setTotalData();
        },
        'setTotalData': function() {
            $('[data-role="count"]').text(cart.count);
            $('[data-role="total"]').text(cart.total);
            checkOrderAvailability();
        },

        'selectorRole': function(name) {
            return '[data-role=' + '"' + name  + '"'+ "]";
        }
     };

    $('[data-role="remove"]').on('click', function() {
        var productPk = $(this).attr('data-value');
        if (confirm("Удалить товар из корзины?")) {
            $(order.selectorRole(productPk)).remove();
            var productPkList = [productPk,];
            cart.remove(productPkList, order.setTotalData);
        }
   });

    $('[data-role="quant"]').on('change', function() {
       var productPk = this.id;
       var quant = this.value;
       order.productPk = productPk;
       var  callback = order.setProduct.bind('context', {'productPk': productPk});
       var productDict = {};
       productDict[productPk]= quant;
       cart.set(productDict, callback);
    }) ;

    $('[data-role="clear"]').on('click', function() {
        cart.clear(order.setTotalData);
    });

    function checkOrderAvailability() {
        console.log(parseFloat($('[data-role="count"]').text()));
        if (parseFloat($('[data-role="count"]').text()) === 0) {
            $('[data-role="order-block"]').hide();
        }
    }

    checkOrderAvailability();

});
