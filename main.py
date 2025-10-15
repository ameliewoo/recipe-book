import os
print("Welcome to the Recipe Book")

userOpeningMenuChoice = input("Are you:" \
"Searching for a recipe? - enter 1" \
"Creating a new recipe? - enter 2 " \
)
match userOpeningMenuChoice:
    case 1:
        Search()
    case 2:
        Create()
    case _:
        print("Invalid input")
        #create loop!

def createRecipeBook():
    #get size of the recipe-book-collection folder 
    count = 0
    folderpath = '/workspaces/recipe-book/recipe-book-collection'
    for file in os.listdir(folderpath):
        if os.file.isfile(os.file.join(folderpath, file)):
            count += 1
    recipeBook = {}
    for file in range(0, count):
        recipeBook[file] = 



def Search():
    print("===================================")
    userMenuChoice = int(input("Search options:" \
    "Search by Title - enter 1" \
    "Search by Ingredients - enter 2" \
    "Search by Serving Size - enter 3" \
    "Search by Meal - enter 4" \
    "Search by dietary tags - enter 5" \
    "Random recipe! - enter 0" \
    "Create a new recipe - enter " \
    "YOUR CHOICE - "))

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
            randomrecipe()

def Create():
    print("================================")

def searchbyTitle():


def searchbyIngredients():

def searchByServings():

def searchByMeal():

def searchByDiet():
    
def randomrecipe():

