# Group 3
# COEN 281 Final Project
# Winter 2020 - Professor David Anastasiu

import csv
import numpy as np
from efficient_apriori import apriori as eff_app
from collections import Counter
from itertools import chain
import pickle
import random

# save np.load
np_load_old = np.load

# modify the default parameters of np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)

with np.load('/WAVE/users/unix/mputra/COEN281-Recipe-Recommendation-System/data/simplified-recipes-1M.npz') as data:
   recipes = data['recipes']
   ingredients = data['ingredients']

# Pre-Process the  schimdt dataset
schmitd_set = [] #name this to recipe list
for recipe in recipes:
   if(recipe.size) == 0:
       continue
   schmitd_set.append(ingredients[recipe])

#Remove bad data
badingr = []
file1 = open('/WAVE/users/unix/mputra/COEN281-Recipe-Recommendation-System/data/baddata.txt', 'r')
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

idx = Counter(chain.from_iterable(final_set_clean))

#Dividing data into training and test sets

final_training_data = [] #training set to run with apriori
final_test_data = []     #represents ground truth

for row in final_set_clean:   #each row is a recipe i.e list of ingredients
    if len(row) == 0:
        continue    
    test_data = row.pop(random.randrange(len(row)))   #pops out random ingredients from the row
    final_test_data.append(test_data)
    final_training_data.append(row)
    

# Efficient Appriori
itemsets, rules = eff_app(final_training_data, min_support=0.005,  min_confidence=0.005)

pickle.dump(rules, open("pickledRules005gt.pkl", "wb"))
pickle.dump(idx, open("pickledIDX005gt.pkl", "wb"))
pickle.dump(final_test_data, open("pickledGroundTruth005gt.pkl", "wb"))