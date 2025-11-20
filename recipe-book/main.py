import os
import random
import pickle

class Recipe:
    def __init__(self, title, ingredients, cooking_time, method, servings, meal, dietary_tags, filename=None):
        self.title = title.strip()
        self.ingredients = [i.strip() for i in ingredients if i and i.strip()]
        self.cooking_time = cooking_time.strip()
        self.method = [s.strip() for s in method if s and s.strip()]
        self.servings = servings.strip()
        self.meal = meal.strip()
        self.dietary_tags = [t.strip() for t in dietary_tags if t and t.strip()]
        self.filename = filename

    @classmethod
    def from_file(cls, path):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        title = lines[0].strip() if lines else ""
        ingredients, cooking_time, method, servings, meal, dietary_tags = [], "", [], "", "", []

        for line in lines[1:]: #cleans up and makes user-friendly
            line = line.strip()
            lower_line = line.lower()
            if lower_line.startswith("ingredients:"):
                raw = line[len("Ingredients:"):].strip()
                ingredients = [i.strip() for i in raw.split(",") if i.strip()]
            elif lower_line.startswith("cooking time:"):
                cooking_time = line[len("Cooking time:"):].strip()
            elif lower_line.startswith("method:"):
                raw = line[len("Method:"):].strip()
                method = [s.strip() for s in raw.split(".") if s.strip()]
            elif lower_line.startswith("serving size:"):
                servings = line[len("Serving size:"):].strip()
            elif lower_line.startswith("meal:"):
                meal = line[len("Meal:"):].strip()
            elif lower_line.startswith("dietary tags:"):
                dietary_tags = [t.strip() for t in line[len("Dietary tags:"):].split(",") if t.strip()]

        return cls(title, ingredients, cooking_time, method, servings, meal, dietary_tags, filename=os.path.basename(path))

    def matches(self, criteria, query):
        if isinstance(query, str):
            query = query.strip().lower()

        recipe_fields = {
            'title': lambda: self.title.lower() == query,
            'ingredients': lambda: isinstance(query, list) and set(i.lower() for i in query).issubset(set(i.lower() for i in self.ingredients)),
            'servings': lambda: self.servings.lower() == query,
            'meal': lambda: self.meal.lower() == query,
            'diet': lambda: query in (t.lower() for t in self.dietary_tags)
        }
        return recipe_fields.get(criteria, lambda: query in self.title.lower())()

    def __str__(self):
        return (
            f"{self.title}\n"
            f"Ingredients: {', '.join(self.ingredients)}\n"
            f"Cooking time: {self.cooking_time}\n"
            f"Method: {'. '.join(self.method)}\n"
            f"Serving size: {self.servings}\n"
            f"Meal: {self.meal}\n"
            f"Dietary tags: {', '.join(self.dietary_tags)}\n"
        )


class RecipeBook:
    def __init__(self, folder='recipe-book-collection', pickle_file='recipes.pkl'):
        self.folder = os.path.join(os.path.dirname(__file__), folder)
        self.pickle_path = os.path.join(self.folder, pickle_file)
        os.makedirs(self.folder, exist_ok=True)
        self.recipes = self._load_recipes()

    def _load_recipes(self):
        # pickle! 
        if os.path.exists(self.pickle_path):
            try:
                with open(self.pickle_path, 'rb') as f:
                    print("Loading recipes from pickle file...")
                    return pickle.load(f)
            except Exception as e:
                print("Failed to load pickle file, loading from .txt instead:", e)

        # if pickle doesn't work - use the .txt files i already have
        recipes = []
        for fname in os.listdir(self.folder):
            path = os.path.join(self.folder, fname)
            if os.path.isfile(path) and fname.endswith(".txt"):
                try:
                    recipes.append(Recipe.from_file(path))
                except Exception as e:
                    print(f"Error loading {fname}: {e}")
        return recipes

    def _save_to_pickle(self):
        with open(self.pickle_path, 'wb') as f:
            pickle.dump(self.recipes, f)
        print("Recipes saved to pickle file.")

    def add_recipe(self, recipe):
        file_path = os.path.join(self.folder, f"{recipe.title}.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(recipe))

        # update pickle
        self.recipes.append(recipe)
        self._save_to_pickle()

    def search(self, criteria, query, return_first=False):
        if criteria == 'ingredients' and isinstance(query, str):
            query = [i.strip() for i in query.split(',') if i.strip()]
        elif isinstance(query, str):
            query = query.strip()

        matches = [r for r in self.recipes if r.matches(criteria, query)]
        return matches[0] if return_first and matches else matches

    def get_random_recipe(self):
        return random.choice(self.recipes) if self.recipes else None

class RecipeApp:
    def __init__(self):
        self.book = RecipeBook()

    def run(self): #3/11 - implemented a loop so it runs util the user wants to exit 
        keep_running = True
        while keep_running:
            print('*' * 30)
            print("Welcome to the Recipe Book")
            print('*' * 30)

            choice = input("Are you:\n\tSearching for a recipe? - enter 1\n\tCreating a new recipe? - enter 2\n")
            try:
                choice = int(choice)
            except ValueError:
                print("Invalid input, please try again")
                continue

            if choice == 1:
                self.search_menu()
            elif choice == 2:
                self.create_recipe()
            else:
                print("Invalid option, please try again")

            again = input("Would you like to do something else? (Y/N): ").strip().upper()
            while again not in ("Y", "N"):
                again = input("Invalid input. Please enter Y or N: ").strip().upper()
            keep_running = again == "Y"

        print("Goodbye!")

    def create_recipe(self):
        print("================================")
        title = input("Enter the title of the recipe: ").strip()
        ingredients = input("Enter the ingredients (comma-separated): ").strip().split(",")
        cooking_time = input("Enter the cooking time (e.g., '10 minutes'): ").strip()
        method = input("Enter the method (steps separated by full stops): ").strip().split(".")
        servings = input("Enter the serving size: ").strip()
        meal = input("Enter the meal type: ").strip()
        dietary_tags = input("Enter the dietary tags (comma-separated): ").strip().split(",")

        recipe = Recipe(title, ingredients, cooking_time, method, servings, meal, dietary_tags)
        self.book.add_recipe(recipe)
        print(f"Recipe for '{title}' saved!")

    def search_menu(self):
        print("=========================================")
        try:
            choice = int(input("Search options:\n"
                "\tSearch by Title - enter 1\n"
                "\tSearch by Ingredients - enter 2\n"
                "\tSearch by Serving Size - enter 3\n"
                "\tSearch by Meal - enter 4\n"
                "\tSearch by dietary tags - enter 5\n"
                "\tRandom recipe! - enter 0\n"
                "===========================================\n"
                "Please enter your choice:   "))
        except ValueError:
            print("Invalid input")
            return

        fields = {
            1: 'title',
            2: 'ingredients',
            3: 'servings',
            4: 'meal',
            5: 'diet'
        }

        if choice == 0:
            recipe = self.book.get_random_recipe()
            print("Random Recipe:\n", recipe if recipe else "No recipes available.")
        elif choice in fields:
            query = input(f"Enter your search query for {fields[choice]}: ").strip()
            results = self.book.search(fields[choice], query)
            if results:
                for r in results:
                    print("Recipe found:\n", r)
            else:
                print("No matching recipes found.")
        else:
            print("Invalid option")


if __name__ == "__main__":
    app = RecipeApp()
    app.run()
