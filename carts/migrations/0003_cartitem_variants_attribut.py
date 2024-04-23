# Generated by Django 5.0.3 on 2024-04-18 10:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("carts", "0002_alter_cartitem_quantity"),
        ("store", "0008_alter_attributevariant_attribut_variant_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="variants_attribut",
            field=models.ManyToManyField(blank=True, to="store.attributevariant"),
        ),
    ]