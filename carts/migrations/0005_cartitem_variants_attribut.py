# Generated by Django 5.0.3 on 2024-04-19 09:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("carts", "0004_remove_cartitem_variants_attribut"),
        ("store", "0008_alter_attributevariant_attribut_variant_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="variants_attribut",
            field=models.ManyToManyField(to="store.attributevariant"),
        ),
    ]
