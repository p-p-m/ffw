/*
Connect:
    1. <script src="{{ STATIC_URL }}cart/cart.js"> </script>
    2. Должен быть задан урл в свойстве тега data-cart-url='some/url/'.

cart data in request.session: {"cart_sum": cart_sum, "cart-count":
        cart_count, "products": {product_pk_1: {'product_code': product_code,
       'name': name,  'price': price,  'quant': quant, 'sum_': sum_}...}}

Object cart:
    After  successfully execution all methods update the attributes of the cart and call function callback

    Methods:

        cart.set(product_pk, quant, callback) - set quantity of the product in the cart equal quant

        cart.add(product_pk, quant, callback) - add quantity of the product in the cart equal quant

        cart.remove(product_pk, callback) - remove the product from the cart

        cart.get(callback) - get attributes of the cart

        cart.clear(callback) -clear the cart

     Attributes :
        cart.products = {{'product_pk': product_code,  'name': name,  'price': price,
           'quant': quant, 'sum_': sum_}...} - dictionary

        cart.sum - total cost of the cart products

        cart.count - total quantity of the cart products


Testing apllication cart:
    url = 'cart/test'

Settings:
    There is necessary insert in  settings:
    CART_SETTINGS = {
        'model_name': model_name,
        'appl_name': appl_name,
        'price_field_name': price_field_name,
        'code_field_name': code_field_name,
        'name_field_name': name_field_name
    }
*/

var cart = {
    'products': {},
    'sum': 0,
    'count': 0,
    'url': '',
    'updateCartAndCallback': function(data, callback=null, callbackData=null) {
            var obj = $.parseJSON(data);
            cart.count = obj.count_cart;
            cart.sum = obj.sum_cart;
            cart.products = obj.products_cart;
            if (callback) {
                if (callbackData) {
                     callback(callbackData);
                }
                 else {
                     callback();
                 };
            };
    },
    'set': function(product_pk, quant, callback=null, callbackData=null) {
        cart.csrf();

        $.ajax({
            url: cart.url + 'set/',
            type: "POST",
            data:{
                'product_pk': product_pk,
                'quant': quant,
           },
            dataType: 'text'
        })
        .done(function(responseData) {
             cart.updateCartAndCallback(responseData, callback, callbackData);
        });
    },
    'add': function(product_pk, quant, callback=null, callbackData=null) {
        cart.csrf();

        $.ajax({
            url: cart.url + 'add/',
            type: "POST",
            data:{
                'product_pk': product_pk,
                'quant': quant,
                'test': test
           },
            dataType: 'text'
        })
        .done(function(data) {
             cart.updateCartAndCallback(data, callback, callbackData);
        });
    },
    'remove': function(product_pk, callback=null, callbackData=null) {
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
             cart.updateCartAndCallback(data, callback, callbackData);
        });
    },
    'clear': function(callback=null, callbackData=null) {
        cart.csrf();

        $.ajax({
            url: cart.url,
            type: "POST",
            dataType: 'text'
       })
        .done(function(data) {
             cart.updateCartAndCallback(data, callback, callbackData);
        });
   },
    'get': function(callback=null, callbackData=null) {
        $.ajax({
            url: cart.url,
            type: "GET",
            dataType: 'text'
       })
       .done(function(data) {
             cart.updateCartAndCallback(data, callback, callbackData);
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
}
