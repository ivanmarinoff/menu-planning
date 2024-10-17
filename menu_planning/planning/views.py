from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView

from .models import Day, Meal, Dish, ShoppingList, Recipe, ShoppingListProduct
from .forms import DishForm, RecipeForm, RecipeProductFormSet
from django.views import generic as views

from ..users.mixins import CustomLoginRequiredMixin, ErrorRedirectMixin

User = get_user_model()


class HomeView(ErrorRedirectMixin, views.ListView):
    model = Day
    template_name = 'index.html'
    context_object_name = 'days'


class MenuView(CustomLoginRequiredMixin, ErrorRedirectMixin, views.DetailView):
    model = Day
    template_name = 'menu.html'
    context_object_name = 'day'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meals'] = self.object.meals.all()
        return context

    @staticmethod
    def get_success_url(self, pk):
        return reverse('menu', args=[pk])


class CreateMealView(CustomLoginRequiredMixin, ErrorRedirectMixin, views.CreateView):
    model = Meal
    template_name = 'create_meal.html'
    fields = ['name']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].label = 'Ястие'
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['day'] = Day.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        day = Day.objects.get(pk=self.kwargs['pk'])
        form.instance.day = day
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('menu', args=[self.kwargs['pk']])


class DishesView(CustomLoginRequiredMixin, ErrorRedirectMixin, views.DetailView):
    model = Meal
    template_name = 'dishes.html'
    context_object_name = 'meal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dishes'] = self.object.dishes.all()
        context['form'] = DishForm()
        return context

    def post(self, request, *args, **kwargs):
        form = DishForm(request.POST)
        if form.is_valid():
            dish = form.save(commit=False)
            dish.meal = self.get_object()
            dish.save()
            return redirect(reverse('dishes', kwargs={'pk': self.get_object().id}))
        return self.render_to_response(self.get_context_data(form=form))


class DishCreateView(CustomLoginRequiredMixin, ErrorRedirectMixin, views.CreateView):
    model = Dish
    template_name = 'dish_form.html'
    fields = ['name', 'description']

    def form_valid(self, form):
        meal_id = self.kwargs.get('meal_id')
        form.instance.meal = Meal.objects.get(pk=meal_id)
        return super().form_valid(form)

    def get_success_url(self):
        meal_id = self.kwargs.get('meal_id')
        return reverse('dishes', args=[meal_id], kwargs={'pk': meal_id})


class DishUpdateView(CustomLoginRequiredMixin, ErrorRedirectMixin, views.UpdateView):
    model = Dish
    template_name = 'dish_form.html'
    fields = ['name', 'description']

    def get_success_url(self):
        return reverse('dishes', args=[self.object.meal.id], kwargs={'pk': self.object.meal.id})


class RecipeListView(CustomLoginRequiredMixin, ErrorRedirectMixin, views.DetailView):
    model = Dish
    template_name = 'recipe.html'
    context_object_name = 'dish'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = self.object.recipes.all()
        context['form'] = RecipeForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = RecipeForm(request.POST)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.dish = self.object
            recipe.save()

            return redirect(reverse('recipe_detail', args=[recipe.id]), kwargs={'pk': recipe.id})

        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class RecipeDetailView(CustomLoginRequiredMixin, ErrorRedirectMixin, views.DetailView):
    model = Recipe
    template_name = 'recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.object.recipeproduct_set.all()

        # Calculate total calories for the recipe
        total_calories = 0
        products_with_calories = []

        for product in products:
            # Calculate calories for each product
            if product.product.calories_per_100g and product.unit == 'гр.':
                calories = (product.quantity_required / 100) * product.product.calories_per_100g
                calories = round(calories, 2)  # Round to two decimal places
            else:
                calories = 0

            products_with_calories.append({
                'product': product,
                'calories': calories
            })

            total_calories += calories

        context['formset'] = RecipeProductFormSet(queryset=products)
        context['total_calories'] = total_calories
        context['products_with_calories'] = products_with_calories
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        formset = RecipeProductFormSet(request.POST)

        if formset.is_valid():
            products = formset.save(commit=False)

            # Create or get the shopping list for the current recipe
            shopping_list, created = ShoppingList.objects.get_or_create(recipe=self.object)

            for product in products:
                product.recipe = self.object
                warehouse_product = product.product

                # If there is not enough stock in the warehouse
                if warehouse_product.quantity_in_stock >= product.quantity_required:
                    # Subtract the required quantity from stock
                    warehouse_product.quantity_in_stock -= product.quantity_required
                else:
                    # Calculate the shortage (quantity_required - quantity_in_stock)
                    shortage = product.quantity_required - warehouse_product.quantity_in_stock

                    # Add the shortage to the shopping list
                    shopping_list_product, _ = ShoppingListProduct.objects.get_or_create(
                        shopping_list=shopping_list,
                        product=warehouse_product,
                        defaults={
                            'quantity_available': warehouse_product.quantity_in_stock,
                            'quantity_required': shortage,
                        }
                    )

                    # If product already exists in shopping list, update the required quantity
                    if not _:
                        shopping_list_product.quantity_required += shortage
                        shopping_list_product.save()

                    # Set the warehouse product stock to 0
                    warehouse_product.quantity_in_stock = 0

                warehouse_product.save()
                product.save()

            # After saving products, recalculate total calories for the recipe
            total_calories = sum(
                (product.quantity_required / 100) * product.product.calories_per_100g
                for product in self.object.recipeproduct_set.all()
                if product.product.calories_per_100g and product.unit == 'гр.'
            )

            # Redirect with updated calorie data
            return redirect('recipe_detail', pk=self.object.pk)

        context = self.get_context_data(formset=formset)
        return self.render_to_response(context)


class ShoppingListView(CustomLoginRequiredMixin, ErrorRedirectMixin, views.ListView):
    model = ShoppingList
    template_name = 'shopping_list.html'
    context_object_name = 'shopping_lists'

    def get_queryset(self):
        day_id = self.kwargs.get('day_id')
        return ShoppingList.objects.filter(recipe__dish__meal__day_id=day_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        day_id = self.kwargs.get('day_id')
        context['day'] = get_object_or_404(Day, pk=day_id)
        return context


class SummaryShoppingListView(CustomLoginRequiredMixin, ErrorRedirectMixin, TemplateView):
    template_name = 'summary_shopping_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Aggregate products from all shopping lists, summing their quantities
        summary = (
            ShoppingListProduct.objects
            .values('product__name', 'product__unit')
            .annotate(total_quantity=Sum('quantity_required'))
            .order_by('product__name')
        )

        context['summary'] = summary
        return context


class DeleteMenuView(CustomLoginRequiredMixin, ErrorRedirectMixin, views.DeleteView):
    model = Day
    template_name = 'confirm_delete.html'  # Add a template for confirmation
    context_object_name = 'menu'

    def get_success_url(self):
        # Redirect to home or some other page after the menu is deleted
        return reverse('home')


class DeleteMealView(CustomLoginRequiredMixin, ErrorRedirectMixin, views.DeleteView):
    model = Meal
    template_name = 'confirm_delete.html'  # Add a template for confirmation
    context_object_name = 'meal'

    def get_success_url(self):
        # Redirect to the menu page after meal deletion
        return reverse('menu', args=[self.object.day.id])


class DeleteRecipeView(CustomLoginRequiredMixin, ErrorRedirectMixin, views.DeleteView):
    model = Recipe
    template_name = 'confirm_delete.html'  # Add a template for confirmation
    context_object_name = 'recipe'

    def get_success_url(self):
        # Redirect to the dishes page after recipe deletion
        return reverse('dishes', args=[self.object.dish.meal.id])
