from django.db import models
from django.urls import reverse


# Model for Days of the Week
class Day(models.Model):
    name = models.CharField(max_length=10)  # e.g., "Monday", "Tuesday", ...

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('menu', args=[str(self.id)])

    @classmethod
    def populate_days(cls):
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day_name in days_of_week:
            cls.objects.get_or_create(name=day_name)


# Model for Meals (Breakfast, Lunch, Dinner)
class Meal(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='meals')
    name = models.CharField(max_length=20)  # e.g., "Breakfast", "Lunch", "Dinner"

    def __str__(self):
        return f"{self.name} on {self.day.name}"

    def get_absolute_url(self):
        return reverse('dishes', args=[str(self.id)])


# Model for Dishes
class Dish(models.Model):
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE, related_name='dishes')
    description = models.TextField(blank=True, null=True)  # Add this line
    name = models.CharField(max_length=100)  # e.g., "Dish 1", "Dish 2", "Dish 3"

    def __str__(self):
        return f"{self.name} for {self.meal.name}"

    def get_absolute_url(self):
        return reverse('category', args=[str(self.id)])


# Model for Products
class Product(models.Model):
    products = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    unit = models.CharField(
        max_length=20,
        choices=[("броя", "броя"),
                 ("гр.", "гр."),
                 ],
        default="гр.",
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f"{self.name} ({self.unit} {self.quantity})"


# Model for Recipes
class Recipe(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=False, null=False, default="Recipe description")
    products = models.ManyToManyField(Product, through='RecipeProduct')

    def __str__(self):
        return f"Recipe for {self.dish.name}"


# Through Model for Recipe Products
class RecipeProduct(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_required = models.DecimalField(max_digits=10, decimal_places=2)  # e.g., required quantity
    unit = models.CharField(
        max_length=20,
        choices=[("броя", "броя"),
                 ("гр.", "гр."),
                 ],
        default="гр.",
    )

    def __str__(self):
        return f"{self.quantity_required} {self.unit} of {self.product.name} for {self.recipe.name}"


# Model for Shopping List
class ShoppingList(models.Model):
    week = models.IntegerField()  # e.g., Week number
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='shopping_lists')
    products_needed = models.ManyToManyField(Product, through='ShoppingListProduct')

    def __str__(self):
        return f"Shopping List for Week {self.week} - {self.day.name}"


# Through Model for Shopping List Products
class ShoppingListProduct(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_available = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_required = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity_required} {self.product.unit} of {self.product.name} for {self.shopping_list.day.name}"
