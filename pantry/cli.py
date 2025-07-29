import sys
import os
import getpass
from tabulate import tabulate

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Try different import patterns
try:
    from crud import UserCRUD, CountryCRUD, FoodCRUD, RecipeCRUD, IngredientCRUD
except ImportError:
    try:
        from pantry.crud import UserCRUD, CountryCRUD, FoodCRUD, RecipeCRUD, IngredientCRUD
    except ImportError:
        print("Error: Cannot import CRUD classes from crud module")
        print("Please ensure crud.py is in the same directory as this file.")
        sys.exit(1)

class PantryCLI:
    """Main CLI interface for the Pantry application"""
    
    def __init__(self):
        self.running = True
        self.authenticated = False
        self.current_user = None
    
    def display_welcome(self):
        """Display welcome message"""
        print("\n" + "="*60)
        print("WELCOME TO PANTRY - FOOD MANAGEMENT SYSTEM")
        print("="*60)
        print("Discover foods from Rwanda, Ghana, Nigeria, Kenya & more!")
        print("Manage your recipes and explore culinary traditions.")
        print("="*60)
    
    def display_auth_menu(self):
        """Display authentication menu"""
        auth_options = [
            ["1", "Login"],
            ["2", "Register New Account"],
            ["3", "Exit"]
        ]
        
        print("\nAUTHENTICATION")
        print("-" * 30)
        print(tabulate(auth_options, headers=["Option", "Action"], tablefmt="simple"))
        print("-" * 30)
    
    def handle_authentication(self):
        """Handle user authentication"""
        while not self.authenticated and self.running:
            self.display_auth_menu()
            choice = self.get_user_choice("Enter your choice: ", ["1", "2", "3"])
            
            if choice == "1":
                self.login()
            elif choice == "2":
                self.register()
            elif choice == "3":
                print("\nGoodbye!")
                self.running = False
    
    def login(self):
        """Handle user login"""
        print("\nUSER LOGIN")
        print("-" * 20)
        
        try:
            username = input("Username: ").strip()
            if not username:
                print("Username is required.")
                return
            
            password = getpass.getpass("Password: ")
            if not password:
                print("Password is required.")
                return
            
            print("Authenticating...")
            if UserCRUD.authenticate_user(username, password):
                self.authenticated = True
                self.current_user = UserCRUD.get_current_user()
                if self.current_user:
                    print(f"Welcome back, {self.current_user['user_name']}!")
                else:
                    print("Welcome back!")
            else:
                print("Invalid username or password.")
                
        except KeyboardInterrupt:
            print("\nLogin cancelled.")
        except Exception as e:
            print(f"An error occurred during login: {e}")
    
    def register(self):
        """Handle user registration"""
        print("\nUSER REGISTRATION")
        print("-" * 25)
        
        try:
            username = input("Choose a username: ").strip()
            if not username:
                print("Username is required.")
                return
            
            if len(username) < 3:
                print("Username must be at least 3 characters long.")
                return
            
            email = input("Enter your email: ").strip()
            if not email:
                print("Email is required.")
                return
            
            if "@" not in email or "." not in email:
                print("Please enter a valid email address.")
                return
            
            password = getpass.getpass("Choose a password (min 6 characters): ")
            if not password:
                print("Password is required.")
                return
            
            if len(password) < 6:
                print("Password must be at least 6 characters long.")
                return
            
            confirm_password = getpass.getpass("Confirm password: ")
            if password != confirm_password:
                print("Passwords do not match.")
                return
            
            # Optional: Select country
            print("\nSelect your country (optional):")
            countries = CountryCRUD.get_all_countries()
            
            if not countries:
                print("No countries available. You can still register without selecting a country.")
                country_id = None
            else:
                country_options = [["0", "Skip (no country)"]]
                for i, country in enumerate(countries, 1):
                    country_options.append([str(i), country['name']])
                
                print(tabulate(country_options, headers=["Option", "Country"], tablefmt="simple"))
                
                valid_choices = [str(i) for i in range(0, len(countries) + 1)]
                choice = self.get_user_choice("Select country: ", valid_choices)
                
                country_id = None
                if choice != "0":
                    selected_country = countries[int(choice) - 1]
                    country_id = selected_country['id']
            
            print("Registering user...")
            success, message = UserCRUD.register_new_user(username, email, password, country_id)
            if success:
                print(f"✓ {message}")
                # Automatically log in the user after registration
                if UserCRUD.authenticate_user(username, password):
                    self.authenticated = True
                    self.current_user = UserCRUD.get_current_user()
                    print(f"Welcome, {username}! You are now logged in.")
                else:
                    print("Registration succeeded but automatic login failed. Please try logging in manually.")
            else:
                print(f"✗ {message}")
                
        except KeyboardInterrupt:
            print("\nRegistration cancelled.")
        except Exception as e:
            print(f"An error occurred during registration: {e}")
    
    def display_main_menu(self):
        """Display the main menu options"""
        user_info = f"Logged in as: {self.current_user['user_name']}" if self.current_user else ""
        
        menu_options = [
            ["1", "Browse Foods by Country"],
            ["2", "View All Foods"],
            ["3", "View Food Details"],
            ["4", "Add New Food"],
            ["5", "Recipes Menu"],
            ["6", "Ingredients Menu"],
            ["7", "Logout"],
            ["8", "Exit Program"]
        ]
        
        print(f"\nMAIN MENU")
        if user_info:
            print(f"{user_info}")
        print("-" * 40)
        print(tabulate(menu_options, headers=["Option", "Description"], tablefmt="simple"))
        print("-" * 40)
    
    def get_user_choice(self, prompt="Enter your choice: ", valid_choices=None, numeric_only=False):
        """Get user input with validation. If numeric_only is True, only accept numbers."""
        while True:
            try:
                choice = input(f"\n{prompt}").strip()
                if numeric_only and not choice.isdigit():
                    print("Please enter a number.")
                    continue
                if valid_choices and choice not in valid_choices:
                    print(f"Please enter a valid choice: {', '.join(valid_choices)}")
                    continue
                return choice
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                sys.exit(0)
            except EOFError:
                print("\n\nGoodbye!")
                sys.exit(0)
    
    def browse_foods_by_country(self):
        """Handle browsing foods by country"""
        try:
            countries = CountryCRUD.get_all_countries()
            
            if not countries:
                print("No countries found in database.")
                return
            
            print("\nAVAILABLE COUNTRIES")
            print("-" * 30)
            
            country_options = []
            for i, country in enumerate(countries, 1):
                country_options.append([str(i), country['name']])
            
            country_options.append([str(len(countries) + 1), "Back to Main Menu"])
            
            print(tabulate(country_options, headers=["Option", "Country"], tablefmt="simple"))
            
            valid_choices = [str(i) for i in range(1, len(countries) + 2)]
            choice = self.get_user_choice("Select a country: ", valid_choices)
            
            if choice == str(len(countries) + 1):
                return
            
            selected_country = countries[int(choice) - 1]
            foods = FoodCRUD.get_foods_by_country(selected_country['id'])
            
            FoodCRUD.display_foods_table(foods, f"Foods from {selected_country['name']}")
            
            if not foods:
                print("You can add foods for this country using option 4 from the main menu!")
                
        except Exception as e:
            print(f"Error browsing foods by country: {e}")
    
    def view_all_foods(self):
        """Display all foods"""
        try:
            foods = FoodCRUD.get_all_foods()
            FoodCRUD.display_foods_table(foods, "All Foods")
        except Exception as e:
            print(f"Error viewing all foods: {e}")
    
    def view_food_details(self):
        """View detailed food information"""
        try:
            foods = FoodCRUD.get_all_foods()
            
            if not foods:
                print("No foods found.")
                return
            
            FoodCRUD.display_foods_table(foods)
            
            while True:
                food_id_input = input("\nEnter food ID to view details (or 'back' to return): ").strip()
                if food_id_input.lower() == 'back':
                    return
                if not food_id_input.isdigit():
                    print("Please enter a valid numeric food ID.")
                    continue
                food_id = int(food_id_input)
                food = FoodCRUD.get_food_with_ingredients(food_id)
                if food:
                    FoodCRUD.display_food_details(food)
                    break
                else:
                    print("Food not found.")
                
        except Exception as e:
            print(f"Error viewing food details: {e}")
    
    def add_new_food(self):
        """Handle adding new food"""
        print("\nADD NEW FOOD")
        print("-" * 20)
        
        try:
            # Get food name
            name = input("Enter food name: ").strip()
            if not name:
                print("Food name is required.")
                return
            if len(name) < 4:
                print("Food name must be at least 4 characters long.")
                return
            if not all(c.isalpha() or c.isspace() for c in name):
                print("Food name must contain only letters and spaces.")
                return
            
            # Select country
            countries = CountryCRUD.get_all_countries()
            if not countries:
                print("No countries available. Please add a country first.")
                return
                
            print("\nSelect Country:")
            
            country_options = []
            for i, country in enumerate(countries, 1):
                country_options.append([str(i), country['name']])
            country_options.append([str(len(countries) + 1), "Add New Country"])
            
            print(tabulate(country_options, headers=["Option", "Country"], tablefmt="simple"))
            
            valid_choices = [str(i) for i in range(1, len(countries) + 2)]
            choice = self.get_user_choice("Select country: ", valid_choices)
            
            if choice == str(len(countries) + 1):
                # Add new country
                new_country = input("Enter new country name: ").strip()
                if not new_country:
                    print("Country name is required.")
                    return
                if not all(c.isalpha() or c.isspace() for c in new_country):
                    print("Country name must contain only letters and spaces.")
                    return
                
                if CountryCRUD.add_country(new_country):
                    print(f"Country '{new_country}' added successfully!")
                    country = CountryCRUD.get_country_by_name(new_country)
                    if country:
                        country_id = country['id']
                    else:
                        print("Error retrieving new country.")
                        return
                else:
                    print("Failed to add country.")
                    return
            else:
                selected_country = countries[int(choice) - 1]
                country_id = selected_country['id']
            
            # Get description
            while True:
                description = input("Enter description (optional): ").strip()
                if description and description[0].isdigit():
                    print("Description should not start with a number. Please re-enter.")
                    continue
                break
            
            # Add food to database
            if FoodCRUD.add_food(name, country_id, description):
                print(f"✓ Food '{name}' added successfully!")
            else:
                print(f"✗ Failed to add food '{name}'.")
                
        except Exception as e:
            print(f"Error adding new food: {e}")
    
    def ingredients_menu(self):
        """Handle ingredients submenu"""
        while True:
            try:
                print("\nINGREDIENTS MENU")
                print("-" * 30)
                
                ingredient_options = [
                    ["1", "View All Ingredients"],
                    ["2", "Add New Ingredient"],
                    ["3", "Back to Main Menu"]
                ]
                
                print(tabulate(ingredient_options, headers=["Option", "Action"], tablefmt="simple"))
                
                choice = self.get_user_choice("Enter your choice: ", ["1", "2", "3"])
                
                if choice == "1":
                    self.view_all_ingredients()
                elif choice == "2":
                    self.add_new_ingredient()
                elif choice == "3":
                    break
                    
            except Exception as e:
                print(f"Error in ingredients menu: {e}")
    
    def view_all_ingredients(self):
        """Display all ingredients"""
        try:
            ingredients = IngredientCRUD.get_all_ingredients()
            
            if not ingredients:
                print("\nNo ingredients found.")
                return
            
            headers = ["ID", "Ingredient Name"]
            table_data = [[ing['id'], ing['name']] for ing in ingredients]
            
            print("\nAll Ingredients")
            print("=" * 40)
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
        except Exception as e:
            print(f"Error viewing ingredients: {e}")
    
    def add_new_ingredient(self):
        """Handle adding new ingredient"""
        try:
            print("\nADD NEW INGREDIENT")
            print("-" * 25)
            while True:
                name = input("Enter ingredient name: ").strip()
                if not name:
                    print("Ingredient name is required.")
                    continue
                if name.isdigit():
                    print("Ingredient name cannot be only numbers.")
                    continue
                if name[0].isdigit():
                    print("Ingredient name cannot start with a number.")
                    continue
                break
            ingredient_id = IngredientCRUD.add_ingredient(name)
            if ingredient_id:
                print(f"✓ Ingredient '{name}' added successfully!")
            else:
                print(f"✗ Failed to add ingredient '{name}'.")
        except Exception as e:
            print(f"Error adding ingredient: {e}")
    
    def recipes_menu(self):
        """Handle recipes submenu"""
        while True:
            try:
                print("\nRECIPES MENU")
                print("-" * 30)
                
                recipe_options = [
                    ["1", "View All Recipes"],
                    ["2", "View Recipe Details"],
                    ["3", "Add New Recipe"],
                    ["4", "Delete My Recipe"],
                    ["5", "Back to Main Menu"]
                ]
                
                print(tabulate(recipe_options, headers=["Option", "Action"], tablefmt="simple"))
                
                choice = self.get_user_choice("Enter your choice: ", ["1", "2", "3", "4", "5"])
                
                if choice == "1":
                    self.view_all_recipes()
                elif choice == "2":
                    self.view_recipe_details()
                elif choice == "3":
                    self.add_new_recipe()
                elif choice == "4":
                    self.delete_my_recipe()
                elif choice == "5":
                    break
                    
            except Exception as e:
                print(f"Error in recipes menu: {e}")
    
    def view_all_recipes(self):
        """Display all recipes"""
        try:
            recipes = RecipeCRUD.get_all_recipes()
            RecipeCRUD.display_recipes_table(recipes)
        except Exception as e:
            print(f"Error viewing recipes: {e}")
    
    def view_recipe_details(self):
        """Display detailed recipe information"""
        try:
            recipes = RecipeCRUD.get_all_recipes()
            
            if not recipes:
                print("No recipes found.")
                return
            
            RecipeCRUD.display_recipes_table(recipes)
            
            recipe_id_input = input("\nEnter recipe ID to view details (or 'back' to return): ").strip()
            
            if recipe_id_input.lower() == 'back':
                return
            
            try:
                recipe_id = int(recipe_id_input)
                recipe = RecipeCRUD.get_recipe_details(recipe_id)
                if recipe:
                    RecipeCRUD.display_recipe_details(recipe)
                else:
                    print("Recipe not found.")
            except ValueError:
                print("Please enter a valid recipe ID.")
                
        except Exception as e:
            print(f"Error viewing recipe details: {e}")
    
    def add_new_recipe(self):
        """Handle adding a new recipe"""
        print("\nADD NEW RECIPE")
        print("-" * 20)
        try:
            # Get recipe name with validation
            while True:
                name = input("Enter recipe name: ").strip()
                if not name:
                    print("Recipe name is required.")
                    continue
                if len(name) < 4:
                    print("Recipe name must be at least 4 characters long.")
                    continue
                if name.isdigit():
                    print("Recipe name cannot be only numbers.")
                    continue
                if name[0].isdigit():
                    print("Recipe name cannot start with a number.")
                    continue
                if not all(c.isalpha() or c.isspace() for c in name):
                    print("Recipe name must contain only letters and spaces.")
                    continue
                break
            # Select country
            countries = CountryCRUD.get_all_countries()
            if not countries:
                print("No countries available. Please add a country first.")
                return
            print("\nSelect Country:")
            country_options = []
            for i, country in enumerate(countries, 1):
                country_options.append([str(i), country['name']])
            country_options.append([str(len(countries) + 1), "Add New Country"])
            print(tabulate(country_options, headers=["Option", "Country"], tablefmt="simple"))
            valid_choices = [str(i) for i in range(1, len(countries) + 2)]
            while True:
                choice = self.get_user_choice("Select country: ", valid_choices, numeric_only=True)
                if choice == str(len(countries) + 1):
                    # Add new country
                    new_country = input("Enter new country name: ").strip()
                    if not new_country:
                        print("Country name is required.")
                        continue
                    if CountryCRUD.add_country(new_country):
                        print(f"Country '{new_country}' added successfully!")
                        country = CountryCRUD.get_country_by_name(new_country)
                        if country:
                            country_id = country['id']
                        else:
                            print("Error retrieving new country.")
                            return
                    else:
                        print("Failed to add country.")
                        return
                    break
                else:
                    selected_country = countries[int(choice) - 1]
                    country_id = selected_country['id']
                    break
            # Get recipe details
            print("\nEnter recipe details:")
            # Description validation
            while True:
                instructions = input("Instructions (required): ").strip()
                if not instructions:
                    print("Instructions are required.")
                    continue
                if instructions.isdigit():
                    print("Instructions cannot be only numbers.")
                    continue
                if instructions[0].isdigit():
                    print("Instructions cannot start with a number.")
                    continue
                break
            # Prep time validation
            while True:
                prep_time = input("Preparation time (e.g., '30 minutes'): ").strip()
                if not prep_time:
                    break
                if prep_time.isdigit():
                    print("Preparation time cannot be only numbers.")
                    continue
                if prep_time[0].isdigit():
                    print("Preparation time cannot start with a number.")
                    continue
                break
            # Cook time validation
            while True:
                cook_time = input("Cooking time (e.g., '45 minutes'): ").strip()
                if not cook_time:
                    break
                if cook_time.isdigit():
                    print("Cooking time cannot be only numbers.")
                    continue
                if cook_time[0].isdigit():
                    print("Cooking time cannot start with a number.")
                    continue
                break
            # Servings validation
            while True:
                servings_input = input("Number of servings (optional): ").strip()
                if not servings_input:
                    servings = None
                    break
                if not servings_input.isdigit() or int(servings_input) <= 0:
                    print("Please enter a valid positive integer for servings.")
                    continue
                servings = int(servings_input)
                break
            family_notes = input("Family notes/story (optional): ").strip()
            # Add recipe to database
            user_id = self.current_user['id'] if self.current_user and 'id' in self.current_user else None
            recipe_id = RecipeCRUD.add_recipe(name, country_id, instructions, prep_time, cook_time, servings, family_notes, user_id)
            if recipe_id:
                print(f"✓ Recipe '{name}' added successfully!")
                print("\nNow, let's add ingredients to your recipe.")
                while True:
                    ing_name = input("Ingredient name (leave blank to finish): ").strip()
                    if not ing_name:
                        break
                    if len(ing_name) < 2:
                        print("Ingredient name must be at least 2 characters long.")
                        continue
                    if ing_name.isdigit():
                        print("Ingredient name cannot be only numbers.")
                        continue
                    if ing_name[0].isdigit():
                        print("Ingredient name cannot start with a number.")
                        continue
                    if not all(c.isalpha() or c.isspace() for c in ing_name):
                        print("Ingredient name must contain only letters and spaces.")
                        continue
                    while True:
                        quantity = input("Quantity (e.g., 2): ").strip()
                        if not quantity:
                            print("Quantity is required.")
                            continue
                        try:
                            float(quantity)
                            break
                        except ValueError:
                            print("Please enter a valid number for quantity.")
                    unit = input("Unit (e.g., cups, tbsp): ").strip()
                    ingredient_id = IngredientCRUD.add_ingredient(ing_name)
                    if ingredient_id:
                        if RecipeCRUD.add_ingredient_to_recipe(recipe_id, ingredient_id, quantity, unit):
                            print(f"✓ Added {quantity} {unit} {ing_name} to recipe.")
                        else:
                            print(f"✗ Failed to link ingredient '{ing_name}' to recipe.")
                    else:
                        print(f"✗ Failed to add ingredient '{ing_name}'.")
                print("All ingredients added!")
            else:
                print(f"✗ Failed to add recipe '{name}'.")
        except Exception as e:
            print(f"Error adding recipe: {e}")
    
    def delete_my_recipe(self):
        """Allow the user to delete their own recipe by ID"""
        try:
            user_id = self.current_user['id'] if self.current_user and 'id' in self.current_user else None
            if not user_id:
                print("User ID not found. Cannot delete recipes.")
                return
            recipes = RecipeCRUD.get_all_recipes()
            my_recipes = [r for r in recipes if r.get('user_id') == user_id]
            if not my_recipes:
                print("You have no recipes to delete.")
                return
            RecipeCRUD.display_recipes_table(my_recipes, title="Your Recipes")
            recipe_ids = [str(r['id']) for r in my_recipes]
            while True:
                recipe_id = input("Enter the ID of the recipe to delete (or 'back' to cancel): ").strip()
                if recipe_id.lower() == 'back':
                    return
                if not recipe_id.isdigit():
                    print("Please enter a valid numeric recipe ID.")
                    continue
                if recipe_id not in recipe_ids:
                    print("Invalid recipe ID.")
                    continue
                if RecipeCRUD.delete_recipe(int(recipe_id), user_id):
                    print("Recipe deleted successfully!")
                else:
                    print("Failed to delete recipe. Make sure you own this recipe.")
                break
        except Exception as e:
            print(f"Error deleting recipe: {e}")
    
    def logout(self):
        """Handle user logout"""
        try:
            if self.current_user:
                print(f"\nGoodbye, {self.current_user['user_name']}!")
            else:
                print("\nGoodbye!")
            UserCRUD.logout_user()
            self.authenticated = False
            self.current_user = None
        except Exception as e:
            print(f"Error during logout: {e}")
            self.authenticated = False
            self.current_user = None
    
    def run(self):
        """Main application loop"""
        try:
            self.display_welcome()
            
            # Handle authentication first
            self.handle_authentication()
            
            # Main application loop (only if authenticated)
            while self.running and self.authenticated:
                self.display_main_menu()
                choice = self.get_user_choice("Enter your choice: ", ["1", "2", "3", "4", "5", "6", "7", "8"])
                
                if choice == "1":
                    self.browse_foods_by_country()
                elif choice == "2":
                    self.view_all_foods()
                elif choice == "3":
                    self.view_food_details()
                elif choice == "4":
                    self.add_new_food()
                elif choice == "5":
                    self.recipes_menu()
                elif choice == "6":
                    self.ingredients_menu()
                elif choice == "7":
                    self.logout()
                    if self.running:  # Only continue if user didn't exit
                        self.handle_authentication()  # Go back to login
                elif choice == "8":
                    print("\nThank you for using Pantry! Goodbye!")
                    self.running = False
                
                if self.running and self.authenticated:
                    input("\nPress Enter to continue...")
                    
        except KeyboardInterrupt:
            print("\n\nApplication interrupted by user. Goodbye!")
            self.running = False
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            import traceback
            traceback.print_exc()

# CLI instance
cli = PantryCLI()
