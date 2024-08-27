from django.contrib import admin
from .models import Day, Meal, Dish, Category, ShoppingList, Recipe, Product, ShoppingListProduct, RecipeProduct


class DayAdmin(admin.ModelAdmin):
    list_display = ['name']  # This will display the 'name' field in the admin list view


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ['name', 'day']


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'meal']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'dish']  # Display the name and dish fields in the list view
    list_filter = ['name', 'dish']  # Add filters for name and dish
    search_fields = ['name', 'dish__name']  # Enable searching by category name and dish name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'unit']


@admin.register(ShoppingListProduct)
class ShoppingListProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity_required', 'shopping_list']


class ShoppingListProductInline(admin.TabularInline):
    model = ShoppingList.products_needed.through
    extra = 1  # How many rows to show by default


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ['week', 'day']  # Display the week number and day in the list view
    list_filter = ['week', 'day']  # Add filters for week and day
    search_fields = ['week', 'day__name']  # Enable searching by week and day name
    inlines = [ShoppingListProductInline]  # Inline for managing related products


class RecipeProductInline(admin.TabularInline):
    model = RecipeProduct
    extra = 1  # How many extra empty rows to display
    min_num = 1  # Minimum number of rows
    max_num = 10  # Maximum number of rows


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['category']  # Display the category in the list view
    list_filter = ['category']  # Add filters for category
    search_fields = ['category__name']  # Enable searching by category name
    inlines = [RecipeProductInline]  # Inline for managing related products


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
