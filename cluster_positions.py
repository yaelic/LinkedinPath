__author__ = 'yaelcohen'

import nltk
import re
import Levenshtein
import difflib

def levenshteinDistance(s1,s2):
    if len(s1) > len(s2):
        s1,s2 = s2,s1
    distances = range(len(s1) + 1)
    for index2,char2 in enumerate(s2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1+1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]

print(levenshteinDistance("kitten","sitting"))
print(levenshteinDistance("rosettacode","raisethysword"))


def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n

    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]

a = 'Hello, All you people'
b = 'hello, all You peopl'
seq=difflib.SequenceMatcher(a=a.lower(), b=b.lower())
seq.ratio()
# print 0.97560975609756095
Levenshtein.ratio('hello world', 'hello')


def clusterPos(listOfPositions):
    print "clustering"
    wordTokenizer = nltk.tokenize.WhitespaceTokenizer()
    stem1 =nltk.stem.porter.PorterStemmer()
    stem2 = nltk.stem.lancaster.LancasterStemmer()
    clusters = []
    for position in listOfPositions:
        matched = False
        for cluster in clusters:
            for p in cluster:
                # text distances using Levenshtein algo and diffLib package
                if Levenshtein.ratio(position,p)>=0.8 or difflib.SequenceMatcher(position.lower(), p.lower()).ratio()>=0.8:
                    matched = True
                    cluster.append(position)
                    break;
                    # id I think each position should be in one cluster I need to add another break
                if position in p or p in position:
                    matched = True
                    cluster.append(position)
                    break;
                wordsA = wordTokenizer.tokenize(position)
                wordsB = wordTokenizer.tokenize(p)
                #for word in wordsA:
                #    print word
                # containing a stem of a word?


        if matched ==False:
            clusters.append([position])
    myPrint(clusters)

path = "/Users/yaelcohen/Documents/cvs/cvGraph2.txt"

def run(path):
    positions =[]
    file =open(path,'r')
    for line in file:
        parts = line.split("^")
        if parts[0] not in positions:
            positions.append(parts[0])
        if parts.__len__()> 1 and parts[1] not in positions:
            positions.append((parts[1]))

    clusterPos(positions)

def myPrint(clusters):
    for c in clusters:
        print c
        #print "\n"

run(path)