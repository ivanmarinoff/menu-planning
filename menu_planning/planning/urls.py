from django.urls import path
from .views import HomeView, MenuView, DishesView, CategoryView, RecipeView, ShoppingListView, CreateMealView, \
    DishCreateView, DishUpdateView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('menu/<int:pk>/', MenuView.as_view(), name='menu'),
    path('meal/<int:pk>/dishes/', DishesView.as_view(), name='dishes'),
    path('meal/<int:meal_id>/dish/add/', DishCreateView.as_view(), name='add_dish'),
    path('dish/<int:pk>/edit/', DishUpdateView.as_view(), name='edit_dish'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category'),
    path('recipe/<int:pk>/', RecipeView.as_view(), name='recipe'),
    path('shopping_list/<int:week>/<int:pk>/', ShoppingListView.as_view(), name='shopping_list'),
    path('day/<int:pk>/create-meal/', CreateMealView.as_view(), name='create_meal'),
]
