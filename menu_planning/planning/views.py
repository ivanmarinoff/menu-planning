from django.db.models import Sum
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView

from .models import Day, Meal, Dish, ShoppingList, Recipe, ShoppingListProduct
from .forms import DishForm, RecipeForm, RecipeProductFormSet, ShoppingListProductForm
from django.views import generic as views


class HomeView(views.ListView):
    model = Day
    template_name = 'index.html'
    context_object_name = 'days'


class MenuView(views.DetailView):
    model = Day
    template_name = 'menu.html'
    context_object_name = 'day'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meals'] = self.object.meals.all()
        return context


class CreateMealView(views.CreateView):
    model = Meal
    template_name = 'create_meal.html'
    fields = ['name']

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


class DishesView(views.DetailView):
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


class DishCreateView(views.CreateView):
    model = Dish
    template_name = 'dish_form.html'
    fields = ['name', 'description']

    def form_valid(self, form):
        meal_id = self.kwargs.get('meal_id')
        form.instance.meal = Meal.objects.get(pk=meal_id)
        return super().form_valid(form)

    def get_success_url(self):
        meal_id = self.kwargs.get('meal_id')
        return reverse('dishes', args=[meal_id])


class DishUpdateView(views.UpdateView):
    model = Dish
    template_name = 'dish_form.html'
    fields = ['name', 'description']

    def get_success_url(self):
        return reverse('dishes', args=[self.object.meal.id])


class RecipeListView(views.DetailView):
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

            return redirect(reverse('recipe_detail', args=[recipe.id]))

        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class RecipeDetailView(views.DetailView):
    model = Recipe
    template_name = 'recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = RecipeProductFormSet(queryset=self.object.recipeproduct_set.all())
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

            return redirect('recipe_detail', pk=self.object.pk)

        context = self.get_context_data(formset=formset)
        return self.render_to_response(context)


class ShoppingListView(views.ListView):
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


class SummaryShoppingListView(TemplateView):
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

