import numpy as np
import mysql.connector as mysql
import csv
import pickle
from nltk.cluster import KMeansClusterer
import nltk
import pprint
from gensim.models import Word2Vec
from gensim.models import FastText
from gensim.corpora import Dictionary
from gensim import models, similarities

from sklearn import cluster
from sklearn import metrics

# Place student names and ID numbers here:
# Jannik Bikowski, 1768542
# Till Emme, 1750770
# Franz Scheuer, 1694029


""" 
Homework 4: This assignment is ment to provide a continued review of (or further
    build skills) in programming and to prepare our data for some future (more 
    complex) processes.
    
    This weeks assignment is more complicated than last weeks, to the extent 
    that I am not providing any code for you to use. It is now your job to 
    either (1) write your own programs fully, or understand what you can take 
    from my prevously provided code, and build off of it. I would recomend that
    you use a class structure similar to the class I constructed in homework 3.
    
    Problem 1.
    Create a function that will create a "corpus" that we can use for text
    processing. The corpus should be made up of ingredient lists of different
    recipes. This can be done in any way that you would like, however, consider
    how you expect to provide the input, for example:
        (A) the input to the function can be similar to the singleRecipes 
            attribute of the recipe class in homework 3, or 
        (B) the input to the function can be a large table generated from an 
            SQL query
        
        It is your job to decide what is the best way to provide input to this
        function.
        
    The output should be structured as follows:
        
    Index 0 of the coprus is equal to the first document in the courpus and
    terms are distinct strings (this should be easier than problem 4). For 
    example:
        corpus[0]
        Out[5]: 
            ['ground beef',
             'sausage',
             'egg',
             'bread crumb',
             'ice',
             'onion',
             'barbecue sauce',
             'ketchup',
             'onion']
                
    When I query an index of a document, I am returned a single term in 
    the document. For example:
        document=corpus[0]
        term=document[0]
        print(term)
        ground beef
        type(term)
        Out[12]: str
        
    Problem 2.
    Perform the same task as problem 1, however, now process each ingredient
    in, or placed in to, the coprpus by removing our class generated list of 
    stopwords (which will be provided after lecture) from all documents and/or 
    terms in the corpus.
    
    Problem 3.
    Perform the same task as problem 2, however, after removing the stop 
    words, process each term such that the original term is replaced with an 
    equivalent ingredient present in the top k  most common ingredients.
     Hints: 1. The following code can be used to convert a column of strings
               from the DB to a list: 
                     temporary=cur.fetchall() #Retrieving a query of strings
                     list=[tempN[0] for tempN in temporary]
            2. I would recommend the following procedure
                (a) Retrieve an ordered list of the top k ingredients from the DB
                    based on the ingredient rank.
                (b) Given an ingredient in a recipe (or term in a document)
                    check if this ingredient can be considered one of the
                    ingredients in the top k ingredient list.
                (c) If yes, replace the ingredient in the recipe (term in the 
                    document) with the name of the equivalent ingredient in
                    in the top k ingredient list
            3. This method is not likely to be "perfect." It is your job to 
               decide how to best replace an ingredeint, you need to make
               your decisions so that the method will perform best. Provide a 
               comment in your function (of aproximarly 2-3 sentences) which
               explains why you performed the task as you have.
               
   Problem 4. 
   Augment the function written in problem 1, however, instead of reporting 
   each document as a list of strings (terms) create each document as a single 
   list, with spaces seperating each term.
   The output should be structured as follows:
       corpus[0]
       Out[15]: 'ground beef sausage egg bread crumb ice onion barbecue sauce 
                 ketchup onion'
       
"""


