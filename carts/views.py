from django.shortcuts import render, redirect

from store.models import Product
from .models import CartItem, Cart


# Create your views here.
def _card_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_card(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_card_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_card_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
        cart_item.save()

    return redirect('carts')


def diminue_item(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_card_id(request))
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if cart_item.quantity == 0:
            return redirect('carts')
        else:
            cart_item.quantity -= 1
            cart_item.save()
            return redirect('carts')
    except:
        return redirect('carts')


def index(request, total=0, cart_id=None, quantity=0):
    cart_items = []
    try:
        cart = Cart.objects.get(cart_id=_card_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except Exception as e:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items
    }
    return render(request, template_name="store/cart.html", context=context)
