from django.contrib import admin
from .models import Day, Meal, Dish, ShoppingList, Recipe, Product, ShoppingListProduct, RecipeProduct


class DayAdmin(admin.ModelAdmin):
    list_display = ['name']  # This will display the 'name' field in the admin list view


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ['name', 'day']


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'meal']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity_in_stock', 'unit']


@admin.register(ShoppingListProduct)
class ShoppingListProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity_required', 'shopping_list']


class ShoppingListProductInline(admin.TabularInline):
    model = ShoppingListProduct
    extra = 1  # How many rows to show by default


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ['recipe']
    list_filter = ['recipe']
    inlines = [ShoppingListProductInline]


class ShoppingListInline(admin.TabularInline):
    model = ShoppingList
    extra = 1


class RecipeProductInline(admin.TabularInline):
    model = RecipeProduct
    extra = 1  # Number of extra forms to display
    search_fields = ['product']


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'dish', 'description']
    inlines = [RecipeProductInline]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