class IngredientCorpus:

    stopwords = ["crumb", "sliced", "chopped", "diced", "oz", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

    def __init__(self, topK=1000):
        con = mysql.connect(user='allrecipes',
                            password='pressackgasse',
                            host='132.199.138.79',
                            database='allrecipes')
        cur = con.cursor()
        print("Acquiring data from database...")
        '''
        cur.execute("""SELECT i.recipe_id, pi.name_after_processing
                               FROM ingredients i
                               LEFT JOIN parsed_ingredients pi ON pi.id = i.id
                               WHERE pi.name_after_processing IS NOT NULL LIMIT 100""")
        '''
        cur.execute("""SELECT pri.recipe_id, pi.name_after_processing FROM `parsed_recipe_ingredients` pri JOIN
parsed_ingredients pi on pri.parsed_ingredient_id = pi.id
WHERE pi.name_after_processing != ''""")

        self.data = np.array(cur.fetchall(), dtype=object)

        cur.execute("""SELECT DISTINCT(name_after_processing), frequency
                       FROM parsed_ingredients
                       WHERE name_after_processing != 'NULL'
                       ORDER BY frequency DESC LIMIT {}""".format(topK))
        self.topKResults = np.array(cur.fetchall(), dtype=object)
        # only store ingredient names, not frequencies
        self.topKResults = [ings[0] for ings in self.topKResults]

        print("Data acquired. \nProcessing data.")
        self.corpus = self.createCorpus(self.data)

    def createCorpus(self, data, verbose=True):
        dataProcessed = 0
        lenData = len(data)
        recDict = {}

        for ingredient in data:
            if ingredient[0] not in recDict:
                recDict[ingredient[0]] = list()

            # remove stopwords from ingredients
            ingAsList = str(ingredient[1]).split(' ')
            ingAsList = [word for word in ingAsList if word not in self.stopwords]
            parsedIngredient = ' '.join(ingAsList)

            # save ingredient to recipe, if in top k results
            if parsedIngredient in self.topKResults:
                recDict[ingredient[0]].append(parsedIngredient)  # = str(recDict[ingredient[0]]) + parsedIngredient + ' '
            else:
                # look for similar ingredient in top k results
                parsedIngredient = [x for x in ingAsList if x in self.topKResults]
                # skip ingredient, if not found in top k results
                if len(parsedIngredient) == 0:
                    '''
                    We decided to skip unpopular ingredients in order to avoid having too many ingredients in the
                    corpus, which only appear once. If too many ingredients are skipped, you can adjust the top k
                    results.
                    '''
                    continue
                # replace ingredient with similar top k results ingredient
                else:
                    # if ingredient can be split into two ingredients, select the more popular from top k results
                    index = min([self.topKResults.index(x) for x in parsedIngredient])
                    parsedIngredient = self.topKResults[index]
                recDict[ingredient[0]].append(parsedIngredient)  # = str(recDict[ingredient[0]]) + parsedIngredient + ' '

            if verbose:
                dataProcessed += 1
                print("\rProcessed data:", dataProcessed, "/", lenData, end="", flush=True)

        return list(recDict.values())

    def saveCorpus(self):
        out = csv.writer(open('recipeCorpus.csv', 'w'), delimiter=',')
        out.writerows(self.corpus)

    def saveTopKIngredients(self):
        out = csv.writer(open('topKIngredients.csv', 'w'), delimiter=',', quoting=csv.QUOTE_ALL)
        out.writerow(self.topKResults)

if __name__=="__main__":
    #a = IngredientCorpus(topK=10000000)
    #document = a.corpus[0]
    #a.saveCorpus()

    recCorpus = []
    with open("recipeCorpus.csv", mode="r") as f:
        reader = csv.reader(f, )
        recCorpus = list(reader)

    #print(recCorpus)


    #gensimDict = Dictionary(recCorpus)
    #recCorpusBow = [gensimDict.doc2bow(line) for line in recCorpus]
    #pickle.dump(recCorpusBow, open("recCorpusBow.p", "wb"))
    """randomRecipe = recCorpusBow[100]
    print(randomRecipe, recCorpus[100])
    tfidfmodel = models.TfidfModel(recCorpusBow)
    #ldaModel = models.LdaModel(recCorpusBow, 100)
    randomRecipeTfIdf = tfidfmodel[randomRecipe]
    #randomRecipeLda = ldaModel[randomRecipe]

    #cosineSimModel = similarities.MatrixSimilarity(tfidfmodel[recCorpusBow])

    #cosineSimModel.save(open("cosineModel.txt", "wb"))
    tfidfmodel.save(open("tfidf.txt", "wb"))

    cosineSimModel = similarities.MatrixSimilarity.load("cosineModel.txt")
    #ldaCosineModel = similarities.MatrixSimilarity(ldaModel[recCorpusBow])
    similarDocs = cosineSimModel[randomRecipeTfIdf]
    #pickle.dump(similarDocs, open("similarDocs.p", "wb"))

    #similarDocsLda = ldaCosineModel[randomRecipeLda]

    #similarDocs = pickle.load(open("similarDocs.p", "rb"))
    similarDocs = similarDocs.argsort()
    for i in range(1, 26):
        print(recCorpus[similarDocs[-i]])

"""

    """
    cosineSimModel = similarities.MatrixSimilarity.load("cosineModel.txt")
    tfidfModel = models.TfidfModel.load("tfidf.txt")
    recCorpusBow = pickle.load(open("recCorpusBow.p", "rb"))
    index = 0
    while index < len(recCorpus):
        usedRecipesDict = {}
        diff_ings_list = []
        dataProcessed = 0
        for i in range(index, index+10000):
            #print(index, i)

            try:
                recipe = recCorpusBow[i]
                tfidfRecipe = tfidfModel[recipe]
                similarDocs = cosineSimModel[tfidfRecipe].argsort()
                #print("\n\n")
                #print(recCorpus[i])
                #print("\n\n")

                for j in range(2, 27):
                    #print(recCorpus[similarDocs[-j]])
                    different_ings = list(set(recCorpus[i]) - set(recCorpus[similarDocs[-j]]))
                    different_ings.extend(list(set(recCorpus[similarDocs[-j]]) - set(recCorpus[i])))
                    #print(different_ings)
                    #print(different_ings)
                    if len(different_ings) > 1:
                        diff_ings_list.append(different_ings)
            except IndexError:
                break

            dataProcessed += 1
            print("\rProcessed data:", dataProcessed, "/", 10000, end="", flush=True)

        pickle.dump(diff_ings_list, open("differentIngsList" + str(index) + ".p", "wb"))
        index += 10000
        if index >= len(recCorpus):
            index = len(recCorpus) - 1


    #print(len(diff_ings_list))
    #pickle.dump(diff_ings_list, open("differentIngsList.p", "wb"))
    """



    diff_ings_list = []
    picklesLoaded = 0
    for i in range(0, 250000, 10000):
        print("\rPickles loaded:", picklesLoaded, "/", 24, end="", flush=True)
        picklesLoaded += 1
        tempList = pickle.load(open("differentIngs25/differentIngsList" + str(i) + ".p", "rb"))
        diff_ings_list.extend(tempList)


    #print(len(diff_ings_list))




    #model = Word2Vec(diff_ings_list, min_count=35)
    model = FastText(diff_ings_list, size=250, window=5, min_count=10, workers=8, sg=1)
    #model.train(diff_ings_list, total_examples=len(diff_ings_list), epochs=10)
    print(model.wv.most_similar("cream"))

    print(model.wv.most_similar("bacon"))
    print(model.wv.most_similar("cucumber"))
    print(model.wv.most_similar("bread"))

    X = model[model.wv.vocab]
    print(len(X))
    

    """
    NUM_CLUSTERS = 100
    kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance, repeats=25, avoid_empty_clusters=True)
    assigned_clusters = kclusterer.cluster(X, assign_clusters=True)
    print(assigned_clusters)

    words = list(model.wv.vocab)
    clusters = {}
    for i, word in enumerate(words):
        print(word + ":" + str(assigned_clusters[i]))
        if str(assigned_clusters[i]) not in clusters:
            clusters[str(assigned_clusters[i])] = []
        clusters[str(assigned_clusters[i])].append(word)
    print(clusters)
    """

    """
    kmeans = cluster.KMeans(n_clusters=100)
    kmeans.fit(X)

    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    print("Cluster id labels for inputted data")
    print(labels)
    print("Centroids data")
    print(centroids)

    print(
        "Score (Opposite of the value of X on the K-means objective which is Sum of distances of samples to their closest cluster center):")
    print(kmeans.score(X))

    silhouette_score = metrics.silhouette_score(X, labels, metric='euclidean')

    print("Silhouette_score: ")
    print(silhouette_score)
    
    #print(model.most_similar(positive=["tomato"], negative=[], topn=2))
    """
    """
    diff_ings_dict = Dictionary(diff_ings_list)
    #print([[key,diff_ings_dict.get(key)] for key in diff_ings_dict.keys()])
    diff_ings_corpus = [diff_ings_dict.doc2bow(text) for text in diff_ings_list]
    #print(diff_ings_corpus)
    ldaIngs = models.LdaModel(diff_ings_corpus, id2word=diff_ings_dict, num_topics=250)
    #lsiIngs = models.LsiModel(diff_ings_corpus, id2word=diff_ings_dict, num_topics=250)
    #print(recCorpus[1])
    pprint.pprint(ldaIngs.show_topics())
    #pprint.pprint(lsiIngs.show_topics())
    #index, prob = ldaIngs.show_topic(0)[0]
    #print(index, prob)
    #print(diff_ings_dict.get(index))
    #print(diff_ings_corpus[int(index)])
    #print(ldaIngs[recCorpusBow[1]])
    
    """



    #print("\n\n")
    #for i in range(1, 26):
    #    print(recCorpus[similarDocsLda.argsort()[-i]])


    # print(document)
    # print(a.corpus)
    # a.saveCorpus()
    # a.saveTopKIngredients()




