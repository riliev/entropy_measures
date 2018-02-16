# in this program I will build wn database using trees. I will start from terminal leaves, and print all paths to the top. Then I will count the mentioning of medium level nodes. Some weighing will be needed since in some cases there will be multiple paths to the top

#r is adverb, n is nouns, v is verb, a is adjective - for the wornet search
import sys
import nltk
from nltk.corpus import wordnet as wn
import operator

#recursive function which will return list of synset part of a tree, + order mentioned
#wn.synset('restrain.v.01').tree(lambda s: s.hypernyms())
import types


def readTreeList(currentList):
    if len(currentList)==2:
        synSetList.append([currentList[0]])
        return readTreeList(currentList[1])
    if len(currentList)== 1:synSetList.append([currentList[0]])

longList1=[]

def readTreeList1 (currentA,newA): #builds list based on current, if fork, builds multiple lists
    new=list(newA)
    current=list(currentA)
    if type(new[-1]) is nltk.corpus.reader.wordnet.Synset:
        current.append(new)
        longList1.append(current)

        return None
    if type(new) is list:
        if len(new)==1: return readTreeList1(current,new)
        if len(new)==2:
            if type(new[0]) is nltk.corpus.reader.wordnet.Synset:
                current.append([new[0]])
                return readTreeList1(current,new[1])
        if len(new)>2:
            readTreeListMulti(current,new)
            return None
        
def readTreeListMulti (currentA,newA):
        new=list(newA)
        current=list(currentA)
        if type(new[-1]) is nltk.corpus.reader.wordnet.Synset: readTreeList1(current,new)
        if type(new) is list:
            for z in range(1,len(new)):
                if type(new[0]) is nltk.corpus.reader.wordnet.Synset:
                    current.append([new[0]])
                    if len(new)==1: readTreeList1(current,new)
                    if len(new)>1: readTreeList1(current,new[z])
                if type(new[0]) is not nltk.corpus.reader.wordnet.Synset:
                    if len(new)==1: readTreeList1(current,new)
                    if len(new)>1: readTreeList1(current,new[z])
           
   
     
    
synSetList=[] #this is used as terminal step to assemble a single path
longList=[] #this assembles all possible paths
numberPathsDict={}#this is used for counting how many times this terminal node participates in the systet

terminalLeavesDict={}#counts number of mentioning

for synset in list(wn.all_synsets('n')):
    if len(synset.hyponyms())==0: # it is easy to add condition here to use only some categories, e.g. only animals, etc.
        synSetList=[]
        list1=synset.tree(lambda s: s.hypernyms())
        numberPathsDict[synset]=len(list1)-1
        readTreeList1([],list1)
longList2=[]

#filter the longlist1, so it will keep only paths which contain a particular node
filterSynset = wn.synset('instrumentality.n.03')
#animal.n.01, plant.n.02, vehicle.n.02, entity.n.01, instrumentality.n.03

longList3=[]
longList3SetList=[]
filteredSynsets=set()
for j in range(len(longList1)):
    buffSet=set()
    for k in range(len(longList1[j])):
        condition=False
        buffSet.update([longList1[j][k][0]])
        if longList1[j][k][0]== filterSynset:
            filteredSynsets.update(buffSet)
            condition=True
            a=k
            break
    if condition:
        if buffSet not in longList3SetList:
            longList3.append(longList1[j][:a+1])
            longList3SetList.append(buffSet)

#remove duplicates
longList1=[]
longList1=[x for x in longList3] #use only the filtered lists



for j in range(len(longList1)):
    if type(longList1[j][0]) is not list: print longList1[j]
    if longList1[j][0][0] in terminalLeavesDict: terminalLeavesDict[longList1[j][0][0]]+=1
    if longList1[j][0][0] not in terminalLeavesDict: terminalLeavesDict[longList1[j][0][0]]=1

import random
dictRand=set()
longListRand =[]
longList3=list(longList1)
random.shuffle(longList3)
for j in range(len(longList3)):
    if longList3[j][0][0] in dictRand: zzzz=1
    if longList3[j][0][0] not in dictRand:
        longListRand.append(longList3[j])
        dictRand.add(longList3[j][0][0])




#print sum orders
allSynsetsOrderSum = {}#this will be the whole synset list with orders, including upper nodes
allSynsetsMentioned= {} #counts each time when a synset is mentioned
allSynsetsMentionedWeighted = {} #weights the counts by number of first node mentioned
allSynsetsMentionedRandom = {}# number mentinoing, if more than one path, randomly exclude one
allSynsetsOrderSumRandom = {} # if more than one path, randomly exclude one
allSynsetsOrderSumReversed = {} #this will the distance from the top


for i in range(len(longList1)):
    for j in range(len(longList1[i])):
        if type(longList1[i][j]) is not list: longList1[i][j] = [longList1[i][j]]
        if type(longList1[i][j]) is list:
            if longList1[i][j][0] in allSynsetsOrderSum:
                allSynsetsOrderSum[longList1[i][j][0]]+=j
                allSynsetsOrderSumReversed[longList1[i][j][0]]+=len(longList1[i])-j
                allSynsetsMentioned[longList1[i][j][0]]+=1
                allSynsetsMentionedWeighted[longList1[i][j][0]]+=1.0/float(terminalLeavesDict[longList1[i][0][0]])

                
            if longList1[i][j][0] not in allSynsetsOrderSum:
                allSynsetsOrderSum[longList1[i][j][0]]=j
                allSynsetsOrderSumReversed[longList1[i][j][0]]=len(longList1[i])-j
                allSynsetsMentioned[longList1[i][j][0]]=1
                allSynsetsMentionedWeighted[longList1[i][j][0]]=1.0/float(terminalLeavesDict[longList1[i][0][0]])
   
