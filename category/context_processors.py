from .models import Category


def menu_nav_link(request):
    links = Category.objects.all()
    return dict(links=links)
