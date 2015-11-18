__author__ = 'yaelcohen'

# -*- coding: cp1252 -*-
import random
import math


def scaleFree(n, d):
    #create a clique
    graph = []
    edgeNum = 0
    for i in range((2*d +1)):
        graph.append([x for x in range(2*d +1) if x != i])
        edgeNum += 2*d

    #add rest of the nodes
    for newV in range(n-2*d-1):
        adj = []
        for existingV in range(newV+2*d+1):
            p = len(graph[existingV])*1.0/edgeNum
            if (random.random() < p):
                edgeNum += 2
                adj.append(existingV)
                graph[existingV].append(newV+2*d+1)
        graph.append(adj)
    return graph
'''
generates a random graph as follows:
for each node, add d edges, between the node
and a uniformally selected random node in the graph.
n - number of nodes
d - the number of edges added along with each node
Returns:
a graph represented by an adjacency list
'''
def uniformGraph(n,d):
    graph = [[] for x in range(n)]
    for node in range(n):
        a = [x for x in range(n)]
        random.shuffle(a)
        adj = a[:d]
        graph[node] += adj
        for existingNode in adj:
            graph[existingNode].append(node)
    return graph

'''
generates a directed nXn 8-neighbour grid, represented as a directed graph.
An 8-neighbor grid is a grid in which each node (except nodes at the edge of
the grid) is connected to its immediate neighbors to the left, right, up and
down, and the diagonal neighbors (up-left, up-right, down-left and down-right).
The grid should be directed, so edges go in both directions between neighboring
nodes. Then, for each directed edge, rewire it with probability
p. The new target is chosen uniformly at random from all other nodes.
n - number of nodes
p - the probability to reqire an edge
Returns:
a 2D list. each cell (i,j) contains the neighbors of the node in the location
i,j in the grid
'''
def smallWorld(n,p):
    graph = [[[]for x in range(n)] for x in range(n)]
    # generate the 8 neighbor graph
    for row in range(n):
        for col in range(n):
            neighbors = [(row-1,col),(row-1,col+1),(row,col+1), (row+1,col+1), (row+1,col),(row+1,col-1),(row,col-1),(row-1,col-1)]
            for nb in neighbors:
                if isLegalPlace(n, nb[0], nb[1]):
                    graph[row][col].append(nb)
    # rewire edges
    for row in range(n):
        for col in range(n):
            for edge in graph[row][col]:
                if (random.random() < p):
                    a = [(x,y) for x in range(n) for y in range(n) if x!=y]
                    random.shuffle(a)
                    newV = a[1]
                    graph[row][col].append(newV)
                    graph[row][col].remove(edge)
    return graph


def SIRSsimulator(graphDict, psi, pir, prs, stateDict, isFirstRun, numRoundsToRun):
    n = len(graphDict.keys())
    v = graphDict.keys()

    ## INITIALIZE
    if (isFirstRun):
        ## init states to R
        for k in v:
            stateDict[k] = 'S'
        seed = v[random.randint(0,n-1)]
        stateDict[seed] = 'I'
        stateDict['I'] = []
        stateDict['R'] = []
        stateDict['S'] = graphDict.keys()
        stateDict['S'].remove(seed)
        stateDict['I'].append(seed)
    done = False
    roundIter = 0
    while ((numRoundsToRun == -1 and not done) or roundIter < numRoundsToRun):
        if (len(stateDict['I']) == 0):
            done = True
            print "Done after " + str(roundIter) + " rounds"
            break #TODO might need to break

        ### INFECT
        tempI =[]
        for node in stateDict['I']:
            for edge in graphDict[node]:
                if stateDict[edge] == 'S':
                    if (random.random() < psi):
                        stateDict[edge] = 'I'
                        #print " we infected: " + str(edge)
                        stateDict['S'].remove(edge)
                        tempI.append(edge)
        stateDict['I'] = stateDict['I'] + tempI

        ### KILL
        tempI =[]
        for node in stateDict['I']:
            if (random.random() < pir):
                #F "just died: " + str(node)
                stateDict[node] = 'R'
                stateDict['R'].append(node)
                tempI.append(node)
        for node in tempI:
            stateDict['I'].remove(node)

        ### RESURRECTION
        tempR =[]
        for node in stateDict['R']:
            if (random.random() < prs):
                #print "OMG! he's alive!!!!: " + str(node)
                stateDict[node] = 'S'
                stateDict['S'].append(node)
                tempR.append(node)
        for node in tempR:
            stateDict['R'].remove(node)

        roundIter += 1

