from .models import cart, CartItem  # Adjusted import statement to import 'cart' instead of 'Cart'
from .views import _cart_id

def counter(request):
    item_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart_obj = cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart_obj[:1])
            for cart_item in cart_items:
                item_count += cart_item.quantity
        except cart.DoesNotExist:
            item_count = 0
    return {'item_count': item_count}
