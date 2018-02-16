#r is adverb, n is nouns, v is verb, a is adjective
import sys
import nltk
from nltk.corpus import wordnet as wn
import operator

#in this program we will start with terminal leaves of the wordnet tree, and build a relational database all the way up to the root
#in this version we change table1 to deal only with uniterupted trees


counter = 0
averageNumber = 0
dictHypernyms = {} # this will be a dictionary with hypernyms which are co-parents
setHypernyms = set()
for synset in list(wn.all_synsets('n')):
    #if len(synset.hyponyms())==0: print synset.hyponyms()
    if len(synset.hypernyms())>1:
        a = synset.hypernyms()
        #print synset, " --- ", synset.hypernyms()
        for j in range(len(a)):
            if a[j] in dictHypernyms:
                dictHypernyms [a[j]]+=1
            else:
                dictHypernyms [a[j]]=0
sorted_x = sorted(dictHypernyms.iteritems(), key=operator.itemgetter(1))
a = [x[1] for x in sorted_x]

def addElement (currentList): # this is a recursive function that traverses the tree upwards
    lastElement= currentList[len(currentList)-1]
    if len(lastElement.hypernyms())==0: return currentList
    if len(lastElement.hypernyms())>1: return currentList
    if lastElement.min_depth()==0: return currentList
    else:
        nextElement=lastElement.hypernyms()
        x1=nextElement[0] # this is the element that will be added to the list, make sure it's not list itself
        if len(nextElement)>1:
            buff_dict={}
            for b in range(len(nextElement)): buff_dict[nextElement[b]]= dictHypernyms[nextElement[b]]
            x1=min(buff_dict.items(), key=lambda x: x[1])[0] #chooses the parent with fewer co-parented children
        currentList.append(x1)
        return addElement(currentList)
        

table1 = [] # this will be the initial table that goes bottom up in the tree, different length of rows
for synset in list(wn.all_synsets('n')):
    singleRow=[]
    if len(synset.hyponyms())==0:
        singleRow.append(synset)
        ab=addElement(singleRow)
        singleRow=ab
        table1.append(singleRow)

table2 = [] # w tazi tablica podrawnqwame table 1 da ima ednakwa dyljina na reda
for j in range(len(table1)):
    x=table1[j]
    buffer_line=[]
    for k in range(20-len(x)): buffer_line.append(x[0])
    table2.append(buffer_line + x)

#count number of containing terminal nodes - from table1
distanceUp={}
distanceDown={} # first element is n, second is sum x, third is sum x^2, sd

for j in range(len(table1)):
    x=table1[j]
    for k in range(len(x)):
        if x[k] in distanceDown:
            
            n=distanceDown[x[k]][0]+1
            distDown = k+1
            bufferline=[]
            new=distDown+distanceDown[x[k]][1]
            newSq=distDown*distDown + distanceDown[x[k]][2]
            sd=(n*newSq-new*new)/(n*n-1) #this formula for standard deviation
            distUp=distanceDown[x[k]][4]+len(x)-k-1 #this adds distances up
            bufferline=[n,new,newSq,sd,distUp,distUp/n]
            distanceDown[x[k]]=bufferline
            
        else :
            bufferline=[1,1,1,1,k,k]
            distanceDown [x[k]] = bufferline
#compute co-parented hyponyms (and-coparants)(and for table1), make selective hiearchies (table1)

table4=[] # table whic adds coparanted childrend, and number of parents
for j in distanceDown:
    parents=len(j.hypernyms())
    coParentedChildren=0
    if j in dictHypernyms:
        coParentedChildren=dictHypernyms[j]+1
    distanceDown[j].append(parents)
    distanceDown[j].append(coParentedChildren)
print "n,new,newSq,sd,distUp,distUp/n, numHypernyms, numCoparantedChildren"
for z in distanceDown: print z, ",", distanceDown[z] # this prints the long output

table2a=[[0 for x in range(len(table2[0]))] for x in range(len(table2))]  #looks at the number of co-paranted children
table2b=[[0 for x in range(len(table2[0]))] for x in range(len(table2))] #looks at number of parents
for j in range(len(table2)):
    for k in range(len(table2[j])):
        a=0
        if table2[j][k] in dictHypernyms: a=dictHypernyms[table2[j][k]]+1
        b=len(table2[j][k].hypernyms())
#for z in range(len(table2)):print table2[z],",",table2a[z],",", table2b[z] #this prints the broad output


