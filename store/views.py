from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product
from category.models import Category
from carts.models import CartItem
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
        cart = CartItem.objects.filter(product=single_product, cart__cart_id=_card_id(request)).exists()
    except Product.DoesNotExist:
        raise  Http404("Product does not exist")
    else:
        context = {'single_product': single_product, 'cart_exist':cart}

    return render(request, 'store/product_detail.html', context)

