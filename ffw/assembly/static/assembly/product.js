var configurations = [];


function initSinglePriceCalculation(priceForOneProduct, productPriceElement, productCountElement) {
    productCountElement.on('input', function() {
        productPriceElement.text(priceForOneProduct * $(this).val());
    });
    if (productCountElement.val() > 1) {
        productPriceElement.text(priceForOneProduct * productCountElement.val());
    }
}

function initConfigrations() {
    $('[data-role="configuration"]').each(function() {
        var configuration = {
            priceForOneConfiguration: parseFloat($(this).find($('[data-role="configuration-price"]')).text()),
            active: $(this).find('[data-role="configuration-active"]').is(':checked'),
            priceElement: $(this).find($('[data-role="configuration-price"]')),
            countElement: $(this).find($('[data-role="configuration-count"]')),
            activeElement: $(this).find('[data-role="configuration-active"]'),
            pkElement: $(this).find($('[data-role="config-pk"]')).text()
        };
        configuration.activeElement.on('change', calculateConfigurationsTotal);
        configuration.countElement.on('input', calculateConfigurationsTotal);
        configurations.push(configuration);
    });
}

function calculateConfigurationsTotal() {
    totalCount = 0;
    totalPrice = 0;
    for (var i = 0; i < configurations.length; i++) {
        configuration = configurations[i];
        if (configuration.activeElement.is(':checked')) {
            totalCount += 1;
            totalPrice += parseInt(configuration.countElement.val()) * configuration.priceForOneConfiguration;
        }
    }
    $('[data-role="configurations-total-count"]').text(totalCount);
    $('[data-role="configurations-total-price"]').text(totalPrice);
}

$(document).ready(function() {
    initConfigrations();
    var commentPopup = activatePopUpBySelector($('[data-role="comment-popup"]'));

    cart.url =$('div#cart').data('url');

    if (configurations.length === 0) {
        // product without configurations
        var productCountElement = $('[data-role="product-count"]'),
            productPriceElement = $('[data-role="product-price"]');

        initSinglePriceCalculation(
            parseFloat(productPriceElement.text()), productPriceElement, productCountElement);
    } else {
        // product with configurations
        for (var i=0; i<configurations.length; i++) {
            configuration = configurations[i];
            initSinglePriceCalculation(
                configuration.priceForOneConfiguration,
                configuration.priceElement,
                configuration.countElement
            );
        }

        calculateConfigurationsTotal();
    }
    // comments
    $('[data-role="add-comment-button"]').click(function() {
        var productId = $('[data-role="product"]').attr('data-product'),
            positive = $('[data-role="comment-positive"]').val(),
            negative = $('[data-role="comment-negative"]').val();
        comments.add(positive, negative, productId, function() {
            alert('Коментарий успешно отправлен на рассмотрение. Он будет добавлен на сайт в течении нескольких часов');
        });
        commentPopup.deactivate();
    });

    $('[data-role="show-comment-popup"]').click(function() {
        commentPopup.activate();
    });

    $('[data-role="comment-cancel"]').click(function() {
        commentPopup.deactivate();
    });

    $('[data-role="add-cart"]').on("click", function() {
        var productDict = {}
        for (var i = 0; i < configurations.length; i++) {
            configuration = configurations[i];

            if (configuration.activeElement.is(':checked')) {console.log('i1- ', typeof(configuration).pkElement, parseInt(configuration.countElement.val()))
               productDict[configuration.pkElement] = parseInt(configuration.countElement.val())
            };
        };
        console.log(productDict)
        cart.add(productDict);
    });

    $('button#print').on("click", function() {
         console.log( cart.count, " - ", cart.total);
    });

    $('button#clear').on("click", function() {
          cart.clear();
    });

});
