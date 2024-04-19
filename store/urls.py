from django.urls import path
from .views import index,product_detail,add_card,diminue_item

urlpatterns = [
    path('', index, name='store'),
    path('<slug:category_slug>/', index, name='product_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', product_detail, name='product_detail'),
    path('add-cart/<int:product_id>', add_card, name='add_cart'),
    path('diminue-item/<int:product_id>', diminue_item, name='diminue_item'),
]
