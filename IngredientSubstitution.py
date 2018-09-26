import mysql.connector as mysql
import numpy as np
import re
import pickle
import time
import csv
from gensim.models import FastText


class IngredientSubstitution:

    USERNAME = 'allrecipes'
    PASSWORD = 'pressackgasse'
    HOST = '132.199.138.79'
    DATABASE = 'allrecipes'

    stopwords = ["grilled", "canned", "ground", "crumb", "sliced", "chopped", "diced", "oz", "1", "2", "3", "4", "5", "6", "7",
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
        sim_ing_scores = {}
        for ingredient in self.parsedRecipe:
            print(ingredient, "substitutions: \n", self.fastTextModel.wv.most_similar(ingredient), "\n\n")
            most_similar = self.fastTextModel.wv.most_similar(ingredient)
            sim_ing_scores[ingredient] = []
            for sim_ing in most_similar[:5]:
                health_score = self.healthScoreDict.get(sim_ing[0])
                if (not health_score is None) and (health_score != '0.0'):
                    sim_ing_scores[ingredient].append((sim_ing[0],health_score))
        for ing in sim_ing_scores:
            sim_ing_list = sim_ing_scores[ing]
            if len(sim_ing_list) == 0: continue
            print(ing," (", self.healthScoreDict.get(ing),")", ": ", min(sim_ing_list, key= lambda t:t[1]))

if __name__ == '__main__':
    starttime = time.time()
    a = IngredientSubstitution("almond-butter")
    a = IngredientSubstitution("chicken-and-pumpkin-goulash")
    a = IngredientSubstitution("easy-beef-goulash")
    a = IngredientSubstitution("mommas-pasta-and-shrimp-salad")
    a.findSubstitutions()
    print(time.time()-starttime)
