
__author__ = 'yaelcohen'

import graph
import numpy
import scipy
import nltk
import Levenshtein
import difflib
import pickle


## Text features

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

def diffLibDist(a,b):
    return difflib.SequenceMatcher(a=a["job_title"].lower(), b=b["job_title"].lower()).ratio()

def LevRatio(a,b):
    #print unicode(a["job_title"].lower()),"-----",unicode(b["job_title"].lower())
    #print Levenshtein.ratio(unicode(a["job_title"].lower()),unicode(b["job_title"].lower()))
    return Levenshtein.ratio(unicode(a["job_title"].lower()),unicode(b["job_title"].lower()))

def JustLev(a,b):
    return levenshtein(a["job_title"].lower(), b["job_title"].lower())



#wordTokenizer = nltk.tokenize.WhitespaceTokenizer()
# wordsA = wordTokenizer.tokenize(position)
# wordsB = wordTokenizer.tokenize(p)
# #for word in wordsA:
# #    print word# containing a stem of a word?

## might add a lot of false positives
#stem1 =nltk.stem.porter.PorterStemmer()
#stem2 = nltk.stem.lancaster.LancasterStemmer()
#print stem1.stem("doing")
#print stem1.stem("developer")


## Graph Features

def trianagles(all_nodes,edges,full_Matrix):
    toNode={}
    for e in edges:
        if (toNode.has_key(e["source_title"])):
            toNode[e["source_title"]].append(e["dest_title"])
        else:
            toNode[e["source_title"]] = [e["dest_title"]]
    for i in range(len(all_nodes)):
        current =[]
        for index in range(len(all_nodes)):
            current.append(0)
        for node_title in toNode[i["job_title"]]:
            for other_node in  toNode[node_title]:
                if toNode[i["job_title"]].count(other_node)>0:
                    for j in range(len(all_nodes)):
                        if j["job_title"] == node_title:
                            current[j]+= toNode[i["job_title"]].count(other_node)
        current = Normalize(current)
        full_Matrix[i] += current
    return full_Matrix
    #[0]*10


## Profile Features

def period(a):
    if a.has_key("period"):
        try:
            return int(a["period"])*1.0/100
        except:
            return 0
    else:
        return 0

def index(a):
    if a.has_key("index"):
        try:
            return int(a["index"])*1.0/20.0
        except:
            return 0
    else:
        return 0

## Company CrunchBase Features

def LevComapnyNameRatio(a,b):
    if (a["company"].lower()!="" and a["company"].lower() != None and b["company"].lower()!="" and b["company"].lower()!= None):
        return Levenshtein.ratio(unicode(a["company"].lower()), unicode(b["company"].lower()))
    else :
        return 0

def isAcquired(a):
    if a.has_key("is_acquired"):
        return int(a["is_acquired"])
    else:
        return 0

def isPublic(a):
    if a.has_key("is_public"):
        return int(a["is_public"])
    else:
        return 0

def Company_value(a):
    if a.has_key("is_public"):
        return int(a["is_public"])
    else:
        return 0

def Money(a):
    if a.has_key("total_money_raised"):
        try:
            return int(a["total_money_raised"])
        except:
            return 0
    else:
        return 0

def Employees(a):
    if a.has_key("number_of_employees"):
        try:
            return int(a["number_of_employees"])*1.0/80000
        except:
            return 0
    else:
        return 0

def LevCotegoryRatio(a,b):
    if (a.has_key("category") and b.has_key("category")):
        return Levenshtein.ratio(a["category"].lower(), b["category"].lower())
    else:
        return 0



## GENERAL

def RunOverNodes(all_nodes,feature_matrix,func):
    for i in range(len(all_nodes)):
        current_features = []
        for j in range(len(all_nodes)):
            #if i==j:
            #    current_features.append(1) ##might be a bad idea
            #else:
            #print all_nodes[i], "---", all_nodes[j]
            #print "===",func(all_nodes[i],all_nodes[j])
            current_features.append(func(all_nodes[i],all_nodes[j]))
        #current_features = Normalize(current_features)
        feature_matrix[i]+=(current_features)
    return feature_matrix

def RunUnFunc(all_nodes,feature_matrix,func):
    for i in range(len(all_nodes)):
        current = func(all_nodes[i])
        feature_matrix[i].append(current)
    return feature_matrix

def Normalize(feature_matrix):
    #print feature_matrix
    for i in range(len(feature_matrix)):
        feature_matrix[i] = feature_matrix[i]/numpy.linalg.norm(feature_matrix[i])
    return feature_matrix


##a=[1.,2.,3.,2,2,2]
##b=a/numpy.linalg.norm(a)
##print b
##print numpy.linalg.norm(a)

def CalcAllFeatures(all_nodes):
    """

    :param all_nodes:
    """
    ##Prep:
    full_Matrix=[]
    for i in range(len(all_nodes)):
         full_Matrix.append([0])

    ##Text:
    #full_Matrix = RunOverNodes(all_nodes,full_Matrix,diffLibDist)
    full_Matrix = RunOverNodes(all_nodes,full_Matrix,LevRatio)
    #full_Matrix = RunOverNodes(all_nodes,full_Matrix,JustLev)

    # ## Company:
    # full_Matrix = RunOverNodes(all_nodes,full_Matrix,LevCotegoryRatio)
    full_Matrix = RunOverNodes(all_nodes,full_Matrix,LevComapnyNameRatio)
    full_Matrix = RunUnFunc(all_nodes,full_Matrix,Employees)
    #full_Matrix = RunUnFunc(all_nodes,full_Matrix,Money)
    #full_Matrix = RunUnFunc(all_nodes,full_Matrix,Company_value)
    full_Matrix = RunUnFunc(all_nodes,full_Matrix,isPublic)
    full_Matrix = RunUnFunc(all_nodes,full_Matrix,isAcquired)
    #
    # ##Profile:
    full_Matrix = RunUnFunc(all_nodes,full_Matrix,period) ## these two are half normelized
    full_Matrix = RunUnFunc(all_nodes,full_Matrix,index)
    # norm_matrix = []
    # for arr in full_Matrix:
    #     norm = Normalize(arr)
    #     norm_matrix.append(arr)
    ##edges = graph.getEdges
    ##full_Matrix = trianagles(all_nodes,edges,full_Matrix)
    ## Save:
    # print norm_matrix
    print full_Matrix
    pickle.dump(full_Matrix, open("features_text_company_profile.p", "wb" ))
    print "Done"

input = pickle.load(open("all_nodes.p", "rb"))
print input[:10]
CalcAllFeatures(input[:1000])