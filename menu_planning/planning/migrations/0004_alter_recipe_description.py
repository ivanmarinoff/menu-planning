# Generated by Django 5.1 on 2024-09-16 13:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("planning", "0003_alter_product_calories_per_100g"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="description",
            field=models.TextField(),
        ),
    ]
