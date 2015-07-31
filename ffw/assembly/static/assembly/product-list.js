function setProductsCount(count) {
    $('[data-role="count"]').text(count);
}

function sort() {
    var value = $(this).attr('data-sort'),
        url = setGetParameter('sort_by', value);

    window.location.href = url;
}

function activateSortItem() {
    var urlVars = getUrlVars();
    if ("sort_by" in urlVars) {
        $('[data-role="sort-item"][data-sort="' + urlVars.sort_by + '"]').addClass('active');
    }
}

function activateProductsView() {
    var urlVars = getUrlVars();
    if ("view" in urlVars) {
        console.log('QQQ' + urlVars.view);
        $('[data-role="products-view-trigger"]').filter(':first').click();
        var viewContainer = $('[data-role="products-view"]');
        viewContainer.filter(function(index) { return index === 1; }).show();
        ProductsViewType(1);
    }
}

$(document).ready(function() {
    filters.activate(setProductsCount);
    $('[data-role="sort-item"]').click(sort);
    activateSortItem();
    activateProductsView();
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

// XXX: Duplicate: has to be moved to core
// Read a page's GET URL variables and return them as an associative array.
function getUrlVars()
{
    if (window.location.href.indexOf('?') == -1) {
        return {};
    }
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars[hash[0]] = hash[1];
    }
    return vars;
}
