import pickle
import re

if __name__ == '__main__':
    """
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

        m = re.search("([0-9._]*?)}", str(ingredient))
        if m:
            scores.append(m.group(1))

    for i in range(len(ings)):
        scoreDict[ings[i]] = scores[i]

    print(scoreList)
    print(scoreDict)

    print(len(scoreList), len(ings), len(scores))

    pickle.dump(scoreDict, open("ingredientScoreList.p", "wb"))
    """
    #ingScoreList = pickle.load(open("ingredientScoreList.p", "rb"))
    #print(ingScoreList)
