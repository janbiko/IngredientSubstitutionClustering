import numpy as np
import mysql.connector as mysql
import re
import csv


class UniqueIngredients:

    stopwords = ["grilled", "canned", "crumb", "sliced", "chopped", "diced", "oz", "1", "2", "3", "4", "5", "6", "7",
                 "8", "9", "0"]

    def __init__(self):
        self.con = mysql.connect(user='allrecipes',
                            password='pressackgasse',
                            host='132.199.138.79',
                            database='allrecipes')
        self.cur = self.con.cursor()
        self.parsedUniqueIngredients = list()

    def getUniqueIngredients(self, saveData=False):
        print("Acquiring data from database...")
        self.parsedUniqueIngredients = list()

        self.cur.execute("""SELECT DISTINCT(name_after_processing), frequency
                                      FROM parsed_ingredients
                                      WHERE name_after_processing != 'NULL'
                                      ORDER BY frequency DESC LIMIT {}""".format(10000))
        uniqueIngs = np.array(self.cur.fetchall(), dtype=object)
        uniqueIngs = [ings[0] for ings in uniqueIngs]

        for ingredient in uniqueIngs:
            # remove stopwords from ingredients
            ingAsList = str(ingredient).split(' ')
            ingAsList = [word for word in ingAsList if word not in self.stopwords]
            parsedIngredient = ' '.join(ingAsList)
            parsedIngredient = re.sub('[0-9]*%', 'g', parsedIngredient)
            self.parsedUniqueIngredients.append(parsedIngredient)
        self.parsedUniqueIngredients = sorted(list(set(self.parsedUniqueIngredients)))
        self.parsedUniqueIngredients.pop(0)

        if saveData:
            out = csv.writer(open('uniqueIngredients.csv', 'w'), delimiter=',', quoting=csv.QUOTE_ALL)
            out.writerow(self.parsedUniqueIngredients)


if __name__ == '__main__':
    #a = UniqueIngredients()
    #a.getUniqueIngredients(saveData=True)

    recCorpus = []
    with open('recipeCorpus.csv') as f:
        reader = csv.reader(f)
        recCorpus = list(reader)[::2]

    uniqueIngredients = []
    for recipe in recCorpus:
        for ingredient in recipe:
            if ingredient not in uniqueIngredients:
                uniqueIngredients.append(ingredient)

    out = csv.writer(open('uniqueIngredients.csv', 'w'), delimiter=',', quoting=csv.QUOTE_ALL)
    out.writerow(uniqueIngredients)
