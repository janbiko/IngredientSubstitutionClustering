import mysql.connector as mysql
import numpy as np


# Place student names and ID numbers here:
# Jannik Bikowski, 1768542
# Till Emme, 1750770
# Franz Scheuer, 1694029

"""
Problem 1
    Using the classes provided below, augment the recipeInitilization function 
    so that when I create a recipeCase object, I define the respective 
    (and correct) value of each recipe's fsa score, rating, and number 
    of bookmarks.
    
    Check that your code provides the correct output.
"""


class Recipe:

    def __init__(self, initial_recipe):
        con = mysql.connect(user='allrecipes',
                            password='pressackgasse',
                            host='132.199.138.79',
                            database='allrecipes')
        cur = con.cursor()
        recipestring = '%' + initial_recipe + '%'
        cur.execute("""SELECT i.*, pi.name_after_processing
                       FROM ingredients i LEFT JOIN parsed_ingredients pi
                       ON pi.id = i.id
                       WHERE i.recipe_id LIKE '%s'""" % recipestring)
        self.recData = np.array(cur.fetchall(), dtype=object)
        cur.execute("""SELECT ft.recipe_id, ft.avg_rating, ft.bookmarks, ft.fsa_score
                       FROM feature_table ft
                       WHERE ft.recipe_id LIKE '%s'""" % recipestring)
        self.recScores = np.array(cur.fetchall(), dtype=object)
        self.singleRecipes = self.recipeInitialization(self.recData, self.recScores)


    def recipeInitialization(self, data, scores):
        # get columns and rows from input arrays
        rows, columns = np.shape(data)
        rowsScores, columnsScores = np.shape(scores)
        singleRecipes = []

        # Initialization
        tempNames = np.array([], dtype=str)
        tempMass = np.array([], dtype=float)
        tempIndex = np.array([], dtype=float)

        i = 0
        c = 0

        # Define the value of the first instance to iterate from 2 and check indecies of i and i-1
        tempNames = np.hstack([tempNames, data[i, 9]])
        if data[i, 3] == '':
            data[i, 3] = '0'
        tempMass = np.hstack([tempMass, float(data[i, 3])])
        tempIndex = np.hstack([tempIndex, i])
        i = 1

        # Check if the next recipe is in the same, if yes then concatenate the current info
        while i < rows:  # Looping through all ingredient instances
            if data[i, 0] == data[i-1, 0]:
                # storing the ingredient data
                tempNames = np.hstack([tempNames, data[i, 5]])
                if data[i, 3] == '':
                    data[i, 3] = '0'
                tempMass = np.hstack([tempMass, float(data[i, 3])])
                tempIndex = np.hstack([tempIndex, i])
            else:
                # defining single recipe

                tempScoresIndex = np.where(scores == data[i-1, 0])[0]
                tempRating, tempBookmarks, tempFSA = self.__getScoresValues(tempScoresIndex, scores)

                singleRecipes.append(RecipeCase(data[i-1, 0], tempNames, tempMass, tempIndex, data[i-1, 0], tempRating,
                                                tempBookmarks, tempFSA))

                # clearing previous data
                tempNames = np.array([], dtype=str)
                tempMass = np.array([], dtype=float)
                tempIndex = np.array([], dtype=float)
                if data[i, 3] == '':
                    data[i, 3] = '0'

                # begin storing the next recipe
                tempNames = np.hstack([tempNames, data[i, 5]])
                tempMass = np.hstack([tempMass, float(data[i, 3])])
                tempIndex = np.hstack([tempIndex, i])
            i += 1

        # defining the last recipe
        tempScoresIndex = np.where(scores == data[i - 1, 0])[0]
        tempRating, tempBookmarks, tempFSA = self.__getScoresValues(tempScoresIndex, scores)
        singleRecipes.append(RecipeCase(data[i-1, 0], tempNames, tempMass, tempIndex, data[i-1, 0], tempRating,
                                        tempBookmarks, tempFSA))

        return singleRecipes

    def __getScoresValues(self, index, scores):
        try:
            index = int(index)
        except TypeError:
            index = -1

        if index == -1:
            return 'None', 0, 0
        else:
            return scores[index][1], scores[index][2], scores[index][3]


class RecipeCase(Recipe):
        
    def __init__(self, recName, ingNames, ingMass, ingIndex, recID, avgRating=0, bookmarks=0, fsa=0):
        self.recMass = sum(ingMass)
        self.ings = ingNames
        self.ingIndex = ingIndex
        self.rating = avgRating
        self.bookmarks = bookmarks
        self.hscore = fsa
        self.recID = recID
        self.recName = recName
        self.ingMass = ingMass


g = Recipe('tacos')
gall = g.singleRecipes

rtgs = np.array([])
bkms = np.array([])
fsa = np.array([])
for i in range(len(gall)):
    rtgs = np.append(rtgs, gall[i].rating)
    bkms = np.append(bkms, gall[i].bookmarks)
    fsa = np.append(fsa, gall[i].hscore)

print(rtgs)
print(bkms)
print(fsa)