for i in range(len(longListRand)):
    for j in range(len(longListRand[i])):
        if type(longListRand[i][j]) is not list: longListRand[i][j] = [longListRand[i][j]]
        if type(longListRand[i][j]) is list:
            if longListRand[i][j][0] in allSynsetsOrderSumRandom:
                allSynsetsOrderSumRandom[longListRand[i][j][0]]+=j
                allSynsetsMentionedRandom[longListRand[i][j][0]]+=1
                
            if longListRand[i][j][0] not in allSynsetsOrderSumRandom:
                allSynsetsOrderSumRandom[longListRand[i][j][0]]=j
                allSynsetsMentionedRandom[longListRand[i][j][0]]=1

def otherInformation (synset1):
    numb_hypernyms=len(synset1.hypernyms())
    numb_hyponyms=len(synset1.hyponyms())
    minDistTop=synset1.min_depth()
    maxDistTop=synset1.max_depth()
    a= [lemma.name for lemma in synset1.lemmas]
    numberLemmas= len(a)
    aSingleWords = filter(lambda x:"_" not in x, a)
    numberSingleLemmas=len(aSingleWords)
    aDoubleWords = filter(lambda x:"_" in x, a)
    numbDoubleLemmas =len(aDoubleWords)
    sum=0
    for b in a: sum+=len(b)
    lengthLemmasSum=sum
    sum=0
    for b in aSingleWords: sum+=len(b)
    lengthSingWordLemmasSum=sum
    sum=0
    for b in aDoubleWords: sum+=len(b)
    lengthDoubleWordLemmasSum=sum

    #here is the information from the tree above (number of termainal nodes contained, etc.)
    totalTerminalNodes = -1 #(total times mentioned in the tree pathx)
    totalTerminalNodesWeighted = -1 #controlling for multiple paths stemming from the same terminal leaves
    rankingSum=-1 #sum of all ranks, based on totalTerminalNodes
    terminalLeave = 0 #if terminal leave, then 1, if not then 0
    numberOfAscendingPaths =-1 #if terminal leave how many ascending paths start from here
    rankingSumReversed=-1

    rankingSumRandom=-1 #randomly excluding multiple paths
    totalTerminalNodesRandom =-1 #randomly excluding multiple paths

    if synset1 in terminalLeavesDict:
        terminalLeave = 1
        numberOfAscendingPaths = terminalLeavesDict[synset1]

    if synset1 in allSynsetsOrderSum:
        rankingSum=allSynsetsOrderSum[synset1]
        rankingSumReversed=allSynsetsOrderSumReversed[synset1]
        totalTerminalNodes=allSynsetsMentioned[synset1]
        totalTerminalNodesWeighted=allSynsetsMentionedWeighted[synset1]


    if synset1 in allSynsetsOrderSumRandom:
        rankingSumRandom=allSynsetsOrderSumRandom[synset1]
        totalTerminalNodesRandom=allSynsetsMentionedRandom[synset1]

    totalTerminalNodes, totalTerminalNodesWeighted, rankingSum, terminalLeave, numberOfAscendingPaths, rankingSumRandom,totalTerminalNodes
    #output1=list([numb_hypernyms,numb_hyponyms,minDistTop,maxDistTop,numberLemmas,numberSingleLemmas,numbDoubleLemmas, lengthLemmasSum, lengthSingWordLemmasSum, lengthDoubleWordLemmasSum,totalTerminalNodes, totalTerminalNodesWeighted, rankingSum, terminalLeave, numberOfAscendingPaths, rankingSumRandom,totalTerminalNodesRandom,rankingSumReversed])
    output1=list([numb_hypernyms,numb_hyponyms,minDistTop,maxDistTop,totalTerminalNodes, totalTerminalNodesWeighted, rankingSum, terminalLeave, numberOfAscendingPaths, rankingSumRandom,totalTerminalNodesRandom,rankingSumReversed])

    return output1

synsetOutput={}   #this combines everything from the synset databse
for synset in filteredSynsets: synsetOutput[synset]=otherInformation(synset)

lemmaOutput={} #this transforms the synset output in lemma based output

#lemmaOutput will be one longer than synsetOutput, last element is counter
for synset1 in synsetOutput:
    lemmaList= [lemma.name for lemma in synset1.lemmas]
    for eachLemma in lemmaList:
        if eachLemma in lemmaOutput:
            for j in range(len(synsetOutput[synset1])):lemmaOutput[eachLemma][j]+=synsetOutput[synset1][j]
            lemmaOutput[eachLemma][j+1]+=1
        if eachLemma not in lemmaOutput:
            buffer1=[]
            for j in range(len(synsetOutput[synset1])):buffer1.append(synsetOutput[synset1][j])
            buffer1.append(1)
            lemmaOutput[eachLemma]=list(buffer1)
                   
#for j in synsetOutput: print j, ",",synsetOutput[j]
    
for j in lemmaOutput: print j, ",",lemmaOutput[j]

#import pattern.en
#for j in lemmaOutput: print pattern.en.pluralize(j)
                                        
   
           


