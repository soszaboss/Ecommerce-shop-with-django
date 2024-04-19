from django.db import models
from django.urls import reverse

from category.models import Category
from django.utils.text import slugify


# Create your models here.
class Variant(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    allow_variants = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the instance first so it gets an ID
        if not self.slug:
            self.slug = slugify(f'{self.product_name}-{self.id}')
            super().save(*args, **kwargs)  # Save again to store the generated slug
        if self.stock == 0:
            self.is_available = False
            super().save(*args, **kwargs)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name


class AttributeVariant(models.Model):
    attribut_variant_name = models.CharField(max_length=100, unique=True)
    is_available = models.BooleanField(default=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='variant_attributes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variant_products')
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.product_name}-{self.variant.name}-{self.attribut_variant_name}"

# class ProductVariant(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variant_products')
#     variant = models.ManyToManyField(Variant)
