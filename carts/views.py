from django.shortcuts import render, redirect, get_object_or_404

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

    if request.method == 'POST':
        attribut_variation = []
        for key in request.POST:
            value = request.POST[key]
            if key != "csrfmiddlewaretoken":
                attribut_variation.append(value)
        attribut_variation.sort()  # Ensure consistent order
        variant_key = ",".join(attribut_variation)  # Create a unique key
        print(attribut_variation)
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product, variant_key=variant_key)
            cart_item.quantity += 1
            cart_item.save()
            cart_item.variants_attribut.add(*attribut_variation)
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart=cart, product=product, variant_key=variant_key, quantity=1)
            cart_item.save()
            cart_item.variants_attribut.add(*attribut_variation)
    else:
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += 1
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
    cart_item.save()
    return redirect('cart:carts')


def diminue_item(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_card_id(request))
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if cart_item.quantity == 0:
            return redirect('cart:carts')
        else:
            cart_item.quantity -= 1
            cart_item.save()
            return redirect('cart:carts')
    except:
        return redirect('cart:carts')


def delete_card(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_card_id(request))
        count = CartItem.objects.all().filter(cart=cart).count()
        # print(count)
        cart_item = CartItem.objects.get(cart=cart, product=product)
    except CartItem.DoesNotExist:
        return redirect('cart:carts')
    else:
        cart_item.delete()
        if count == 0:
            cart.delete()
        return redirect('cart:carts')
def delete_variant_card(request, product_id, key):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_card_id(request))
        count = CartItem.objects.all().filter(cart=cart).count()
        # print(count)
        cart_item = CartItem.objects.get(cart=cart, product=product, variant_key=key)
    except CartItem.DoesNotExist:
        return redirect('cart:carts')
    else:
        cart_item.delete()
        if count == 0:
            cart.delete()
        return redirect('cart:carts')


def index(request, total=0, cart_id=None, quantity=0):
    cart_items = []
    try:
        cart = Cart.objects.get(cart_id=_card_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('-id')
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


def add_variant_card(request, product_id, key):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_card_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_card_id(request))
        cart.save()
    cart_item = get_object_or_404(CartItem, cart=cart, product=product, variant_key=key)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:carts')


def diminue_variant_item(request, product_id, key):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_card_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_card_id(request))
        cart.save()
    cart_item = get_object_or_404(CartItem, cart=cart, product=product, variant_key=key)
    if cart_item.quantity == 0:
        return redirect('cart:carts')
    else:
        cart_item.quantity -= 1
        cart_item.save()
        return redirect('cart:carts')
