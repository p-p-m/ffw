
def cart_processor(request):
    if 'cart' not in request.session:
            request.session['cart'] = {'products': {}, 'total': 0, 'count': 0}
    else:
        if 'products' not in request.session['cart']:
            request.session['cart'] = {'products': {}, 'total': 0, 'count': 0}

    return {'cart': request.session['cart']}
