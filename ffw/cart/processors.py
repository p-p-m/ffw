
def cart_processor(request):
    if not 'cart' in request.session:
            request.session['cart'] = {'products': {}, 'total': 0, 'count': 0}
    else:
        if not 'products' in request.session['cart']:
            request.session['cart'] = {'products': {}, 'total': 0, 'count': 0}

    return {'cart': request.session['cart']}
