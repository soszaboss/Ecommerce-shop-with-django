from .models import Cart, CartItem
from .views import _card_id


def cart_counter(request):
    count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart = Cart.objects.filter(cart_id=_card_id(request))
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for item in cart_items:
                count += item.quantity
        except Cart.DoesNotExist:
            count = 0
    return dict(count_item=count)