def convertGraphToDict(graph, is2D):
    gDict = {}
    if (is2D):
        for i in range(len(graph)):
            for j in range(len(graph)):
                gDict[(i,j)] = graph[i][j]
    else:
        for i in range(len(graph)):
            gDict[i] = graph[i]
    return gDict

def isLegalPlace(n, row, column):
    return not (row >= n or row < 0 or column >= n or column < 0)

def cleanGraph(graphDict):
    for key in graphDict.keys():
        graphDict[key] = set(graphDict[key])
        if key in graphDict[key]:
            graphDict[key].remove(key)

def q1():
    n = 10000
    g = scaleFree(n, 3)

    #create L1
    baseL = [x for x in range(n)]
    random.shuffle(baseL)
    L = baseL[:100]
    L1 = baseL[:100]
    for node in L:
        if (len(g[node]) != 0):
            newNode = random.randint(0,len(g[node])-1)
            L1.append(g[node][newNode])
    print len(L)
    print len(L1)

    d = convertGraphToDict(g,False)
    cleanGraph(d)
    stateDict = {}
    SIRSsimulator(d, 0.03, 0, 0, stateDict, True, 1)
    done = False
    rounds = 1
    printed = False
    while (not done):
        #print ','.join([str(rounds),str(len(list(set(stateDict['I']) & set(L)))),str(len(list(set(stateDict['I']) & set(L1))))])
        if (len(list(set(stateDict['I']) & set(L))) >= 30):
            done = True
            print "L is done after %d rounds" % rounds
            continue
        if (len(list(set(stateDict['I']) & set(L1))) >= 30):
            if (not printed):
                print "L1 is done after %d rounds" % rounds
                printed=True
        rounds += 1
        SIRSsimulator(d, 0.03, 0, 0, stateDict, False, 1)

def q2(imunizedNum):
    n = 10000
    d = 3
    sfGraph = scaleFree(n, d)
    #uniGraph = uniformGraph(n,d)
    sfDict = convertGraphToDict(sfGraph, False)
    #uniDict = convertGraphToDict(uniGraph, False)
    cleanGraph(sfDict)
    #cleanGraph(uniDict)

    base = [x for x in range(n)]
    random.shuffle(base)
    immuneRandSF = base[:imunizedNum]
    #immuneRandUni = base[:imunizedNum]

    sort_key = lambda s: (-len(sfDict[s]))
    toSort = sfDict.keys()
    toSort.sort(key=sort_key)
    immuneTopDegSF = toSort[:imunizedNum]
    #sort_key = lambda s: (-len(uniDict[s]))
    #toSort = uniDict.keys()
    #toSort.sort(key=sort_key)
    #immuneTopDegUni = toSort[:imunizedNum]

    #stateDictRandSF = {}
    #initStateDict(stateDictRandSF, sfDict, immuneRandSF)
    #stateDictRandUni = {}
    #initStateDict(stateDictRandUni, uniDict, immuneRandUni)
    stateDictDegSF = {}
    initStateDict(stateDictDegSF, sfDict, immuneTopDegSF)
    #stateDictDegUni = {}
    #initStateDict(stateDictDegUni, uniDict, immuneTopDegUni)

    #print "Running sf Random: "
    #SIRSsimulator(sfDict, 0.2, 0.2, 0, stateDictRandSF, False, -1)
    #print "Number of dead people: " + str(len(stateDictRandSF['R'])-imunizedNum)
    print "Running sf Top deg: "
    SIRSsimulator(sfDict, 0.2, 0, 0, stateDictDegSF, False, -1)
    print "Number of dead people: " + str(len(stateDictDegSF['R'])-imunizedNum)
    #print "Running uni Random: "
    #SIRSsimulator(uniDict, 0.2, 0.2, 0, stateDictRandUni, False, -1)
    #print "Number of dead people: " + str(len(stateDictRandUni['R'])-imunizedNum)
    #print "Running uni top deg: "
    #SIRSsimulator(uniDict, 0.2, 0.2, 0, stateDictDegUni, False, -1)
    #print "Number of dead people: " + str(len(stateDictDegUni['R'])-imunizedNum)

