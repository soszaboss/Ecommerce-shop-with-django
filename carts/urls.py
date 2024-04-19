from django.urls import path
from .views import *

app_name = 'cart'
urlpatterns = [
    path('', index, name='carts'),
    path('add-cart/<int:product_id>', add_card, name='add_cart'),
    path('diminue-item/<int:product_id>', diminue_item, name='diminue_item'),
    path('delete-item/<int:product_id>', delete_card, name='delete_card'),
    path('delete-item/<int:product_id>/<str:key>', delete_variant_card, name='delete_variant_card'),
    path('add-variant-cart/<int:product_id>/<str:key>', add_variant_card, name='add_variant_card'),
    path('diminue-variant-item/<int:product_id>/<str:key>', diminue_variant_item, name='diminue_variant_item'),

]
