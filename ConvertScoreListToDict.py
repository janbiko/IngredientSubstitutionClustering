import pickle
import re

if __name__ == '__main__':

    scoreList = pickle.load(open("ingredientScoreList.p", "rb"))
    scoreDict = {}

    ings = []
    scores = []
    for ingredient in scoreList:
        #m = re.search("'((.|\n)*?)'", str(ingredient))
        m = re.search("'([a-zA-Z0-9'&-_ \t\n\r\f\v]*?)'", str(ingredient))
        #m = re.search("'(a-zA-Z)*?'", str(ingredient))
        #print(ingredient)
        #print(m)
        if m:
            ings.append(m.group(1))
        elif "baker's white chocolate" in str(ingredient):
            ings.append("baker's white chocolate")
        elif "devil's food cake mix" in str(ingredient):
            ings.append("devil's food cake mix")
        elif "hershey's cocoa" in str(ingredient):
            ings.append("hershey's cocoa")
        elif "reese's piece" in str(ingredient):
            ings.append("reese's piece")
        elif "confectioners' sugar" in str(ingredient):
            ings.append("confectioners' sugar")

        m = re.search("([0-9._]*?)}", str(ingredient))
        if m:
            scores.append(m.group(1))

    for i in range(len(ings)):
        scoreDict[ings[i]] = scores[i]

    #print(scoreList)
    #print(scoreDict)

    #print(len(scoreList), len(ings), len(scores))

    badIngs = []
    for ing in scoreDict.keys():
        if scoreDict[ing] == "100":
            badIngs.append(ing)
    print(badIngs)

    scoreDict["pepper flake"] = "1.0"
    scoreDict["lemon zest"] = "0.0"
    scoreDict["bbq seasoning"] = "1.25"
    scoreDict["artichoke heart"] = "0.25"
    scoreDict["italian seasoning"] = "1.25"
    scoreDict["liquid smoke"] = "3.25"
    scoreDict["broccoli floret"] = "0.0"
    scoreDict["orange zest"] = "0.0"
    scoreDict["salmon fillet"] = "2.25"
    scoreDict["pie dough"] = "3.0"
    scoreDict["lime zest"] = "0.0"
    scoreDict["cajun seasoning"] = "1.25"
    scoreDict["ice cube"] = "0.0"
    scoreDict["breadcrumb"] = "2.5"
    scoreDict["mixed veggy"] = "0.0"
    scoreDict["prosciutto"] = "2.5"
    scoreDict["thick-cut bacon"] = "5.0"
    scoreDict["sherry"] = "0.0"
    scoreDict["brandy"] = "1.25"
    scoreDict["pancetta"] = "5.0"
    scoreDict["bourbon"] = "1.25"
    scoreDict["food coloring"] = "0.0"
    scoreDict["baguette"] = "2.5"
    scoreDict["marinated artichoke heart"] = "0.5"
    scoreDict["jalepeno"] = "3.5"
    scoreDict["garam masala"] = "1.25"
    scoreDict["parsley flake"] = "2.5"
    scoreDict["evoo"] = "4.25"
    scoreDict["creole seasoning"] = "1.5"
    scoreDict["pizza dough"] = "2.25"
    scoreDict["crisco"] = "3.75"
    scoreDict["margarine"] = "3.75"
    scoreDict["mayonaise"] = "3.5"
    scoreDict["old bay seasoning"] = "1.5"
    scoreDict["chilly"] = "3.5"
    scoreDict["pb cup"] = "4.5"
    scoreDict["chicken base"] = "4.75"
    scoreDict["chipotle peppers in adobo"] = "1.5"
    scoreDict["bread cube"] = "2.5"
    scoreDict["real bacon recipe piece"] = "5.0"
    scoreDict["linguine"] = "1.0"
    scoreDict["parmigiano reggiano"] = "6.25"
    scoreDict["agave nectar"] = "3.25"
    scoreDict["lime jello"] = "3.25"
    scoreDict["beef base"] = "1.75"
    scoreDict["tater tot"] = "1.0"
    scoreDict["dry sherry"] = "0.0"
    scoreDict["chipotle"] = "3.5"
    scoreDict["rotel"] = "0.25"
    scoreDict["triple sec"] = "3.0"
    scoreDict["bread dough"] = "2.5"
    scoreDict["crabmeat"] = "1.25"
    scoreDict["sprinkle"] = "3.5"
    scoreDict["cod fillet"] = "2.25"
    scoreDict["chili flake"] = "3.5"
    scoreDict["fettuccine"] = "1.0"
    scoreDict["ready-to-serve asian fried rice"] = "1.5"
    scoreDict["strawberry jello"] = "3.25"
    scoreDict["food dye"] = "0.0"
    scoreDict["semi-sweet chocolate"] = "5.0"
    scoreDict["bisquick"] = "5.75"
    scoreDict["cauliflower floret"] = "0.0"
    scoreDict["hashbrown"] = "1.25"
    
    pickle.dump(scoreDict, open("ingredientScoreList.p", "wb"))

    #ingScoreList = pickle.load(open("ingredientScoreList.p", "rb"))
    #print(ingScoreList)
