import requests
import json

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

    def initNutritionLevelArrays(self):
        for i in range(10):
            self.energyLevels.append(335*(i+1))
            self.fatLevels.append(i+1)
            self.sugarLevels.append(4.5*(i+1))
            self.sodiumLevels.append(90*(i+1))


    def getIngredientDbNumber(self, ingredient):
        request_url = self.url + self.search_url + "&q=" + ingredient
        response = requests.post(request_url)
        parsed_response =json.loads(response.text)
        ndbno = parsed_response["list"]["item"][0]["ndbno"]
        return self.getNutritionValues(ndbno, ingredient)


    def getNutritionValues(self, db_number, ingredient):
        request_url = self.url + self.nutrition_url + "&ndbno=" + db_number
        response = requests.post(request_url)
        parsed_response =json.loads(response.text)
        nutrients = parsed_response["foods"][0]["food"]["nutrients"]
        print(parsed_response)
        saturated_fat, sodium, energy, sugar = 0.0, 0.0, 0.0, 0.0
        for nutrient in nutrients:
            name = nutrient["name"]
            value = float(nutrient["value"])
            if name == "Energy":
                energy = value*4.1868
            elif name == "Sugars, total":
                sugar = value
            elif name == "Sodium, Na":
                sodium = value
            elif name == "Fatty acids, total saturated":
                saturated_fat = value
        print(saturated_fat, sodium, energy, sugar)

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



if __name__=="__main__":
    foodRequest = FoodDatabaseRequests()
    ingScore = foodRequest.getIngredientDbNumber("fat")
    print(ingScore)
