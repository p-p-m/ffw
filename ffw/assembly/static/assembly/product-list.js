PRODUCTS_ON_PAGE = 12;  // XXX: Warning: magic number in code: need to change.

var productList = {
    activate: function() {
        // select sort button
        var urlVars = getUrlVars(),
            vm = this,
            productPopup = activatePopUpBySelector($('[data-role="product-popup"]'));
        if ("sort_by" in urlVars) {
            $('[data-role="sort-item"][data-sort="' + urlVars.sort_by + '"]').addClass('active');
        }
        $('[data-role="sort-item"]').click(vm.sort);
        // activate products on page count
        vm.visibleProductsCount = PRODUCTS_ON_PAGE;
        vm.page = 1;
        // activate "show more" button
        $('[data-role="show-more"]').click(function() {
            vm.showMoreProducts();
        });
        // reinit list on view trigger
        $('[data-role="products-view-trigger"]').click(function() {
            vm.visibleProductsCount = PRODUCTS_ON_PAGE;
            vm.page = 1;
            vm.inspectShowMoreButton();
        });

        $('[data-role="buy"]').click(function() {
            $.ajax({
                url: $(this).attr('data-product-url'),
            }).done(function(data) {
                $('[data-role="product-popup"]').html(data);
                productPopup.activate();
                $('[data-role="buy-cancel"]').click(function() {
                    productPopup.deactivate();
                });
                initProductBuyFeatures();
                regularPopup();
                priceInput();
            });
        });

    },

    sort: function() {
        var sort_by = $(this).attr('data-sort');
        url = setGetParameter('sort_by', sort_by);
        window.location.href = url;
    },

    showMoreProducts: function() {
        var url = setGetParameter('view_type', this.getViewType()),
            vm = this;
        url = setGetParameter('page', this.page + 1, url);

        $.ajax({
            url: url,
        }).done(function(data) {
            var table = $('[data-role="products-table"][data-view-type="' + vm.getViewType() + '"]');
            table.html(table.html() + data);
            vm.visibleProductsCount += PRODUCTS_ON_PAGE;
            vm.page += 1;
            vm.inspectShowMoreButton();
        });
    },

    // XXX: think about better name
    inspectShowMoreButton: function() {
        if (this.getProductsCount() <= this.getVisibleProductsCount()) {
            $('[data-role="show-more-block"]').hide();
        } else {
            $('[data-role="show-more-block"]').show();
        }
    },

    // global project count
    setProductsCount: function(count) {
        $('[data-role="count"]').text(count);
    },

    // global projects count
    getProductsCount: function() {
        return parseInt($('[data-role="count"]').text());
    },

    getVisibleProductsCount: function() {
        return this.visibleProductsCount;
    },

    getViewType: function() {
        if (parseInt(localStorage.view, 10) === 0) {
            return 'grid';
        } else {
            return 'list';
        }
    }

};


$(document).ready(function() {
    productList.activate();
    filters.activate(productList.setProductsCount);
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
