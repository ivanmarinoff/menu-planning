from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from .models import Day, Meal, Dish, ShoppingList, Recipe, RecipeProduct
from .forms import DishForm, RecipeForm, RecipeProductFormSet
from django.views import generic as views, generic, View
import logging


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
        form.instance.day = Day.objects.get(pk=self.kwargs['pk'])
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
        context['form'] = DishForm()  # Add an empty form to the context
        return context

    def post(self, request, *args, **kwargs):
        form = DishForm(request.POST)
        if form.is_valid():
            dish = form.save(commit=False)
            dish.meal = self.get_object()  # Associate the dish with the meal
            dish.save()
            return redirect(reverse('dishes', kwargs={'pk': self.get_object().id}))
        return self.render_to_response(self.get_context_data(form=form))


class DishCreateView(views.CreateView):
    model = Dish
    template_name = 'dish_form.html'
    fields = ['name', 'description']  # Add any other fields you have in your Dish model

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
            recipe.dish = self.object  # Link the recipe to the current dish
            recipe.save()

            return redirect(reverse('recipe_detail', args=[recipe.id]))

        # If the form is invalid, render the page with errors
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


class AddProductView(views.View):
    template_name = 'recipe_detail.html'

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        formset = RecipeProductFormSet(queryset=RecipeProduct.objects.none())
        return self.render_form(request, recipe, formset)

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        formset = RecipeProductFormSet(request.POST)
        if formset.is_valid():
            products = formset.save(commit=False)
            for product in products:
                product.recipe = recipe
                product.save()
            return redirect(reverse('recipe_detail', args=[pk]))
        return self.render_form(request, recipe, formset)

    def render_form(self, request, recipe, formset):
        return render(request, self.template_name, {
            'recipe': recipe,
            'formset': formset,
        })


class ShoppingListView(views.DetailView):
    model = Day
    template_name = 'shopping_list.html'
    context_object_name = 'day'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week = self.kwargs['week']
        context['shopping_list'] = ShoppingList.objects.filter(week=week, day=self.object).first()
        return context
