from django.views.generic import ListView, DetailView
from .models import Day, Meal, Dish, Category, ShoppingList
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


class DishesView(DetailView):
    model = Meal
    template_name = 'dishes.html'
    context_object_name = 'meal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dishes'] = self.object.dishes.all()
        return context


class CategoryView(DetailView):
    model = Dish
    template_name = 'category.html'
    context_object_name = 'dish'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.object.categories.all()
        return context


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
