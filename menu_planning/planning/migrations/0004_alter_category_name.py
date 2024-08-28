# Generated by Django 5.1 on 2024-08-28 09:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("planning", "0003_recipe_description_recipe_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                choices=[
                    ("Месо", "Месо"),
                    ("Риба", "Риба"),
                    ("Млечни продукти", "Млечни продукти"),
                    ("Зърнени храни", "Зърнени храни"),
                    ("Плодове и зеленчуци", "Плодове и зеленчуци"),
                    ("Добавки/Сосове", "Добавки/Сосове"),
                    ("Други", "Други"),
                ],
                max_length=30,
            ),
        ),
    ]
