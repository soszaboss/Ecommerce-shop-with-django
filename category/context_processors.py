from .models import Category
from django.utils.timezone import datetime


def menu_nav_link(request):
    links = Category.objects.all()
    return dict(links=links, year=datetime.now().year)
