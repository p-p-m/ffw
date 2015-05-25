var cart = {
    'products': {},
    'sum': 0,
    'count': 0,
    'url': '',
    'set': function(product_pk, quant) {
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
             cart.event_success('set', data);
       });
   },
    'remove': function(product_pk) {
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
             cart.event_success('remove', data);
       });

   },
    'clear': function() {
        cart.csrf();

        $.ajax({
            url: cart.url,
            type: "POST",
            dataType: 'text'
       })
        .done(function(data) {
             cart.event_success('clear', data);
       });

   },
    'get': function() {
        $.ajax({
            url: cart.url,
            type: "GET",
            dataType: 'text'
       }).done(function(data) {
         alert(data);
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
    'event_success':  function(funct_name='', data) {
        if (funct_name == 'clear') {
            count_cart = 0;
            sum_cart = 0;
       }
        else {
            var obj = $.parseJSON(data);
            count_cart = obj.count_cart;
            sum_cart = obj.sum_cart;
       };

        $('div.cart-count').text(count_cart);
        $('span.sum').text(sum_cart + ' грн');
   }
};


$(document).ready(function() {

    cart.url =$('div#cart').data('url');

    // For cart-display.html
    $('button#remove').on('click', function() {
        var product_pk = this.value;
        cart.remove(product_pk);
   });

    //  For products_list.html and product.html
    $('button#buy').on('click', function() {
        var product_pk = this.value;
        var quant = $(this).data('quant');
        cart.set(product_pk, quant);
        //cart.get()
        //cart.clear()
   });
});