import copy
import string
import random
from random import seed
from random import randint

# Printing the List to Check
def ItemListChecker(list_to_print):
    for i in range(len(list_to_print)):
        print(list_to_print[i])


# Finding all subsets of the items
def subsetfinder(items):
    Com = len(items)
    # Genereting all possible N*N sets of items
    for i in range(2 ** Com):
        combinations = []
        for j in range(Com):
            if (i >> j) % 2 == 1:
                combinations.append(items[j])
        yield combinations


# Computing the 1-item frequent candidate item set, and will cover all as frozen set
def computeCandidate1(dataSet):
    C1 = []
    for itemsets in dataSet:
        for item in itemsets:
            if [item] not in C1:
                C1.append([item])
    C1.sort()
    # Mapping C1 Canditae Item Set
    return [frozenset(var) for var in C1]


def supportchecker(Data, Ck, minimumSupport):
    subsetcount = {}
    for transaction in Data:
        for candidate in Ck:
            if candidate.issubset(transaction):
                subsetcount[candidate] = subsetcount.get(candidate, 0) + 1
    itemsnum = float(len(Data))
    returnList = []
    sppData = {}
    for key in subsetcount:
        support = subsetcount[key] / itemsnum
        if support >= minimumSupport:
            returnList.insert(0, key)
        sppData[key] = support
    # Collection of Itemsets That Are Frequent
    return returnList, sppData


def apriorigenerator(Lk, k):
    generetedlist = []
    for i in range(len(Lk)):
        L1 = list(Lk[i])[: k - 2]
        for j in range(i + 1, len(Lk)):
            L2 = list(Lk[j])[: k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                generetedlist.append(Lk[i] | Lk[j])  # Union of the Two List
    return generetedlist


def infrequent_subset(L, Ck, k):
    # This involves deep copy and shallow copy knowledge
    Ck_temp = copy.deepcopy(Ck)
    for i in Ck:
        s = [t for t in i]
        is_subset = subsetfinder(s)
        subsets = [i for i in is_subset]  # Subsets
        for each in subsets:
            if each != [] and each != s and len(each) < k:
                if frozenset(each) not in [t for z in L for t in z]:
                    Ck_temp.remove(i)
                    break
    return Ck_temp


def apriori_alg(dataSet, minSupport):
    C1 = computeCandidate1(dataSet)  # Initial Candidate 1-Itemset
    L1, suppData = supportchecker(dataSet, C1, minSupport)  # Initial Frequent Itemset
    L = [L1]
    k = 2
    while (len(L[k - 2]) > 0):
        Ck = apriorigenerator(L[k - 2], k)
        Ck2 = infrequent_subset(L, Ck, k)  # Pruning the List
        Lk, supportedK = supportchecker(dataSet, Ck2, minSupport)  # Candidate Support Count
        suppData.update(supportedK)  # Adding the Supported Item Set
        L.append(Lk)  # Adding The Itemset that are greater than minimum support ratio
        k = k + 1
    return L[:-1], suppData

#Size of the Random Itemset
def randomNumber():
    seed(1)
    value = randint
    yield value

#Random Item Generator
randomList = []
for i in range(1,50):
    k = randomNumber()
    for j in (1,k):
        rand_char=random.choice(string.ascii_lowercase)
        randomList.append(rand_char)
    print("Created Random List",randomList)

# Using The Sample Itemset
sampledata = [['a', 'c', 'd'], ['b', 'c', 'e'], ['a', 'b', 'c', 'e'], ['b', 'e'], ['b', 'c']]
print("Sample Input Itemset:")
ItemListChecker(sampledata)
L, sppData = apriori_alg(sampledata, 0.02)
print("All Frequent Item Sets of L According to Each Pass:")
ItemListChecker(L)





