#in this file we measure enthropy based on the tree path
# and how many nodes are contained within each node in the path
# we closely follow Resnik 1995 paper on similarity and Wordnet
#we assume equal weight for each of the trees
from nltk.corpus import wordnet as wn
wn.ensure_loaded()

import math
import numpy as np

#https://github.com/nltk/nltk/commit/ba8ab7e23ea2b8d61029484098fd62d5986acd9c

#create a dictionary with lemmas only



#build a set of all synsets which are part of the rooted tree (entity.n.01)
synset_set = set()
       
for synset in list(wn.all_synsets('n')):
    path_synsets = synset.hypernym_paths()
    for j in range(0,len(path_synsets)):
        current_path = path_synsets[j]
        if current_path[0] == wn.synset('entity.n.01'):
            if synset not in synset_set:
                synset_set.add(synset)


lemmas_set = set()
for synset in synset_set:
    #print(synset)
    lemmasList = [lemma.name() for lemma in synset.lemmas()]
    #print(lemmasList)
    for j in range(0,len(lemmasList)):
        current_lemma = str(lemmasList[j])
        current_lemma = current_lemma.lower()
        if current_lemma not in  lemmas_set:
           lemmas_set.add(current_lemma)



#create different dictionaries based on the what type of path inclusion you have
#split path adds a partial weight for each of the existing paths.
synsetDictMaxPath = {}
synsetDictMinPath = {}
synsetDictSplitPath = {}
synsetDictSumPath = {}
for synset in synset_set:
   synsetDictMaxPath[synset]=0
   synsetDictMinPath[synset]=0
   synsetDictSplitPath[synset]=0
   synsetDictSumPath[synset]=0


def addFrequencies(currentPath, weight):
    # this function takes an ascending path from a synest,
    # and from each synset it adds the weight to dictionary keeping track for all weights
    synsetCurrentDict = {}
    if currentPath[0] == wn.synset('entity.n.01'):
        for j in currentPath:
            synsetCurrentDict[j] = weight
    return(synsetCurrentDict)


#
for synset in synset_set:
    path_synsets = synset.hypernym_paths()
    if len(path_synsets) > 1:
        min_path = min(path_synsets, key=len)
        current_dict = addFrequencies (min_path,1)
        for j in current_dict:
            synsetDictMinPath[j] += current_dict[j]
        max_path = max(path_synsets, key=len)
        current_dict = addFrequencies (max_path,1)
        for j in current_dict:
            synsetDictMaxPath[j] += current_dict[j]
        for j in range(0,len(path_synsets)):
            current_path = path_synsets[j]
            current_dict_sum = addFrequencies (current_path,1)
            current_dict_split = addFrequencies (current_path,1.0/len(path_synsets))
            for k in current_dict_sum:
                synsetDictSumPath[k] += current_dict_sum[k]
                synsetDictSplitPath[k] += current_dict_split[k] 
    if len(path_synsets) == 1:
        current_path = path_synsets[0]
        current_dict = addFrequencies (current_path,1)
        for j in current_dict:
            synsetDictMaxPath[j] += current_dict[j]
            synsetDictMinPath[j] += current_dict[j]
            synsetDictSumPath[j] += current_dict[j]
            synsetDictSplitPath[j] += current_dict[j] 

#it seems that there is small discreapncy between entity.n.01 value for 



#compute information content for lemmas (min, max, average)


def computeEntropy (inputDict):
    #compute probabilities from frequencies
    freq_list = [inputDict[i] for i in inputDict]
    max_count = max(freq_list)
    outputDict = {x: math.log(float(inputDict[x])/max_count,2) for x in inputDict}
    return(outputDict)


synsetDictMaxPath = computeEntropy(synsetDictMaxPath)
synsetDictMinPath = computeEntropy(synsetDictMinPath)
synsetDictSumPath = computeEntropy(synsetDictSumPath)
synsetDictSplitPath = computeEntropy(synsetDictSplitPath)






print "lemma",\
        "min_entropy_list_max",\
        "min_entropy_list_min",\
        "min_entropy_list_sum",\
        "min_entropy_list_split",\
        "max_entropy_list_max",\
        "max_entropy_list_min",\
        "max_entropy_list_sum",\
        "max_entropy_list_split",\
        "np_mean_entropy_list_max",\
        "np_mean_entropy_list_min",\
        "np_mean_entropy_list_sum",\
        "np_mean_entropy_list_split"  


for lemma in lemmas_set:
    synsets = wn.synsets(lemma)
    synsets = [ synset for synset in synsets if synset in synset_set]
    entropy_list_max = [synsetDictMaxPath[i] for i in synsets]
    entropy_list_min = [synsetDictMinPath[i] for i in synsets]
    entropy_list_sum = [synsetDictSumPath[i] for i in synsets]
    entropy_list_split = [synsetDictSplitPath[i] for i in synsets]
    print lemma,\
        round(-min(entropy_list_max),2),\
        round(-min(entropy_list_min),2),\
        round(-min(entropy_list_sum),2),\
        round(-min(entropy_list_split),2),\
        round(-max(entropy_list_max),2),\
        round(-max(entropy_list_min),2),\
        round(-max(entropy_list_sum),2),\
        round(-max(entropy_list_split),2),\
        round(-np.mean(entropy_list_max),2),\
        round(-np.mean(entropy_list_min),2),\
        round(-np.mean(entropy_list_sum),2),\
        round(-np.mean(entropy_list_split),2),\
        len(synsets)
    



#add a version which takes natural frequencies into account (might or might be useful)

