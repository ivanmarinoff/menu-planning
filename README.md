# Meal Planner & Shopping List Application
- This is a Django-based web application for planning meals, managing recipes, and generating shopping lists. 
The application allows users to create meal plans for specific days, assign recipes to those meals, and automatically generate shopping lists based on the required ingredients. It also tracks calories for each product and calculates the total calorie content for each recipe.

## Features
- Day and Meal Management:
Create and manage meals for each day of the week.
Assign recipes to meals and customize the meals for different days.
- Recipe and Ingredient Management:
Add, update, and delete recipes.
Each recipe includes a list of ingredients (products) with their required quantities.
- Shopping List Generator:
Automatically generates a shopping list for each recipe.
Combines products across meals into a summary shopping list, ensuring that repeated products are aggregated with total quantities.
The shopping list also reflects stock available and shortfalls.
- Calorie Tracking:
Products can optionally have calorie information.
Calories are automatically calculated for the total recipe based on product quantities and displayed alongside each ingredient.

## Requirements
- Python 3.x
- Django 3.x or 4.x
- Bootstrap (optional for styling)
- SQLite (default) or any other supported database like PostgreSQL
- 
## Installation
Clone the repository:

```bash
git clone https://github.com/ivanmarinoff/menu-planning.git
cd meal-planner-app
```
## Set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
## Install dependencies:

```bash
pip install -r requirements.txt
```
## Run migrations to set up the database:

```bash
python manage.py migrate
```
## Create a superuser to access the admin panel:

```bash
python manage.py createsuperuser
```
## Run the development server:

```bash
python manage.py runserver
```
## Access the application:

- Open your browser and go to http://127.0.0.1:8000/ to view the app.
- Admin interface: http://127.0.0.1:8000/admin/ for managing products, meals, days, etc.
## Code Structure and Logic
1. Models
- Day: Represents each day of the week and stores the associated meals.
- Meal: Stores the meals for a specific day. Each meal can have multiple dishes (recipes).
- Recipe: Represents a dish with its associated products (ingredients).
- Product: Stores individual products, including optional fields like calories_per_100g for tracking calories.
- RecipeProduct: Acts as a junction table between Recipe and Product, storing the quantity required for each recipe.
- ShoppingList: Automatically generated based on the recipe requirements. If products are not available in stock, they are added to the shopping list.
- ShoppingListProduct: Stores the products that need to be purchased, reflecting the quantity required for the shopping list.
2. Views
- CreateMealView (CBV): Allows users to create a new meal for a selected day. It uses Django's CreateView class and overrides the form_valid method to associate a meal with a specific day.
- RecipeDetailView (CBV): Displays the details of a specific recipe. It shows the list of products in the recipe, calculates the total calories for each product, and generates the shopping list if the required product quantities are unavailable.
- SummaryShoppingListView (CBV): Displays a summary shopping list that combines the required quantities of each product across multiple meals for the week.
3. Forms
- The forms are primarily generated using Django's ModelForm to handle input for the creation and update of meals, recipes, and products. A FormSet is used for adding and managing multiple RecipeProduct entries.
4. Templates
- The templates are built using Django’s template language and Bootstrap for styling.
## Key templates:
- index.html: Displays the days of the week, allowing users to view meals for each day.
- create_meal.html: Allows users to add a meal for a selected day.
- recipe_detail.html: Displays the details of a recipe along with its ingredients and calorie information.
- summary_shopping_list.html: Displays a summary of the shopping list for the week, aggregating product quantities across all meals.
1. Shopping List Logic
- When a user adds a product to a recipe, the system checks the available stock. If the stock is insufficient, the product is added to the shopping list with the required amount.
- If the product exists multiple times in recipes throughout the week, it is summed up in the summary shopping list to avoid duplicate entries.
2. Calorie Calculation
- The calories_per_100g field in the Product model is used to calculate the total calories for each product in a recipe.
- The total calories for a recipe are displayed by multiplying the quantity_required by the calories_per_100g for each product and summing them for all products in the recipe.
Usage
3. Creating a Day and a Meal:
- Use the admin panel or the frontend UI to create new days and add meals for each day.
4. Adding Recipes:
- Recipes consist of products (ingredients) with quantities required.
You can add products via the admin panel, including optional calorie information.
5. Summary Shopping List:
A shopping list is generated for each day based on the recipes associated with meals.
The summary shopping list combines ingredients across all days and ensures that repeated items are aggregated.
6. Calorie Calculation:
- The application calculates calories for each product in a recipe and totals them for the entire recipe.

## Contributing
### Feel free to contribute to this project by submitting a pull request. Any contributions that improve the functionality or performance are welcome.

## License
- This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- This project was inspired by the need for efficient meal planning and grocery shopping.
Special thanks to the Django and Python community for providing robust tools and frameworks.

