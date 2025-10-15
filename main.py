import os
def main():
    print("Welcome to the Recipe Book")
    userOpeningMenuChoice = input("Are you:" \
    "Searching for a recipe? - enter 1" \
    "Creating a new recipe? - enter 2 " \
    )
    try:
        userOpeningMenuChoice = int(userOpeningMenuChoice)
    except ValueError:
        print("Invalid input, please enter a number")
        exit()
    match userOpeningMenuChoice:
        case 1:
            Search()
        case 2:
            Create()
        case _:
            print("Invalid option, please enter 1 or 2")

def createRecipeBook():
    #get size of the recipe-book-collection folder 
    count = 0
    folderPath = os.path.dirname(__file__) + '/recipe-book-collection'
    for file in os.listdir(folderPath):
        if os.path.isfile(os.path.join(folderPath, file)):
            count += 1
    
    recipeBook = {}
    for file in range(0, count):
        recipeBook[file] = {}
    #search for the ingredients etc in each file and add to the dictionary
    for file in os.listdir(folderPath):
        with open(os.path.join(folderPath, file), 'r') as f:
            lines = f.readlines()
            title = lines[0].strip()
            ingredients = []
            servings = ""
            meal = ""
            diet = []
            instructions = []
            for line in lines[1:]:
                if line.startswith("Ingredients:"):
                    ingredients = line[len("Ingredients:"):].strip().split(",")
                elif line.startswith("Servings:"):
                    servings = line[len("Servings:"):].strip()
                elif line.startswith("Meal:"):
                    meal = line[len("Meal:"):].strip()
                elif line.startswith("Dietary Tags:"):
                    diet = line[len("Dietary Tags:"):].strip().split(", ")
                elif line.startswith("Instructions:"):
                    instructions = line[len("Instructions:"):].strip().split(".")
            recipeBook[file] = {
                "Title": title,
                "Ingredients": ingredients,
                "Servings": servings,
                "Meal": meal,
                "Dietary Tags": diet,
                "Instructions": instructions
            }
            
    print(folderPath)
    print(recipeBook)
    return recipeBook

def Search():
    print("===================================")
    userMenuChoice = int(input("Search options:" \
    "Search by Title - enter 1" \
    "Search by Ingredients - enter 2" \
    "Search by Serving Size - enter 3" \
    "Search by Meal - enter 4" \
    "Search by dietary tags - enter 5" \
    "Random recipe! - enter 0" \
    "==================================="))
    
    try :
        match userMenuChoice:
            case 1:
                searchbyTitle()
            case 2:
                searchbyIngredients()
            case 3:
                searchByServings()
            case 4:
                searchByMeal()
            case 5:
                searchByDiet()
            case 0:
                randomRecipe()
            case _:
                print("Invalid option, please enter a number between 0 and 5")
    except ValueError:
        print("Invalid input, please enter a number")

def Create():
    print("================================")
    

def searchbyTitle():
    #takes input from user and searches the recipe book for the title
    recipeBook = createRecipeBook()
    title = input("Enter the title of the recipe: ")
    for recipe in recipeBook.values():
        if recipe["Title"].lower() == title.lower():
            print(f"Recipe found: {recipe['Title']}")
            print(f"Ingredients: {', '.join(recipe['Ingredients'])}")
            print(f"Servings: {recipe['Servings']}")
            print(f"Meal: {recipe['Meal']}")
            print(f"Dietary Tags: {', '.join(recipe['Dietary Tags'])}")
            print(f"Instructions: {' '.join(recipe['Instructions'])}")
            return  


def searchbyIngredients():
    #takes input from user and searches the recipe book for the ingredients
    #! alow 
    recipeBook = createRecipeBook()
    ingredients = input("Enter the ingredients (comma-separated): ").strip().split(", ")
    for recipe in recipeBook.values():
        if set(ingredients).issubset(set(recipe["Ingredients"])):
            print(f"Recipe found: {recipe['Title']}")
            print(f"Ingredients: {', '.join(recipe['Ingredients'])}")
            print(f"Servings: {recipe['Servings']}")
            print(f"Meal: {recipe['Meal']}")
            print(f"Dietary Tags: {', '.join(recipe['Dietary Tags'])}")
            print(f"Instructions: {' '.join(recipe['Instructions'])}")
            return
def searchByServings():
    pass

def searchByMeal():
    pass

def searchByDiet():
    pass

def randomRecipe():
    import random
    P = '/workspaces/recipe-book/recipe-book-collection'
    files = os.listdir(P)
    random_file = random.choice(files)
    print(f"Random Recipe: {random_file}")
    with open(os.path.join(P, random_file), 'r') as file:
        print(file.read())

#! main running code here
createRecipeBook() 