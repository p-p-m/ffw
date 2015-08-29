COMMENTS_URL = '/comments/';

var comments = {
    add: function(positive, negative, productId, callback) {
        $.ajax({
            url: COMMENTS_URL,
            type: 'POST',
            data: {
                'positive_sides': positive,
                'negative_sides': negative,
                'product': productId,
            },
        }).done(function(responseData) {
             callback(responseData);
        });
    }
};
