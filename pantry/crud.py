
import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Try different import patterns
try:
    from db import pantry_vault
except ImportError:
    try:
        from pantry.db import pantry_vault
    except ImportError:
        print("Error: Cannot import pantry_vault from db module")
        sys.exit(1)

from tabulate import tabulate

class UserCRUD:
    """CRUD operations for user authentication"""
    
    @staticmethod
    def authenticate_user(username, password):
        """Authenticate user login"""
        return pantry_vault.validate_user(username, password)
    
    @staticmethod
    def register_new_user(username, email, password, country_id=None):
        """Register a new user"""
        return pantry_vault.register_user(username, email, password, country_id)
    
    @staticmethod
    def get_current_user():
        """Get current logged-in user"""
        return pantry_vault.get_current_user()
    
    @staticmethod
    def logout_user():
        """Logout current user"""
        pantry_vault.logout()


class CountryCRUD:
    """CRUD operations for countries"""
    
    @staticmethod
    def get_all_countries():
        """Get all countries"""
        query = "SELECT id, name FROM countries ORDER BY name"
        return pantry_vault.execute_query(query)
    
    @staticmethod
    def add_country(name):
        """Add a new country"""
        query = "INSERT INTO countries (name) VALUES (%s)"
        result = pantry_vault.execute_update(query, (name,))
        return result > 0
    
    @staticmethod
    def get_country_by_name(name):
        """Get country by name"""
        query = "SELECT id, name FROM countries WHERE name = %s"
        result = pantry_vault.execute_query(query, (name,))
        return result[0] if result else None


class FoodCRUD:
    """CRUD operations for foods"""
    
    @staticmethod
    def get_all_foods():
        """Get all foods with country information"""
        query = """
            SELECT f.id, f.name, c.name as country, f.description
            FROM foods f
            LEFT JOIN countries c ON f.country_id = c.id
            ORDER BY f.name
        """
        return pantry_vault.execute_query(query)
    
    @staticmethod
    def get_foods_by_country(country_id):
        """Get foods by country"""
        query = """
            SELECT f.id, f.name, f.description, c.name as country
            FROM foods f
            LEFT JOIN countries c ON f.country_id = c.id
            WHERE f.country_id = %s
            ORDER BY f.name
        """
        return pantry_vault.execute_query(query, (country_id,))
    
    @staticmethod
    def add_food(name, country_id, description=""):
        """Add a new food"""
        query = "INSERT INTO foods (name, country_id, description) VALUES (%s, %s, %s)"
        result = pantry_vault.execute_update(query, (name, country_id, description))
        return result > 0
    
    @staticmethod
    def get_food_with_ingredients(food_id):
        """Get food details with ingredients"""
        # Get food details
        food_query = """
            SELECT f.id, f.name, f.description, c.name as country
            FROM foods f
            LEFT JOIN countries c ON f.country_id = c.id
            WHERE f.id = %s
        """
        food_result = pantry_vault.execute_query(food_query, (food_id,))
        
        if not food_result:
            return None
        
        food = food_result[0]
        
        # Get ingredients for this food
        ingredients_query = """
            SELECT i.name, fi.quantity, fi.unit
            FROM ingredients i
            JOIN food_ingredients fi ON i.id = fi.ingredient_id
            WHERE fi.food_id = %s
        """
        ingredients = pantry_vault.execute_query(ingredients_query, (food_id,))
        
        return FoodCRUD.new_method(food, ingredients)

    @staticmethod
    def new_method(food, ingredients):
        food['ingredients'] = ingredients or []
        return food
    
    @staticmethod
    def display_foods_table(foods, title="Foods"):
        """Display foods in a formatted table"""
        if not foods:
            print(f"\nNo {title.lower()} found.")
            return
        
        headers = ["ID", "Name", "Country", "Description"]
        table_data = []
        
        for food in foods:
            description = food.get('description', '')
            if len(description) > 50:
                description = description[:47] + "..."
            
            table_data.append([
                food['id'],
                food['name'],
                food.get('country', 'Unknown'),
                description
            ])
        
        print(f"\n{title}")
        print("=" * 60)
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    @staticmethod
    def display_food_details(food):
        """Display detailed food information with ingredients"""
        if not food:
            print("Food not found.")
            return
        
        print(f"\n{food['name']}")
        print("=" * 50)
        print(f"Country: {food.get('country', 'Unknown')}")
        print(f"Description: {food.get('description', 'No description available')}")
        
        if food.get('ingredients'):
            print(f"\nIngredients:")
            for ingredient in food['ingredients']:
                quantity = ingredient.get('quantity', '')
                unit = ingredient.get('unit', '')
                amount = f"{quantity} {unit}".strip()
                if amount:
                    print(f"  • {ingredient['name']} - {amount}")
                else:
                    print(f"  • {ingredient['name']}")
        else:
            print(f"\nNo ingredients information available")
        
        print("-" * 50)