def q3(psi, pir, prs, prwire, fileName, printDist):
    f = open(fileName, 'w')
    g = smallWorld(300, prwire)
    d = convertGraphToDict(g, True)
    cleanGraph(d)
    stateDict = {}
    seed = initStateDict(stateDict, d, [])
    rounds = 1
    lastNumOfR = 0
    while (True):
        if (len(stateDict['I']) == 0 or rounds > 10000):
            break
        SIRSsimulator(d, psi, pir, prs, stateDict, False, 1)
        if printDist:
            #largest distance
            f.write(str(rounds) + "," + str(calcMaxDist(seed,stateDict['I'])) + "\n")
        else:
            #number of removed nodes
            f.write(str(rounds) + "," + str(len(stateDict['R'])-lastNumOfR) + "\n")
            lastNumOfR = len(stateDict['R'])
        rounds += 1
    f.close

def calcMaxDist(seed, infected):
    maxDist = 0
    for node in infected:
        curDist = math.sqrt(pow(node[0]-seed[0],2) + pow(node[1]-seed[1],2))
        if curDist > maxDist :
            maxDist = curDist
    return maxDist

def initStateDict(stateDict, graphDict, Immune):
    n = len(graphDict.keys())
    v = graphDict.keys()
    stateDict['S'] = []
    for k in v:
        if k not in Immune:
            stateDict[k] = 'S'
            stateDict['S'].append(k)
        else:
            stateDict[k] = 'R'
    seed = v[random.randint(0,n-1)]
    while (seed in Immune):
        seed = v[random.randint(0,n-1)]
    stateDict[seed] = 'I'
    stateDict['I'] = []
    stateDict['I'].append(seed)
    stateDict['R'] = Immune
    stateDict['S'].remove(seed)
    return seed

'''
-----------------------------------------------------
'''

def main():
    #g = smallWorld(5,0.2)
    #d = convertGraphToDict(g,True)
    #cleanGraph(d)
    #stateDict = {}
    #SIRSsimulator(d, 0.8, 0.2, 0.5, stateDict, True, 30)
    n = 10000
    d = 3
    sfGraph = scaleFree(n, d)
    sfDict = convertGraphToDict(sfGraph, False)
    sort_key = lambda s: (-len(sfDict[s]))
    toSort = sfDict.keys()
    toSort.sort(key=sort_key)
    f = open(fileName, 'w')
    count = 0
    for node in toSort:
        f.write(str(count)+" "+str(len(sfDict[node]))+"\n")
        count += 1
    f.close()

if __name__ == "__main__":

    fileName = "C:\\Users\\t-inbarn\\Dropbox\\3 year - inbar\\social computing\\neighDist.csv"
    fileName = "/Users/yaelcohen/Documents/neighDist.csv"


    for i in range(1):
        print " "
        #(psi, pir, prs, prwire, fileName, printDist)
        q3(0.05, 0.1, 0.004, 0.3, fileName, False)
        #main()
        #q2(226)