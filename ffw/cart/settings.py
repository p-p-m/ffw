from django.conf import settings

USER_CART_SETTINGS = getattr(settings, 'CART_SETTINGS')

CART_SETTINGS = {
     'product_model': USER_CART_SETTINGS.get('product_model', 'products.Product')
     'price_field':  USER_CART_SETTINGS.get('price_field', 'price_uah')
 }
