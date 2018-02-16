#r is adverb, n is nouns, v is verb, a is adjective
import sys
from nltk.corpus import wordnet as wn

counter=0
for synset in list(wn.all_synsets('n'))[:100]:
    lenHyper=len(synset.hypernyms())
    lenHypo=len(synset.hyponyms())
    a= [lemma.name for lemma in synset.lemmas]
    aSingleWords = filter(lambda x:"_" not in x, a) # for word length use only single words
    sum=0
    averageLength=1
    for b in aSingleWords:
        sum = sum+len(b)
    if len(aSingleWords)>0 : averageLength = sum/len(aSingleWords)

    
    print synset, ", ", len(synset.hyponyms()),", ", synset.min_depth(),", ", synset.max_depth(),", ", averageLength, ", ",len(aSingleWords), ", ", len(a)
    counter+=1




#number of lemmas, average length (exclude two worded)


#min depth, max depth, number hyponims, 
    
dog=wn.synsets('dog')
dog=dog[0]
hyp = lambda s:s.hypernyms()
from pprint import pprint
pprint(dog.tree(hyp))


car=wn.synsets('car')
car=car[0]
pprint(car.tree(hyp))

hypo = lambda s:s.hyponyms()


pprint(car.tree(hypo))
pprint(dog.tree(hypo))


