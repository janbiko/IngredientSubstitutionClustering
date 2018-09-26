import requests
import json
import csv
import pickle
import time


class FoodDatabaseRequests:
    def __init__(self):
        self.api_key = "99Pz4D0mHTP7g4GqR42iGU0di6X9Hq4ii0r3G9qb"
        self.api_key2 = "Ss3J1M1phqRHb9EsOqRaeX9kRLMckI7all1NKb8W"
        self.url = "https://api.nal.usda.gov/ndb"
        self.search_url = "/search/?format=json&ds=Standard%20Reference&sort=r&max=1&offset=0" \
                          "&api_key=" + self.api_key
        self.nutrition_url = "/V2/reports?type=b&format=json&api_key=" + self.api_key
        self.energyLevels = []
        self.fatLevels = []
        self.sugarLevels = []
        self.sodiumLevels = []
        self.initNutritionLevelArrays()
        self.topKIngredients = self.importTopKIngredients()

    def importTopKIngredients(self):
        with open("topKIngredients.csv") as f:
            reader = csv.reader(f)
            return list(reader)[0]

    def initNutritionLevelArrays(self):
        for i in range(10):
            self.energyLevels.append(335 * (i + 1))
            self.fatLevels.append(i + 1)
            self.sugarLevels.append(4.5 * (i + 1))
            self.sodiumLevels.append(90 * (i + 1))

    def getIngredientDbNumber(self, ingredient, new_ing):
        request_url = self.url + self.search_url + "&q=" + new_ing
        response = requests.post(request_url)
        parsed_response = json.loads(response.text)
        # print(parsed_response)
        if "errors" in parsed_response and ingredient == new_ing:
            return self.getIngredientDbNumber(ingredient, self.getTopKAlternative(ingredient))
        else:
            if new_ing == "":
                return {ingredient: 100}
        ndbno = parsed_response["list"]["item"][0]["ndbno"]
        return self.getNutritionValues(ndbno, ingredient)

    def getTopKAlternative(self, ingredient):
        ingAsList = []
        if "-" in ingredient:
            ingAsList = str(ingredient).split('-')
        elif " " in ingredient:
            ingAsList = str(ingredient).split(' ')
        else:
            return ""
        newIngredient = ""
        for word in list(reversed(ingAsList)):
            if word in self.topKIngredients:
                newIngredient = word
                break
        return newIngredient

    def getNutritionValues(self, db_number, ingredient):
        request_url = self.url + self.nutrition_url + "&ndbno=" + db_number
        response = requests.post(request_url)
        parsed_response = json.loads(response.text)
        nutrients = parsed_response["foods"][0]["food"]["nutrients"]
        saturated_fat, sodium, energy, sugar = 0.0, 0.0, 0.0, 0.0
        for nutrient in nutrients:
            name = nutrient["name"]
            value = float(nutrient["value"])
            if name == "Energy":
                energy = value * 4.1868
            elif name == "Sugars, total":
                sugar = value
            elif name == "Sodium, Na":
                sodium = value
            elif name == "Fatty acids, total saturated":
                saturated_fat = value

        score = 0
        for i in range(len(self.fatLevels)):
            if saturated_fat > self.fatLevels[i]:
                score += 1
            if energy > self.energyLevels[i]:
                score += 1
            if sugar > self.sugarLevels[i]:
                score += 1
            if sodium > self.sodiumLevels[i]:
                score += 1

        score /= 4
        return {ingredient: score}

    def parseCsvFile(self, filename):
        with open(filename) as f:
            reader = csv.reader(f)
            return list(reader)[0]


ingScoreList = []


def doRequests(index):
    global ingScoreList
    for i in range(index, index + 1000):
        try:
            ingredient = foodRequest.getIngredientDbNumber(ingList[i], ingList[i])
            if ingredient == 0: continue
            ingScoreList.append(ingredient)
            print(i)
        except IndexError:
            break

    pickle.dump(ingScoreList, open("ingredientScoreList.p", "wb"))
    ingScoreList = pickle.load(open("ingredientScoreList.p", "rb"))
    print(ingScoreList)


if __name__ == "__main__":
    foodRequest = FoodDatabaseRequests()
    print(foodRequest.getIngredientDbNumber("spice rub", "spice rub"))
    #ingList = foodRequest.parseCsvFile("topKIngredients.csv")
    #index = 0
    #while index < 4000:
    #    doRequests(index)
    #    time.sleep(3600)
    #    index += 1000
