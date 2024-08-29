from django import forms, template
from django.forms import inlineformset_factory
register = template.Library()
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
        fields = ['name', 'description']
        labels = {'name': 'Ястие',
                  'description': 'Описание'}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Категория'}


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
        fields = ['product', 'quantity_required', 'unit']
        labels = {'product': 'Продукт',
                  'quantity_required': 'Необходимо Количество',
                  'unit': 'Мерна Единица'}


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
        labels = {'name': 'Продукт',
                  'quantity': 'Количество',
                  'unit': 'Мерна Единица'}


class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['week', 'day', 'products_needed']
