from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from store.models import Product


def home(request):
    product = Product.objects.all().filter(is_available=True)
    count = Product.objects.all().count()
    context = {'products': product, 'count': count}
    return render(request, 'index.html', context)


def search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        products = Product.objects.all().filter(Q(product_name__icontains=q) | Q(description__icontains=q))
        if products:
            paginator = Paginator(products, 3)
            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)
            count = products.count()
            context = {'products': page, 'count': count, 'q': q}
        else:
            context = {'products': {}, 'count': 0}
        return render(request, 'store/store.html', context)

