# Generated by Django 5.0.3 on 2024-04-16 11:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0004_variant_product_allow_variants_attributevariant"),
    ]

    operations = [
        migrations.AddField(
            model_name="attributevariant",
            name="modified_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]