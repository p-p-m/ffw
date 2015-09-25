$(document).ready(function() {
    $("[data-role='section-filter']").change(function() {
        var value = parseInt($(this).find(":selected").attr('data-value')),
            url = removeGetParameter('subcategory__category', removeGetParameter('subcategory'));
        if (value !== 0) {
            window.location.href = setGetParameter('subcategory__category__section', value, url);
        } else {
            window.location.href = removeGetParameter('subcategory__category__section', url);
        }
    });

    $("[data-role='category-filter']").change(function() {
        var value = parseInt($(this).find(":selected").attr('data-value')),
            url = removeGetParameter('subcategory');
        if (value !== 0) {
            window.location.href = setGetParameter('subcategory__category', value, url);
        } else {
            window.location.href = removeGetParameter('subcategory__category', url);
        }
    });

    $("[data-role='subcategory-filter']").change(function() {
        var value = parseInt($(this).find(":selected").attr('data-value'));
        if (value !== 0) {
            window.location.href = setGetParameter('subcategory', value);
        } else {
            window.location.href = removeGetParameter('subcategory');
        }
    });

});


function setGetParameter(paramName, paramValue, url) {
    // returns current url with additional get parameter
    url = url || window.location.href;
    if (url.indexOf(paramName + '=') >= 0)
    {
        var prefix = url.substring(0, url.indexOf(paramName + '=')),
        suffix = url.substring(url.indexOf(paramName + '='));

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

function removeGetParameter(parameter, url) {
    url = url || window.location.href;
    //prefer to use l.search if you have a location/link object
    var urlparts = url.split('?');
    if (urlparts.length>=2 && urlparts[1]) {

        var prefix= encodeURIComponent(parameter)+'=';
        var pars= urlparts[1].split(/[&;]/g);

        //reverse iteration as may be destructive
        for (var i= pars.length; i-- > 0;) {
            //idiom for string.startsWith
            if (pars[i].lastIndexOf(prefix, 0) !== -1) {
                pars.splice(i, 1);
            }
        }
        url = urlparts[0];
        if (pars.length !== 0) {
            url +='?' + pars.join('&');
        }
        return url;
    } else {
        return url;
    }
}