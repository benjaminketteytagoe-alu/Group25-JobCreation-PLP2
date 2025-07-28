from recipeManager import recipeManager

# List of countries to choose from by default
def pantry_vault():
    countries = ["Rwanda", "Ghana", "Nigeria"]
    print("=" * 40)
    print("   Welcome to the Pantry Vault!  ")
    print(" Discover and Share Global Recipes ")
    print("=" * 40)

    while True:
        # Display list of countries and options
        print("\nSelect a country to explore recipes:")
        for i, country in enumerate(countries, start=1):
            print(f"{i}. {country.title()}")
        print(f"{len(countries) + 1}. Add new country")
        print(f"{len(countries) + 2}. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == str(len(countries) + 2):
            # Exit the program
            print("Exiting the Pantry Vault. Goodbye!")
            break
        elif choice == str(len(countries) + 1):
            # Option to add a new country
            new_country = input("Enter the name of new country: ").strip()
            # Only add if it's not a duplicate and not empty
            if new_country and new_country.title() not in [i.title() for i in countries]:
                countries.append(new_country)
                print(f"{new_country.title()} added successfully!")
            else:
                print("The country name already exist")
            continue
        try:
            choice = int(choice)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if choice < 1 or choice > len(countries):
            print("Invalid choice. Please select a valid country.")
            continue
        # Launch the country menu for the selected country
        selected_country = countries[choice - 1]
        manager = recipeManager(selected_country)
        country_menu(manager, selected_country)

def country_menu(manager, country_name):
    while True:
        # Show the country-specific menu options
        print(f"\nRecipes for {country_name.title()}:")
        print("1. Add Recipe")
        print("2. Search Recipe")
        print("3. Random Recipe")
        print("4. list Recipes")
        print("5. Back to country selection")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == '1':
            # Add a new recipe
            name = input("Enter the name of the recipe: ")
            ingredients = input("Enter ingredients (comma separated): ").split(',')
            steps = []
            # Collect cooking steps until user types 'done'
            step = input("Enter cooking step (type 'done' to finish): ")
            while step.lower() != 'done':
                steps.append(step)
                step = input("Enter next step (type 'done' to finish): ")
            instructions = "\n".join(steps)
            cook_time = input("Enter cooking time: ")
            manager.add_recipe(name, ingredients, instructions, cook_time)
            print("Recipe added successfully!")
            # Ask user if they want to add another recipe or exit to the menu
            print("\nWhat would you like to do next?")
            print("1. Add another recipe")
            print("2. Exit to country menu")
            next_action = input("Enter your choice: ").strip()
            if next_action == '1':
                continue    # Add another recipe
            elif next_action == '2':
                break   # Exit to country menu
            else:
                print("Invalid choice. Returning to country menu.")
                break

        elif choice == '2':
            # Search for a recipe by name   
            manager.search_recipe()
        elif choice == '3':
            # Show a random recipe
            manager.random_recipe()
        elif choice == '4':
            # List all recipes for this country
            manager.list_recipe()
        elif choice == '5':
            # Back to main country selection
            break
        elif choice == '6':
            # Exit the whole program
            print("Exiting the Pantry Vault. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    pantry_vault()



    
