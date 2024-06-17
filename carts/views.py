from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from order.forms import OrderForm
from store.models import Product
from .models import CartItem, Cart


# Create your views here.
def _card_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_card(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = _card_id(request)

    attribut_variation = [value for key, value in request.POST.items() if key != "csrfmiddlewaretoken"]
    attribut_variation.sort()  # Ensure consistent order
    variant_key = ",".join(attribut_variation)  # Create a unique key

    cart_item_defaults = {'quantity': 1}
    if attribut_variation:
        cart_item_defaults['variant_key'] = variant_key

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            user=request.user,
            defaults=cart_item_defaults,
        )
    else:
        cart, created = Cart.objects.get_or_create(cart_id=cart_id)
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            defaults=cart_item_defaults,
            cart=cart,
        )

    if not created:
        cart_item.quantity += 1
        cart_item.save(update_fields=['quantity'])

    if attribut_variation:
        # Assuming variants_attribut is a ManyToManyField or similar
        cart_item.variants_attribut.add(*attribut_variation)

    return redirect('cart:carts')

def diminue_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, user=request.user, product=product)
    else:
        cart = _card_id(request)
        cart_item = get_object_or_404(CartItem, cart__cart_id=cart, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        return redirect('cart:carts')
    else:
        cart_item.delete()
        return redirect('cart:carts')

def delete_card(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, user=request.user, product=product)
        # count = get_object_or_404(CartItem).objects.filter(user=request.user).count()
    else:
        cart = _card_id(request)
        cart_item = get_object_or_404(CartItem, cart__cart_id=cart, product=product)
        # count = get_object_or_404(CartItem).objects.filter(cart=cart).count()
    cart_item.delete()
    return redirect('cart:carts')


def delete_variant_card(request, product_id, key):

    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(user=request.user, product=product, variant_key=key)
            # count = CartItem.objects.all().filter(user=request.user).count()
        else:

            cart = Cart.objects.get(cart_id=_card_id(request))
            cart_item = CartItem.objects.get(cart__cart_id=cart, product=product, variant_key=key)
            count = CartItem.objects.all().filter(cart__cart_id=cart).count()
            if count == 0:
                cart.delete()
    except CartItem.DoesNotExist:
        return redirect('cart:carts')
    else:
        cart_item.delete()
        return redirect('cart:carts')


def index(request):
    total = 0
    quantity = 0
    # cart_items = []

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True).order_by('-id')
    else:
        cart, created = Cart.objects.get_or_create(cart_id=_card_id(request))
        cart_items = CartItem.objects.filter(cart__cart_id=cart, is_active=True).order_by('-id')

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items
    }
    return render(request, 'cart/cart.html', context)





def add_variant_card(request, product_id, key):

    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, user=request.user, product=product, variant_key=key)
    else:
        cart, created = Cart.objects.get_or_create(cart_id=_card_id(request))
        cart_item = get_object_or_404(CartItem, cart__cart_id=cart, product=product, variant_key=key)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:carts')


def diminue_variant_item(request, product_id, key):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, user=request.user, product=product, variant_key=key)
    else:
        cart, created = Cart.objects.get_or_create(cart_id=_card_id(request))
        cart_item = get_object_or_404(CartItem, cart__cart_id=cart, product=product, variant_key=key)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:carts')

@login_required
def checkout(request, total=0, cart_id=None, quantity=0):
    cart_items = []
    form = OrderForm()
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True).order_by('-id')
    else:
        cart = Cart.objects.get(cart_id=_card_id(request))
        cart_items = CartItem.objects.filter(cart__cart_id=cart, is_active=True).order_by('-id')
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'form': form
    }
    return render(request, 'cart/checkout.html', context)
