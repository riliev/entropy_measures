#in this file we measure enthropy based on the tree path
#we assume equal weight for each of the trees
from nltk.corpus import wordnet as wn
wn.ensure_loaded()

import math

#https://github.com/nltk/nltk/commit/ba8ab7e23ea2b8d61029484098fd62d5986acd9c

#create a dictionary with lemmas only

lemmas_set = set()

for synset in list(wn.all_synsets('n')):
    #print(synset)
    lemmasList = [lemma.name() for lemma in synset.lemmas()]
    #print(lemmasList)
    for j in range(0,len(lemmasList)):
        current_lemma = str(lemmasList[j])
        current_lemma = current_lemma.lower()
        if current_lemma not in  lemmas_set:
           lemmas_set.add(current_lemma)


#function which records the number of syblings for each node in a path
#the last member in the path is ignored since this is the element itsef
current_path = synset.hypernym_paths()[0]
def pathsToSiblings (current_path):
    if current_path[0] != wn.synset('entity.n.01'):
        siblings_ls = ""
    if current_path[0] == wn.synset('entity.n.01'):
        siblings_ls = []
        for j in range(0,len(current_path)-1):
            num_hyponyms = len(current_path[j].hyponyms())
            siblings_ls.append(num_hyponyms)
    return(siblings_ls)

#from a sequence of numbers, compute the enthropy
#based on the number of siblings of node
# return as logarithm

def pathsToenthropy (current_path):
    probability = 1.0
    for j in range(0,len(current_path)):
        if current_path[j] == 0:
            return("")
        probability = probability*(1.0/current_path[j])
    return_value = ""
    if len(current_path) > 0:
       return_value = math.log(probability)
    return(return_value)

counter = 0
for lemma in lemmas_set:
    synsets = wn.synsets(lemma)
    for j in range(0,len(synsets)):
        path_synsets = synsets[j].hypernym_paths()
        for k in range(0,len(path_synsets)):
            path_to_siblings = pathsToSiblings(path_synsets[k])
            enthropy_log = pathsToenthropy(path_to_siblings)
            path_length = len(path_synsets[k])
            if enthropy_log != "":
                print lemma,
                print path_length,
                print enthropy_log
            counter +=1

