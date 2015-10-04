var configurations = [];


function initSinglePriceCalculation(priceForOneProduct, productPriceElement, productCountElement) {
    productCountElement.on('change', function() {
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
            sumElement: $(this).find($('[data-role="configuration-sum"]')),
            countElement: $(this).find($('[data-role="configuration-count"]')),
            activeElement: $(this).find('[data-role="configuration-active"]'),
            pk: parseInt($(this).attr('data-configuration-id')),
        };
        configuration.activeElement.on('change', function() {
            if ($(this).is(':checked')) {
                if (configuration.countElement.val() == 0) {
                    configuration.countElement.val(1);
                }
            } else {
                configuration.countElement.val(0);
            }
            calculateConfigurationsTotal()
        });
        configuration.countElement.on('change', calculateConfigurationsTotal);
        configurations.push(configuration);
    });
}


function calculateConfigurationsTotal() {
    totalCount = 0;
    totalPrice = 0;
    for (var i = 0; i < configurations.length; i++) {
        configuration = configurations[i];
        configurationSum = parseInt(configuration.countElement.val()) * configuration.priceForOneConfiguration;
        configuration.sumElement.text(configurationSum);
        if (configuration.activeElement.is(':checked')) {
            totalCount += 1;
            totalPrice += configurationSum;
        }
    }
    $('[data-role="configurations-total-count"]').text(totalCount);
    $('[data-role="configurations-total-price"]').text(totalPrice);
}

function addConfigurationsToCart(callback) {
    var selectedConfigurations = {};
    for (var i = 0; i < configurations.length; i++) {
        configuration = configurations[i];
        if (configuration.activeElement.is(':checked')) {
            selectedConfigurations[configuration.pk] = parseInt(configuration.countElement.val());
        }
    }
    if (Object.keys(selectedConfigurations).length !== 0) {
        cart.add(selectedConfigurations, callback);
    } else {
        alert('Нужно выбрать хотя бы одну конфигурацию продукта.');
    }
}


function addProductToCart(callback) {
    var pk = parseInt($('[data-role="product-add-to-cart"]').attr('data-product-pk')),
        count = $('[data-role="product-count"]').val();

    var selectedProduct = {};
    selectedProduct[pk] = count;
    cart.add(selectedProduct, callback);
}

function initProductBuyFeatures() {
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
                configuration.sumElement,
                configuration.countElement
            );
        }

        calculateConfigurationsTotal();
    }

    $('[data-role="configurations-add-to-cart"]').click(function() {
        addConfigurationsToCart(function() {
            localStorage.message = 'Товар успешно добавлен в корзину.';
            location.reload();
        });
    });

    $('[data-role="configurations-buy-in-one-click"]').click(function() {
        addConfigurationsToCart(function() {
            window.location.href = "/cart/order/";
        });
    });

    $('[data-role="product-add-to-cart"]').click(function() {
        addProductToCart(function() {
            localStorage.message = 'Товар успешно добавлен в корзину.';
            location.reload();
        });
    });

    $('[data-role="product-buy-in-one-click"]').click(function() {
        addProductToCart(function() {
            window.location.href = "/cart/order/";
        });
    });
}


$(document).ready(function() {
    initProductBuyFeatures();
    var commentPopup = activatePopUpBySelector($('[data-role="comment-popup"]'));

    // comments
    $('[data-role="add-comment-button"]').click(function() {
        var productId = $('[data-role="product"]').attr('data-product'),
            positive = $('[data-role="comment-positive"]').val(),
            negative = $('[data-role="comment-negative"]').val();
        comments.add(positive, negative, productId, function() {
            var flash = activateFlashPopUp();
            flash.activate('Коментарий успешно отправлен на рассмотрение. Он будет добавлен на сайт в течении нескольких часов.');
        });
        commentPopup.deactivate();
    });

    $('[data-role="show-comment-popup"]').click(function() {
        commentPopup.activate();
    });

    $('[data-role="comment-cancel"]').click(function() {
        commentPopup.deactivate();
    });

});
