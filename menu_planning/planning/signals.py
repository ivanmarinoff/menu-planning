from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver

from menu_planning.planning.models import ShoppingList, Recipe, ShoppingListItem, Day


@receiver(post_save, sender=Recipe)
def create_shopping_list(sender, instance, created, **kwargs):
    if created:
        shopping_list = ShoppingList.objects.create(recipe=instance)
        for recipe_product in instance.recipeproduct_set.all():
            ShoppingListItem.objects.create(
                shopping_list=shopping_list,
                product=recipe_product.product,
                quantity=recipe_product.quantity_required,
                unit=recipe_product.unit
            )


@receiver(post_migrate)
def populate_days_after_migration(sender, **kwargs):
    Day.populate_days()
