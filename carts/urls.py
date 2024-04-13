from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='carts'),
    path('add-cart/<int:product_id>', add_card, name='add_cart'),
    path('diminue-item/<int:product_id>', diminue_item, name='diminue_item')
]
