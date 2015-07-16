function loadForm(container, callback) {
    var url = container.attr('data-url');
    $.ajax({
        url: url,
    }).done(function(form) {
        container.append(form);
        if (callback) callback(form);
    });
}

function saveForm(form, callback) {
    fields = form.serializeArray();
    var data = {};
    for (var i = 0; i < fields.length; i++) {
        data[fields[i].name] = fields[i].value;
    }
    var url = form.attr('action');
    $.ajax({
        url: url,
        method: 'POST',
        data: data,
    }).done(function(data, code) {
        form.replaceWith(data);
    });
}

$(document).ready(function() {
    var productContainer = $('[data-role="product-container"]'),
        productConfigurationContainer = $('[data-role="product-configurations-container"]');
    loadForm(productContainer);

    $('[data-role="product-form-save"]').click(function() {
        saveForm($('[data-role="product-form"]'));
    });

    // $('[data-role="add-product-configuration"]').click(function() {
    //     loadForm(productContainer);
    // });

});