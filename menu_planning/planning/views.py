from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Day, Meal, Dish, Category, ShoppingList
from .forms import DishForm, CategoryForm
import logging


class HomeView(ListView):
    model = Day
    template_name = 'index.html'
    context_object_name = 'days'


class MenuView(DetailView):
    model = Day
    template_name = 'menu.html'
    context_object_name = 'day'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meals'] = self.object.meals.all()
        return context


class CreateMealView(CreateView):
    model = Meal
    template_name = 'create_meal.html'
    fields = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['day'] = Day.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        day = Day.objects.get(pk=self.kwargs['pk'])
        print(f"Creating meal for day: {day}")  # Debugging line
        form.instance.day = Day.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('menu', args=[self.kwargs['pk']])


class DishesView(DetailView):
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


class DishCreateView(CreateView):
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


class DishUpdateView(UpdateView):
    model = Dish
    template_name = 'dish_form.html'
    fields = ['name', 'description']

    def get_success_url(self):
        return reverse('dishes', args=[self.object.meal.id])



class CategoryView(DetailView):
    model = Dish
    template_name = 'category.html'
    context_object_name = 'dish'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.object.categories.all()
        context['form'] = CategoryForm(initial={'dish': self.object})
        return context

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('category', args=[self.get_object().id]))
        return self.render_to_response(self.get_context_data(form=form))


class RecipeView(DetailView):
    model = Category
    template_name = 'recipe.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = self.object.recipes.all()
        return context


class ShoppingListView(DetailView):
    model = Day
    template_name = 'shopping_list.html'
    context_object_name = 'day'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week = self.kwargs['week']
        context['shopping_list'] = ShoppingList.objects.filter(week=week, day=self.object).first()
        return context