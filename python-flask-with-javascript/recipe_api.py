#Python APIs for our Javascript!
import pickle
import numpy as np
from collections import Counter
from random import choice

class RecipeApi:
    def __init__(self):
        print("Recipe_API object initialized")

    def getListofIngredients(self, pickledCounterObject):
        '''
        params: a pickle file that contains a Counter object of ingredients and its frequency
        returns: an unordered list of unique ingredients
        '''
        ingredientFrequency = self.reconstructPickleObject(pickledCounterObject)
        return list(ingredientFrequency.keys())

    def getKMostPopularIngredients(self, pickledCounterObject):
        '''
        params: a pickle file that contains a Counter object of ingredients and its frequency
        returns: a list of top k most frequent ingredient
        '''
        ingredientFrequency = self.reconstructPickleObject(pickledCounterObject)
        return ingredientFrequency.most_common(5)

    def predict(self, listOfUserIngredients, pickledRules, final_training_data, pickledGroundTruth):
        '''
        params: a list of ingredients that the user enters, pickled object of the rules from the Association Rule Mining
        returns: the predicted ingredient using Association Rule Mining
        '''
        print(listOfUserIngredients)
        generatedRules = self.reconstructPickleObject(pickledRules)
        final_test_data = self.reconstructPickleObject(pickledGroundTruth)
        topKFinding = []
        for r in generatedRules:
            #print("LHS =", set(listOfUserIngredients))
            #print("RHS =", set(list(r.lhs)))
            if set(listOfUserIngredients) == set(list(r.lhs)):
                #Add Tuple of RHS and confidence to topKFinding
                topKFinding.append((list(r.rhs), r.confidence))
        #Sort top k ingredients mapped from ARM in decreasing order of confidence
        topKFinding.sort(key = lambda x: -x[1])
        k = 3
        topKFinding = topKFinding[0:k]
        print(topKFinding)

        index_found = 0
        map_ingr = {}

        # Counts no of times an ingr is found in ground truth
        for top_ingr in topKFinding:
            map_ingr[top_ingr[0][0]] = 0

        for recipe in final_training_data:
            if set(listOfUserIngredients).issubset(set(recipe)):
                #Checks if ingredient found in ground truth is actually what we predicted
                if final_test_data[index_found] in map_ingr:
                    #if yes then increase count
                    map_ingr[final_test_data[index_found]] += 1
            index_found += 1

        #Calucating ARHR
        k = 1
        hits = 0
        summation = 0

        for top_ingr in topKFinding:
            # if there was a hit for rank k-th item
            if map_ingr[top_ingr[0][0]] > 0:
                summation += 1.0 / k
                hits += 1
            k += 1

        if hits == 0:
            arhr = 0
        else:
            arhr = summation/hits

        return arhr, topKFinding

    def supriseIngredient(self, n = 10):
        '''
        params: n is bottom n least common frequency (default=10)
        returns: a random ingredient of the n-lowest frequency
        '''
        ingredientFrequency = self.reconstructPickleObject(pickledCounterObject)
        leastCommon = ingredientFrequency.most_common(n)[:-n:-1]
        return choice(leastCommon)[0]

    def reconstructPickleObject(self, pickledFile):
        '''
        params: a pickle file
        returns: a/n (list) of object(s) of the pickled file
        '''
        with open(pickledFile, 'rb') as f:
            objects = pickle.load(f)
        return objects

    def recreateTrainingSet(self, pickledGroundTruth):
        '''
        params: the pickled ground truth file
        returns: a list of recipes with the ground truth removed
        '''
        groundTruth = self.reconstructPickleObject(pickledGroundTruth)
        # save np.load
        np_load_old = np.load
        # modify the default parameters of np.load
        np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)

        with np.load('data/simplified-recipes-1M.npz') as data:
            recipes = data['recipes']
            ingredients = data['ingredients']

        schmitd_set = []

        for recipe in recipes:
            if(recipe.size) == 0:
                continue
            schmitd_set.append(ingredients[recipe])

        #Remove bad data
        badingr = []
        file1 = open('data/baddata.txt', 'r')
        Lines = file1.readlines()
        for line in Lines:
            badingr.append(line.strip())

        final_set_badwords= schmitd_set
        final_set_clean = []
        for recipe in final_set_badwords:
            temprecipe = []
            for ingr in recipe:
                if ingr in badingr:
                    continue
                temprecipe.append(ingr)
            final_set_clean.append(temprecipe)

        final_training_data = []
        for row in final_set_clean:   #each row is a recipe i.e list of ingredients
            if len(row) == 0:
                continue
            final_training_data.append(row)

        print(len(final_training_data))
        print(type(groundTruth))
        print(len(groundTruth))

        i = 0
        trainingSet = []
        for recipe in final_training_data:
            if groundTruth[i] in recipe:
                temp = np.delete(recipe, np.where(recipe == groundTruth[i]))
                trainingSet.append(temp)
                i +=1
            else:
                print("Something is wrong with the ground truth")
        return trainingSet
