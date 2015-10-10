COMMENTS_URL = '/comments/';

var comments = {
    add: function(username, comments, positive, negative, productId, callback) {
        $.ajax({
            url: COMMENTS_URL,
            type: 'POST',
            data: {
                'username': username,
                'comments': comments,
                'positive_sides': positive,
                'negative_sides': negative,
                'product': productId,
            },
        }).done(function(responseData) {
             callback(responseData);
        });
    }
};
