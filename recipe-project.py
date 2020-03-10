# Header Files
import csv
import numpy as np
from csv import DictReader
from efficient_apriori import apriori as eff_app
import pickle

# save np.load
np_load_old = np.load

# modify the default parameters of np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)

with np.load('data/simplified-recipes-1M.npz') as data:
    recipes = data['recipes']
    ingredients = data['ingredients']

# Pre-Process the data
ingrlist = [] #name this to recipe list
counter = 0
for recipe in recipes:
    if(recipe.size) == 0:
        continue
    ingrlist.append(ingredients[recipe])
    counter += 1

#Remove bad data
badingr = []

file1 = open('baddata.txt', 'r')
Lines = file1.readlines()
for line in Lines:
   badingr.append(line.strip())

final_training_set = []
for recipe in ingrlist:
   temprecipe = []
   for ingr in recipe:
       if ingr in badingr:
           continue
       temprecipe.append(ingr)
   final_training_set.append(temprecipe)

# Efficient Appriori
itemsets, rules = eff_app(final_training_set, min_support=0.01,  min_confidence=0.1)

for r in rules:
    print(r.confidence, r)

pickle.dump(rules, open("pickledRules", "wb"))
#reconstruct the pickled object
#reconstructedRules = pickle.load(open("pickledRules", "rb"))
