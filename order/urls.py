from django.urls import path
from .views import place_order, create_order, capture_order
urlpatterns = [
    path('place-order', place_order, name='place-order'),
    path('api/orders/', create_order, name='order'),
    path('api/orders/<str:order_id>/capture/', capture_order, name='capture'),
]