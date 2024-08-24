from django.urls import path
from .views import HomeView, MenuView, DishesView, CategoryView, RecipeView, ShoppingListView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('menu/<int:pk>/', MenuView.as_view(), name='menu'),
    path('dishes/<int:pk>/', DishesView.as_view(), name='dishes'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category'),
    path('recipe/<int:pk>/', RecipeView.as_view(), name='recipe'),
    path('shopping_list/<int:week>/<int:pk>/', ShoppingListView.as_view(), name='shopping_list'),
]
