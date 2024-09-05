from django import template
from django.forms import inlineformset_factory
from .models import Day, Meal, Dish, Recipe, Product, ShoppingList, RecipeProduct, ShoppingListProduct
from django import forms

register = template.Library()


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
        fields = ['name', 'description']
        labels = {'name': 'Ястие',
                  'description': 'Описание'}


class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__clear_fields_helper_text()

        for field_name in ['name', 'description']:
            self.fields[field_name].help_text = None

    def __clear_fields_helper_text(self):
        for field in self.fields.values():
            field.help_text = None
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Recipe
        fields = ['name', 'description']
        labels = {'name': 'Рецепта',
                  'description': 'Описание'}


class RecipeProductForm(forms.ModelForm):
    class Meta:
        model = RecipeProduct
        fields = ['product', 'unit', 'quantity_required']
        labels = {'product': 'Продукт',
                  'unit': 'Мерна Единица',
                  'quantity_required': 'Необходимо Количество'}


# Create an inline formset for RecipeProduct
RecipeProductFormSet = inlineformset_factory(
    Recipe,
    RecipeProduct,
    fields=['product', 'unit', 'quantity_required'],
    labels={'product': 'Продукт',
            'unit': 'Мерна Единица',
            'quantity_required': 'Необходимо Количество'},
    extra=1,
    can_delete=True
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity_in_stock', 'unit']
        labels = {'name': 'Продукт',
                  'quantity_in_stock': 'Количество в наличност',
                  'unit': 'Мерна Единица'}


class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['recipe']


class ShoppingListProductForm(forms.ModelForm):
    class Meta:
        model = ShoppingListProduct
        fields = ['product', 'quantity_available', 'quantity_required']
        labels = {'product': 'Продукт',
                  'quantity_available': 'Налично количество',
                  'quantity_required': 'Необходимо Количество'}