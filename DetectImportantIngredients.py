import mysql.connector as mysql
import numpy as np
import re


class RecipeIngredients:

    stopwords = ["grilled", "canned", "crumb", "sliced", "chopped", "diced", "oz", "1", "2", "3", "4", "5", "6", "7",
                 "8", "9", "0"]
    amountRecipesTreshold = 0.05

    def __init__(self, dish):
        con = mysql.connect(user='allrecipes',
                            password='pressackgasse',
                            host='132.199.138.79',
                            database='allrecipes')
        cur = con.cursor()
        dishString = '%' + dish + '%'
        print("Acquiring data from database...")
        cur.execute("""SELECT i.recipe_id, pi.name_after_processing
                       FROM ingredients i
                       LEFT JOIN parsed_ingredients pi ON pi.id = i.id
                       WHERE pi.name_after_processing IS NOT NULL
                       AND i.recipe_id LIKE '%s'""" % dishString)

        self.recipeData = np.array(cur.fetchall(), dtype=object)
        print("Data acquired. \nProcessing data.")
        self.corpus = self.createCorpus()
        self.importantIngredients = self.detectImportantIngredients()

    def createCorpus(self):
        recipeDict = {}

        for ingredient in self.recipeData:
            if ingredient[0] not in recipeDict:
                recipeDict[ingredient[0]] = []

            # remove stopwords from ingredients
            ingAsList = str(ingredient[1]).split(' ')
            ingAsList = [word for word in ingAsList if word not in self.stopwords]
            parsedIngredient = ' '.join(ingAsList)
            parsedIngredient = re.sub('[0-9]*%', 'g', parsedIngredient)

            recipeDict[ingredient[0]].append(parsedIngredient)

        ingredientsList = list(recipeDict.values())

        return ingredientsList

    def detectImportantIngredients(self):
        ingsDict = {}
        recipeCount = len(self.corpus)
        importantIngs = []

        for recipe in self.corpus:
            for ingredient in recipe:
                if ingredient not in ingsDict:
                    ingsDict[ingredient] = 1 / recipeCount
                else:
                    ingsDict[ingredient] += 1 / recipeCount

        for ingredient in ingsDict:
            if ingsDict[ingredient] > self.amountRecipesTreshold:
                importantIngs.append(ingredient)

        print(importantIngs)

        return 0

a = RecipeIngredients("taco")
