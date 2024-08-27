from django import forms
from django.forms import inlineformset_factory

from .models import Day, Meal, Dish, Category, Recipe, Product, ShoppingList, RecipeProduct


class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ['name']


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['day', 'name']


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['meal', 'name']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['dish', 'name']


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description']


class RecipeProductForm(forms.ModelForm):
    class Meta:
        model = RecipeProduct
        fields = ['product', 'quantity_required', 'unit']


# Create an inline formset for RecipeProduct
RecipeProductFormSet = inlineformset_factory(
    Recipe,
    RecipeProduct,
    form=RecipeProductForm,
    extra=1,
    can_delete=True
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity', 'unit']


class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['week', 'day', 'products_needed']
