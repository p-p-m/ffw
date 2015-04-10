var cart = {
    'products': {},
    'sum': 0,
    'count': 0,
    //calc data of cart, insert total sum and count of products in the cart
    'fulling': function () {
        var sum_cart = $('div#cart').data('sum-cart');
        var count_cart = $('div#cart').data('count-cart');
        $('div.cart-count').text(count_cart);
        $('span.sum').text(sum_cart);
    },


    //action  can be: "clear" - clear the cart, "remove" - remove the product from the cart,
        //'add' (or any string) - add the product to the cart
    cart_change: function(product_pk, action) {
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

        $.ajaxPrefilter( function( options ) {
            options.url = $('div#cart').data('url');
        });

        if (action == 'remove' || action == 'clear') {
            //remove product from cart
            $.ajax({
                type: "POST",
                data:{
                    'product_pk': product_pk,
                    'action': action
                },
                dataType: 'text'
            })
            .done(function(data) {
                var obj = $.parseJSON(data);
                $('div.cart-count').text(obj.count_cart);
                $('span.sum').text(obj.sum_cart);
            });
        }
        else {
            //add product to cart
            $.ajax({
                type: "POST",
                data:{
                    'product_pk': product_pk
                },
                dataType: 'text'
            })
            .done(function(data) {
                var obj = $.parseJSON(data);
                $('div.cart-count').text(obj.count_cart);
                $('span.sum').text(obj.sum_cart);
                if (obj.msg) {
                    alert(obj.msg);
                };
            });
        };
    }
}
