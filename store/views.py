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
    single_product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
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

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=single_product, user=request.user)
        else:
            cart_item = CartItem.objects.get(product=single_product, cart__cart_id=_card_id(request))
    except CartItem.DoesNotExist:
        cart_item = None
    cart_exist = True if cart_item else False
    context = {'single_product': single_product, 'cart_exist': cart_exist, '' if not data else 'variant': data,
               '' if not cart_exist else 'cart_item': cart_item}

    return render(request, 'store/product_detail.html', context)

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

    return redirect(product.get_url())

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
        return redirect(product.get_url())
    else:
        cart_item.delete()
        return redirect(product.get_url())

