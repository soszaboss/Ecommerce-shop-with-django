from django.contrib.auth.decorators import login_required
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
            if request.user.is_authenticated:
                cart_items = CartItem.objects.get(user=request.user, product=product, variant_key=variant_key)
            else:
                cart_item = CartItem.objects.get(cart=cart, product=product, variant_key=variant_key, user=None)
            cart_item.quantity += 1
            cart_item.save()
            cart_item.variants_attribut.add(*attribut_variation)
        except CartItem.DoesNotExist:
            if request.user.is_authenticated:
                cart_items = CartItem.objects.create(user=request.user, product=product, variant_key=variant_key,quantity=1)
            else:
                cart_item = CartItem.objects.create(cart=cart, product=product, variant_key=variant_key, quantity=1)
            cart_item.save()
            cart_item.variants_attribut.add(*attribut_variation)
    else:
        try:
            if request.user.is_authenticated:
                cart_item = CartItem.objects.get(user=request.user, product=product)
            else:
                cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += 1
        except CartItem.DoesNotExist:
            if request.user.is_authenticated:
                cart_item = CartItem.objects.create(user=request.user, product=product, quantity=1)
            else:
                cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
    cart_item.save()
    return redirect('cart:carts')


def diminue_item(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(user=request.user, product=product)
        else:
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
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(user=request.user, product=product)
            count = CartItem.objects.all().filter(user=request.user).count()
        else:
            cart = Cart.objects.get(cart_id=_card_id(request))
            cart_item = CartItem.objects.get(cart=cart, product=product)
            count = CartItem.objects.all().filter(cart=cart).count()
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
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(user=request.user, product=product, variant_key=key)
            count = CartItem.objects.all().filter(user=request.user).count()
        else:
            cart = Cart.objects.get(cart_id=_card_id(request))
            cart_item = CartItem.objects.get(cart=cart, product=product, variant_key=key)
            count = CartItem.objects.all().filter(cart=cart).count()
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
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True).order_by('-id')
            print(cart_item)
        else:
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
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, user=request.user, product=product, variant_key=key)
    else:
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
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, user=request.user, product=product, variant_key=key)
    else:
        cart_item = get_object_or_404(CartItem, cart=cart, product=product, variant_key=key)
    if cart_item.quantity == 0:
        return redirect('cart:carts')
    else:
        cart_item.quantity -= 1
        cart_item.save()
        return redirect('cart:carts')

@login_required
def checkout(request, total=0, cart_id=None, quantity=0):
    cart_items = []
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.filter(user=request.user, is_active=True).order_by('-id')
        else:
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
    return render(request, 'store/checkout.html', context)
