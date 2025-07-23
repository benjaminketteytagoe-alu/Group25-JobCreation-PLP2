import os     # for working with files and folders

import random # to randomly pick recipe
RECIPE_FOLDER = "recipes"  # Folder to store recipe files
import json # for working with JSON data


class recipeManager:
    def __init__(self,country_name):
        self.country_name = country_name
        self.recipe_folder = os.path.join(RECIPE_FOLDER,  f"{country_name.lower()}.json")
        self.recipes = []
        self.load_recipes()
        if not os.path.exists(RECIPE_FOLDER):
            os.makedirs(RECIPE_FOLDER)

    def load_recipes(self):
        if os.path.exists(self.recipe_folder):
            with open(self.recipe_folder, 'r') as file:
                self.recipes = json.load(file)
        else:
            self.recipes = []
            print(f"Recipe file for {self.country_name} not found.")
    def save_recipes(self):
        with open(self.recipe_folder, 'w') as file:
            json.dump(self.recipes, file, indent=4)
            print(f"Recipes saved to {self.recipe_folder}")

    def add_recipe(self, name, ingredients, instructions, cook_time):
        recipe = {
            "name": name,
            "ingredients": ingredients,
            "instructions": instructions,
            "cook_time": cook_time
        }
        self.recipes.append(recipe)
        self.save_recipes()
        name = input("Enter the name of the recipe: ")
        ingredients = input("Enter ingredients (comma separated): ").split(',')
        steps = input("Enter cooking steps (type 'done' to finish): ")
        steps = []
        while steps.lower() != 'done':
            steps.append(steps)
            steps = input("Enter next step (type 'done' to finish): ")
        instructions = "\n".join(steps)   
        cook_time = input("Enter cooking time: ")

    def search_recipe(self):
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
        if not self.recipes:
            print("No recipes available to choose from.")
            return
        recipe = random.choice(self.recipes)
        print(f"   Random Recipe: {recipe['name']}")
        print(f"   Ingredients: {', '.join(recipe['ingredients'])}")
        print(f"   Instructions: {recipe['instructions']}")
        print(f"   Cook Time: {recipe['cook_time']}")

    def list_recipe(self):
        if not self.recipes:
            print("No recipes available.")
        else:
            print(f"Recipes for {self.country_name}:")
            for recipe in self.recipes:
                print(f"   {recipe['name']}")
                print(f"   Ingredients: {', '.join(recipe['ingredients'])}")
                print(f"   Instructions: {recipe['instructions']}")
                print(f"   Cook Time: {recipe['cook_time']}")
                print("=" * 40)