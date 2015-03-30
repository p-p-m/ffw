var cart = {
    'products': {},
               //find and insert  sum and quantity of products of the cart
    'fulling': function () {   
        $.ajaxPrefilter( function( options ) {
            options.url = "http://" + document.location.host + '/products/cart_get'  ;
        });

        $.ajax({
            type: "GET",         
            dataType: 'text'
        }).done(function(data) { 
            var cart_sess =  jQuery.parseJSON(data).cart;
            $('output#quant_cart').text(cart_sess.quant);  
            $('output#sum_cart').text(cart_sess.sum);
            cart.sum = cart_sess.sum;
            cart.quant = cart_sess.quant;
            cart.products = cart_sess.products;
        });
    }, 
    
    
               //action  can be: "clear" - clear the cart, "remove" - remove the product from the cart,
                  //any - add the product to the cart 
    cart_change: function(product_code, action) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
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
            options.url = "http://" + document.location.host + '/products/cart/'  ;
        });
        var res = action == 'remove' || action == 'clear';
        if (res) { 
                     //remove product from cart
            $.ajax({
                type: "POST",
                data:{
                    'product_code': product_code,
                    'action': action                    
                },            
                dataType: 'text'
            }) 
            .done(function(data) { 
                var obj = jQuery.parseJSON(data);
                $('output#quant_cart').text(obj.quant);  
                $('output#sum_cart').text(obj.sum);
            });       
        }
        else {
                       //add product to cart     
            $.ajax({
                type: "POST",
                data:{
                    'product_code': product_code                
                },            
                dataType: 'text'
            }) 
            .done(function(data) { 
                var obj = jQuery.parseJSON(data);
                $('output#quant_cart').text(obj.quant);  
                $('output#sum_cart').text(obj.sum);
            });   
        }
    }
};    
