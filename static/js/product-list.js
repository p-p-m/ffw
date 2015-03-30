function setGetParameter(paramName, paramValue, url) {
    // returns current url with additional get parameter
    url = url || window.location.href;
    if (url.indexOf(paramName + '=') >= 0)
    {
        var prefix = url.substring(0, url.indexOf(paramName)),
        suffix = url.substring(url.indexOf(paramName));

        suffix = suffix.substring(suffix.indexOf('=') + 1);
        suffix = (suffix.indexOf('&') >= 0) ? suffix.substring(suffix.indexOf('&')) : '';
        url = prefix + paramName + '=' + paramValue + suffix;
    } else {
        if (url.indexOf('?') < 0) {
            url += '?' + paramName + '=' + paramValue;
        } else {
            url += '&' + paramName + '=' + paramValue;
        }
    }
    return url;
}

function executeSearchForm() {
    var url = window.location.href.split('?')[0] + '?' + $('form#search-form').serialize(),
        countUrl = setGetParameter('count', 'on', url);
    window.history.pushState('', '', url);
    $.ajax({
        url: countUrl,
    }).done(function(data) {
        $('div#search-count').text(data);
    });
}

$(document).ready(function() {
    $('form#search-form input').on('change', function() {
        executeSearchForm();
    });

    $('form#search-form input[type="number"]').on('keyup', function() {
        executeSearchForm();
    });

    $('select#paginate-by').on('change', function() {
        var selected = $(this).find(":selected").text(),
            url = setGetParameter('paginate_by', selected);
        window.location.href = url;
    });

    $('select#id_sort_by').on('change', function() {
        var selected = $(this).find(":selected").attr('value');
        window.location.href = (window.location.href.split('?')[0] + '?' +
            $('form#search-form').serialize() + '&sort_by=' + selected);
    });

    cart.fulling();

    $('button#product_add').on('click', function() {
        var product_code = this.value; 
        cart.cart_change(product_code);    
    });
    
    $('button#go_cart').on('click', function() {
        document.location.href = "http://" + document.location.host + '/products/cart/cart/';
    });

});
