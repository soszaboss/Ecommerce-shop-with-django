from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category


# Create your views here.
def index(request, category_slug=None):
    if not category_slug:
        products = Product.objects.all().filter(is_available=True)
    else:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    count = products.count()
    context = {'products': products, 'count': count}
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(slug=product_slug, category__slug=category_slug)
    except Product.DoesNotExist:
        raise  Http404("Product does not exist")
    else:
        context = {'single_product': single_product}

    return render(request, 'store/product_detail.html', context)
