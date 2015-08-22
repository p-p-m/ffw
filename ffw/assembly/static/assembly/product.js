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
            activeElement: $(this).find('[data-role="configuration-active"]')
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
            totalCount += parseInt(configuration.countElement.val());
            totalPrice += parseInt(configuration.countElement.val()) * configuration.priceForOneConfiguration;
        }
    }
    console.log('ololol!');
    $('[data-role="configurations-total-count"]').text(totalCount);
    $('[data-role="configurations-total-price"]').text(totalPrice);
}

$(document).ready(function() {
    initConfigrations();

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

});
