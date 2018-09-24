import mysql.connector as mysql
import numpy as np
import re
import pickle
import csv
from gensim.models import FastText


class IngredientSubstitution:

    USERNAME = 'allrecipes'
    PASSWORD = 'pressackgasse'
    HOST = '132.199.138.79'
    DATABASE = 'allrecipes'

    stopwords = ["grilled", "canned", "crumb", "sliced", "chopped", "diced", "oz", "1", "2", "3", "4", "5", "6", "7",
                 "8", "9", "0", "red", "green", "yellow", "fresh", "whole", "dried"]

    def __init__(self, recipe):
        con = mysql.connect(user=self.USERNAME,
                            password=self.PASSWORD,
                            host=self.HOST,
                            database=self.DATABASE)
        cur = con.cursor()
        recipeString = "'%/" + recipe + "/%'"
        cur.execute("""SELECT DISTINCT(pri.recipe_id), pi.name_after_processing FROM parsed_recipe_ingredients pri
                       JOIN parsed_ingredients pi ON pi.new_ingredient_id = pri.parsed_ingredient_id
                       WHERE pri.recipe_id LIKE {}""".format(recipeString))

        recipeData = np.array(cur.fetchall(), dtype=object)
        self.originalRecipe = [ings[1] for ings in recipeData]
        print("Original recipe:\n", self.originalRecipe, "\n")
        self.parsedRecipe = self.removeStopwords()

        self.healthScoreDict = pickle.load(open("ingredientScoreList.p", "rb"))
        self.recipeHealthDict = self.mapHealthScores()

        self.fastTextModel = pickle.load(open("fastTextModel.p", "rb"))

    def removeStopwords(self):
        parsedRecipe = []

        for ingredient in self.originalRecipe:
            ingAsList = str(ingredient).split(' ')
            ingAsList = [word for word in ingAsList if word not in self.stopwords]
            parsedIngredient = ' '.join(ingAsList)
            parsedIngredient = re.sub('[0-9]*%', 'g', parsedIngredient)
            parsedRecipe.append(parsedIngredient)

        print("Recipe after stopword removal:\n", parsedRecipe, "\n")
        return parsedRecipe

    def mapHealthScores(self):
        recDict = {}
        for ingredient in self.parsedRecipe:
            if ingredient not in recDict:
                recDict[ingredient] = self.healthScoreDict.get(ingredient)

        print("Ingredient health scores:\n", recDict, "\n")
        return recDict

    def findSubstitutions(self):
        for ingredient in self.parsedRecipe:
            print(ingredient, "substitutions: \n", self.fastTextModel.wv.most_similar(ingredient), "\n\n")

if __name__ == '__main__':
    a = IngredientSubstitution("chicken-and-pumpkin-goulash")
    a.findSubstitutions()
