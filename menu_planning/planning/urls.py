from django.urls import path
from ..users.views import RegisterUserView, LoginUserView, LogoutUserView
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('menu/<int:pk>/', views.MenuView.as_view(), name='menu'),
    path('meal/<int:pk>/dishes/', views.DishesView.as_view(), name='dishes'),
    path('meal/<int:meal_id>/dish/add/', views.DishCreateView.as_view(), name='add_dish'),
    path('dish/<int:pk>/edit/', views.DishUpdateView.as_view(), name='edit_dish'),
    path('recipes/<int:pk>/recipes/', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('shopping_list/<int:day_id>/', views.ShoppingListView.as_view(), name='shopping_list'),
    path('day/<int:pk>/create-meal/', views.CreateMealView.as_view(), name='create_meal'),
    path('summary_shopping_list/', views.SummaryShoppingListView.as_view(), name='summary_shopping_list'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]
