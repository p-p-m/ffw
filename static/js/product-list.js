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


