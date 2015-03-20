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

function activateFilters() {
    var urlVars = getUrlVars();
    for (var key in urlVars) {
        if (urlVars.hasOwnProperty(key)) {
            $('[data-role="filter-item"][name=' + key + ']').addClass("active");
        }
    }
}


$(document).ready(function() {

    activateFilters();

    $('[data-role="filter-item"]').on('click', function() {
        var name = $(this).attr("name"),
            url = setGetParameter(name, '1'),
            countUrl = setGetParameter('count', 'on', url);
        window.history.pushState('', '', url);

        $.ajax({
            url: countUrl,
        }).done(function(data) {
            alert(data);
        });
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

});
