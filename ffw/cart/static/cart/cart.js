/*
cart data in request.session: {"cart_sum": cart_sum, "cart-count":
        cart_count, "products": {product_pk_1: {'product_code': product_code,
       'name': name,  'price': price,  'count': count, 'sum_': sum_}...}}

 cart.set(product_pk, quant, callback) - добавляет товар с кол-вом quant  в
         корзину или устанавливает  количество данного товара в корзине равным
         quant

cart.remove(product_pk, callback) - удаляет товар из корзины и вызывает функцию
        callback

cart.get(callback) - получает данные корзины и вызывает функцию callback

cart.clear(callback) - удаляет все товары из корзины и вызывает функцию
        callback

cart.products = {'product_pk': product_code,  'name': name,  'price': price,
    'count': count, 'sum_': sum_}...}  словарь

cart.sum - товаров в корзине на сумму

cart.count - кол-во товаров в корзине
*/

var cart = {
    'products': {},
    'sum': 0,
    'count': 0,
    'url': '',
    'updateCartAndCallback': function(data,callback) {
            var obj = $.parseJSON(data);
            cart.count = obj.count_cart;
            cart.sum = obj.sum_cart;
            cart.products = obj.products_cart;
            callback();
        },
    'set': function(product_pk, quant, callback) {
        cart.csrf();

        $.ajax({
            url: cart.url + 'set/',
            type: "POST",
            data:{
                'product_pk': product_pk,
                'quant': quant
           },
            dataType: 'text'
        })
        .done(function(data) {
             cart.updateCartAndCallback(data, callback);
        });
    },
    'remove': function(product_pk, callback) {
        cart.csrf();

        $.ajax({
            url: cart.url + 'remove/',
            type: "POST",
            data:{
                'product_pk': product_pk,
           },
            dataType: 'text'
       })
        .done(function(data) {
             cart.updateCartAndCallback(data, callback);
        });
    },
    'clear': function(callback) {
        cart.csrf();

        $.ajax({
            url: cart.url,
            type: "POST",
            dataType: 'text'
       })
        .done(function(data) {
             cart.updateCartAndCallback(data, callback);
        });
   },
    'get': function(callback) {
        $.ajax({
            url: cart.url,
            type: "GET",
            dataType: 'text'
       })
       .done(function(data) {
             cart.updateCartAndCallback(data, callback);
        });
    },
    'csrf': function() {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = $.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                   }
               }
           }
            return cookieValue;
       }

        var csrftoken = getCookie('csrftoken');

        function csrfSafeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
       }
         $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
               }
           }
        });
   },
};

$(document).ready(function() {
    cart.url =$('div#cart').data('url');
    cart.get(function() {console.log(cart.products, 'get')});
    cart.clear(function() {console.log(cart.products, 'clear')});
    // For cart-display.html
    $('button#remove').on('click', function() {
        var product_pk = this.value;
        cart.remove(product_pk, function() {console.log(cart.products, 'remove')});
   });

    //  For products_list.html and product.html
    $('button#buy').on('click', function() {
        var product_pk = this.value;
        var quant = $(this).data('quant');
        cart.set(product_pk, quant,function() {console.log(cart.products, 'set')});
   });
});
