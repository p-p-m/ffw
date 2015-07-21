function setProductsCount(count) {
    $('[data-role="count"]').text(count);
}

function sort() {
    var value = $(this).attr('data-sort'),
        url = setGetParameter('sort_by', value);

    window.location.href = url;
}

$(document).ready(function() {
    filters.activate(setProductsCount);
    $('[data-role="sort-item"]').click(sort);
});


// XXX: Duplicate: has to be moved to core
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
