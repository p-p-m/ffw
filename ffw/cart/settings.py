from django.conf import settings

USER_CART_SETTINGS = getattr(settings, 'CART_SETTINGS',{})

CART_SETTINGS = {
    'model_name': USER_CART_SETTINGS.get('model_name', 'Product'),
    'app_name': USER_CART_SETTINGS.get('app_name', 'products'),
    'price_field_name': USER_CART_SETTINGS.get('price_field_name', 'price_uah'),
    'code_field_name': USER_CART_SETTINGS.get('code_field_name', 'code'),
    'name_field_name': USER_CART_SETTINGS.get('name_field_name', 'name')
}
