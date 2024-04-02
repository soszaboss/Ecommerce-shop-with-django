from django.shortcuts import render
from store.models import Product
def home(request):
    product = Product.objects.all().filter(is_available=True)
    count = Product.objects.all().count()
    context = {'products': product, 'count': count}
    return render(request, 'index.html', context)