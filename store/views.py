from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product
from category.models import Category
from carts.models import CartItem, Cart
from carts.views import _card_id


# verifie si une categorie spécifique a été inserer dans l'url.
def index(request, category_slug=None):
    # si non récupère tous les produits disponibles si aucune categorie n'a été demanndée
    if not category_slug:
        products = Product.objects.all().filter(is_available=True)
        paginator = Paginator(products, 3)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
    else:
        # ici récupère tous les produits disponibles d'une categorie demanndée
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 3)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
    count = products.count()
    context = {'products': page, 'count': count}
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(slug=product_slug, category__slug=category_slug)
        data = {}
        if single_product.allow_variants:
            variants = single_product.variant_products.all()
            differents_variants = set(var.variant.name for var in variants)
            for _ in differents_variants:
                var_data = []
                for variant in variants:
                    if variant.variant.name == _:
                        var_data.append(variant)
                data[_] = var_data

    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    else:
        try:
            cart = CartItem.objects.get(product=single_product, cart__cart_id=_card_id(request), variant_key=None)
        except CartItem.DoesNotExist:
            cart = None
        cart_exist = True if cart else False
        context = {'single_product': single_product, 'cart_exist': cart_exist, '' if not data else 'variant': data,
                   '' if not cart_exist else 'cart_item': cart}

    return render(request, 'store/product_detail.html', context)


def add_card(request, product_id):
    # if request.method == 'POST':
    #     for item in request.POST:
    #         key = item
    #         value = request.POST[key]
    #         print(value)
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

    return redirect(product.get_url())


def diminue_item(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_card_id(request))
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if cart_item.quantity == 0:
            return redirect(product.get_url())
        else:
            cart_item.quantity -= 1
            cart_item.save()
            return redirect(product.get_url())
    except:
        return redirect(product.get_url())
