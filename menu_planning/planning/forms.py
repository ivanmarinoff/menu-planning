from django import forms
from .models import Day, Meal, Dish, Category, Recipe, Product, ShoppingList


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
        fields = ['category', 'products']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity', 'unit']


class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['week', 'day', 'products_needed']
