"""Recipe_Handler.py: Retrieves Recipes."""

__author__      = "Nicholas Leontiev"

import requests
import json
import os
class Recipe_Handler():
    # Variables
    
    # Constructor
    def __init__(self):
        self.HEADERS = {
            "X-RapidAPI-Host": "",
            "X-RapidAPI-Key": ""
        }

    def requests_left(self):
        response = requests.get("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/convert?sourceUnit=cups&sourceAmount=2.5&ingredientName=flour&targetUnit=grams", headers =self.HEADERS)
        numleft = response.headers['x-ratelimit-requests-remaining']
        
        return numleft
    # Searches for 20 random recipes from the Spoonacular API that will be considered for posting and returns one formatted string
    def search_recipe(self,keyword=None):
        recipe =""
        if(int(self.requests_left()) > 0):
            if(keyword ==None):
            
                response = requests.get("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/random?number=10", headers =self.HEADERS)
            
                data = json.loads(response.text)
            
                # Returns the first recipe out of 20 that hasn't been posted before and has good ratings
                recipe = self.check_recipes(data['recipes'])
            
            else:
                keyword = keyword.strip()
                keywords1 = keyword.split(",")
                keyword1 = "" + '%2C'.join(keywords1)

                keywords = keyword1.split(" ")   
                response = requests.get("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/random?number=1&tags=" + '+'.join(keywords), headers =self.HEADERS)
                data = json.loads(response.text)
                recipe = self.summarize(data['recipes'][0])    
        else:    
            recipe = "Out of recipe requests, please try again tomorrow. Sorry for the inconvenience."
              

        return recipe

    # Stores a recipe that has been selected and adds it to the previously posted filexs
    def store_recipes(self,recipe_title):
        f = open("posted_recipes.txt","a+")
        f.write("recipe " + recipe_title + "\n")
        f.close()
        return
        
        
    # Checks the recipes recieved from the api and returns the string of a recipe that meets specifications 
    def check_recipes(self, recipes):
        
        #loops through each recipe
        recipe = ""
        i = 0
        while (i < 10):
            if not self.recipe_exists(recipes[i]['title']):
                if ('spoonacularScore' in recipes[i] and recipes[i]['spoonacularScore'] >= 75) or ('aggregateLikes' in recipes[i] and recipes[i]['aggregateLikes'] >= 200):   
                    if(len(self.summarize(recipes[i])) < 280 ):
                        recipe = recipes[i]
                        break
            i += 1
        
        if(recipe == ""):
            return "Recipe not found. Please try again"
        else:
            # stores the id of the selected recipe
            self.store_recipes(recipe['title'])
            # returns a formatted string of the recipe
            return self.summarize(recipe)
                  
    # Produces a brief description of the recipe based on its tags
    def summarize(self, recipe):
        formattedRecipe = recipe['title'] + "\nCook Time: " + str(recipe['readyInMinutes'])+ " minutes\n"  + recipe["sourceUrl"]
        
        return formattedRecipe    
    

    # checks to see if article was posted before 
    def recipe_exists(self,rec_recipe):
        if not os.path.isfile("posted_recipes.txt"):
            open("posted_recipes.txt", "w+").close()
        test = "recipe " + rec_recipe
        
        found = False
        f = open("posted_recipes.txt", "r")
        for line in f:
            line = line.strip()
            if(line == test):
               found = True

                
        f.close()
        return found
        


            
