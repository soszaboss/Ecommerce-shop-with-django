from django.db import models
from accounts.models import Account
from store.models import Product, AttributeVariant


# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    variant_key = models.CharField(max_length=10, blank=True, unique=False, default=None, null=True)
    variants_attribut = models.ManyToManyField(AttributeVariant)
    is_active = models.BooleanField(default=True)

    @property
    def total(self):
        return self.quantity * self.product.price

    def __str__(self):
        return str(self.product.product_name)


class CartVariant(models.Model):
    cartitem = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='variant')
    variant_key = models.CharField(max_length=250, blank=False, unique=True)
