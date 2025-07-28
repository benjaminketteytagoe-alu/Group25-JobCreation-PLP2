import os     # for working with files and folders

import random # to randomly pick recipe
import json # for working with JSON data
# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECIPE_FOLDER = os.path.join(BASE_DIR, "recipes")  # Folder to store recipe files

class recipeManager:
    def __init__(self,country_name):
        # Store the country name and set the path for its recipe file
        self.country_name = country_name
        self.recipe_folder = os.path.join(RECIPE_FOLDER,  f"{country_name.lower()}.json")
        self.recipes = []
        self.load_recipes()     # Load any existing recipes from file
        if not os.path.exists(RECIPE_FOLDER):
            os.makedirs(RECIPE_FOLDER)      # Create the recipes folder if it doesn't exist

    def load_recipes(self):
        # Load recipes from the corresponding country's JSON file
        if os.path.exists(self.recipe_folder):
            with open(self.recipe_folder, 'r') as file:
                self.recipes = json.load(file)
        else:
            self.recipes = []
            print(f"Recipe file for {self.country_name} not found.")
    def save_recipes(self):
        # Save all recipes to the country's JSON file
        with open(self.recipe_folder, 'w') as file:
            json.dump(self.recipes, file, indent=4)
            print(f"Recipes saved to {self.recipe_folder}")

    def add_recipe(self, name, ingredients, instructions, cook_time):
        # Add a new recipe to the manager and save it
        recipe = {
            "name": name,
            "ingredients": ingredients,
            "instructions": instructions,
            "cook_time": cook_time
        }
        self.recipes.append(recipe)
        self.save_recipes()

    def search_recipe(self):
        # Search for a recipe by name (case-insensitive)
        name = input("Enter the name of the recipe to search: ")
        found_recipes = [recipe for recipe in self.recipes if recipe['name'].lower() == name.lower()]
        if found_recipes:
            for recipe in found_recipes:
                print(f"   {recipe['name']}")
                print(f"   Ingredients: {', '.join(recipe['ingredients'])}")
                print(f"   Instructions: {recipe['instructions']}")
                print(f"   Cook Time: {recipe['cook_time']}")
                print("=" * 40)
        else:
            print(f"No recipes found with the name '{name}'.")

    def random_recipe(self):
        # Display a random recipe from the list
        if not self.recipes:
            print("No recipes available to choose from.")
            return
        recipe = random.choice(self.recipes)
        print(f"==={recipe['name']}===")
        print(f"Ingredients: {', '.join(recipe['ingredients'])}")
        print("steps:")
        for i, step in enumerate(recipe['instructions'].split('\n'), start=1):
            print(f"{i}: {step}")
        print(f"Cook Time: {recipe['cook_time']}")
        print("=" * 40)

    def list_recipe(self):
        # List all recipes for the country
        if not self.recipes:
            print("No recipes available.")
        else:
            print(f"Recipes for {self.country_name}:")
            for recipe in self.recipes:
                print(f"==={recipe['name']}===")
                print(f"Ingredients: {', '.join(recipe['ingredients'])}")
                print("steps:")
                for i, step in enumerate(recipe['instructions'].split('\n'), start=1):
                    print(f"{i}: {step}")
                print(f"Cook Time: {recipe['cook_time']}")
                print("=" * 40)