class RecipeCRUD:
    """CRUD operations for recipes"""
    
    @staticmethod
    def get_all_recipes():
        """Get all recipes with country information"""
        query = """
            SELECT r.id, r.name, c.name as country, r.prep_time, r.cook_time, r.servings
            FROM recipes r
            LEFT JOIN countries c ON r.country_id = c.id
            ORDER BY r.name
        """
        return pantry_vault.execute_query(query)
    
    @staticmethod
    def get_recipe_details(recipe_id):
        """Get detailed recipe information with ingredients"""
        # Get recipe details
        recipe_query = """
            SELECT r.*, c.name as country
            FROM recipes r
            LEFT JOIN countries c ON r.country_id = c.id
            WHERE r.id = %s
        """
        recipe_result = pantry_vault.execute_query(recipe_query, (recipe_id,))
        
        if not recipe_result:
            return None
        
        recipe = recipe_result[0]
        
        # Get ingredients for this recipe
        ingredients_query = """
            SELECT i.name, ri.quantity, ri.unit
            FROM ingredients i
            JOIN recipe_ingredients ri ON i.id = ri.ingredient_id
            WHERE ri.recipe_id = %s
        """
        ingredients = pantry_vault.execute_query(ingredients_query, (recipe_id,))
        
        recipe['ingredients'] = ingredients or []
        return recipe
    
    @staticmethod
    def add_recipe(name, country_id, instructions, prep_time="", cook_time="", servings=None, family_notes="", user_id=None):
        """Add a new recipe and return its ID"""
        query = """
            INSERT INTO recipes (name, country_id, instructions, prep_time, cook_time, servings, family_notes, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        result = pantry_vault.execute_update(query, (name, country_id, instructions, prep_time, cook_time, servings, family_notes, user_id))
        if result > 0:
            get_id_query = "SELECT LAST_INSERT_ID() as id"
            id_result = pantry_vault.execute_query(get_id_query)
            return id_result[0]['id'] if id_result else None
        return None

    @staticmethod
    def delete_recipe(recipe_id, user_id):
        """Delete a recipe only if it belongs to the given user_id"""
        query = "DELETE FROM recipes WHERE id = %s AND user_id = %s"
        result = pantry_vault.execute_update(query, (recipe_id, user_id))
        return result > 0
    
    @staticmethod
    def display_recipes_table(recipes, title="Recipes"):
        """Display recipes in a formatted table"""
        if not recipes:
            print(f"\nNo {title.lower()} found.")
            return
        
        headers = ["ID", "Recipe Name", "Country", "Prep Time", "Cook Time", "Servings"]
        table_data = []
        
        for recipe in recipes:
            table_data.append([
                recipe['id'],
                recipe['name'],
                recipe.get('country', 'Unknown'),
                recipe.get('prep_time', 'N/A'),
                recipe.get('cook_time', 'N/A'),
                recipe.get('servings', 'N/A')
            ])
        
        print(f"\n{title}")
        print("=" * 70)
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    @staticmethod
    def display_recipe_details(recipe):
        """Display detailed recipe information"""
        if not recipe:
            print("Recipe not found.")
            return
        
        print(f"\n{recipe['name']}")
        print("=" * 50)
        print(f"Country: {recipe.get('country', 'Unknown')}")
        print(f"Prep Time: {recipe.get('prep_time', 'N/A')}")
        print(f"Cook Time: {recipe.get('cook_time', 'N/A')}")
        print(f"Servings: {recipe.get('servings', 'N/A')}")
        
        if recipe.get('ingredients'):
            print(f"\nIngredients:")
            for ingredient in recipe['ingredients']:
                quantity = ingredient.get('quantity', '')
                unit = ingredient.get('unit', '')
                amount = f"{quantity} {unit}".strip()
                if amount:
                    print(f"  • {ingredient['name']} - {amount}")
                else:
                    print(f"  • {ingredient['name']}")
        else:
            print(f"\nNo ingredients listed")
        
        print(f"\nInstructions:")
        print(recipe.get('instructions', 'No instructions provided'))
        
        if recipe.get('family_notes'):
            print(f"\nFamily Notes:")
            print(recipe.get('family_notes'))
        
        print("-" * 50)

    @staticmethod
    def add_ingredient_to_recipe(recipe_id, ingredient_id, quantity, unit):
        """Link an ingredient to a recipe with quantity and unit"""
        query = "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES (%s, %s, %s, %s)"
        result = pantry_vault.execute_update(query, (recipe_id, ingredient_id, quantity, unit))
        return result > 0


class IngredientCRUD:
    """CRUD operations for ingredients"""
    
    @staticmethod
    def get_all_ingredients():
        """Get all ingredients"""
        query = "SELECT id, name FROM ingredients ORDER BY name"
        return pantry_vault.execute_query(query)
    
    @staticmethod
    def add_ingredient(name):
        """Add a new ingredient"""
        # Check if ingredient already exists
        check_query = "SELECT id FROM ingredients WHERE name = %s"
        existing = pantry_vault.execute_query(check_query, (name,))
        
        if existing:
            return existing[0]['id']  # Return existing ingredient ID
        
        # Insert new ingredient
        query = "INSERT INTO ingredients (name) VALUES (%s)"
        result = pantry_vault.execute_update(query, (name,))
        
        if result > 0:
            # Get the ID of the newly inserted ingredient
            get_id_query = "SELECT LAST_INSERT_ID() as id"
            id_result = pantry_vault.execute_query(get_id_query)
            return id_result[0]['id'] if id_result else None
        
        return None