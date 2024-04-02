from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='store'),
    path('<slug:category_slug>/', index, name='product_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', product_detail, name='product_detail')
]
