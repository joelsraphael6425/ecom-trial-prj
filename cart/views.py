from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .models import cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id
    
def add_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect('shop:index')  # Redirect to some appropriate view if the product does not exist

    cart_id = _cart_id(request)
    cart_instance, created = cart.objects.get_or_create(cart_id=cart_id)

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart_instance)  
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart_instance
        )

    return redirect('cart:cart_detail')  # Assuming you have a URL named 'cart_detail' for the cart detail view

def cart_detail(request, total=0, counter=0, cart_items=None):
    cart_instance = get_object_or_404(cart, cart_id=_cart_id(request))

    cart_items = CartItem.objects.filter(cart=cart_instance, active=True)
    for cart_item in cart_items:
        total += cart_item.sub_total()
        counter += cart_item.quantity

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total, 'counter': counter})

def cart_remove(request, product_id):
    cart_obj = cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart_obj)
    if cart_item.quantity > 1:  # Accessing quantity attribute of CartItem object
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')

def full_remove(request, product_id):
    cart_obj = cart.objects.get(cart_id=_cart_id(request))  # Renamed variable to cart_obj
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart_obj)  # Changed variable to cart_obj
    cart_item.delete()
    return redirect('cart:cart_detail')


