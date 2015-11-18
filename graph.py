__author__ = 'yaelcohen'

import pickle

#text += e.source +"^"+e.target+"^" + e.weight + "\n";

def getEdges(all_data_dict):
    edges = []
    for person in all_data_dict:
        #print all_data_dict[person]
        ## I made sure they are ordered by chronological ID
        for i in range(len(all_data_dict[person])-1):
            edges.append({"source_id":all_data_dict[person][i+1]["ID"], "source_title":all_data_dict[person][i+1]["job_title"], "weight":all_data_dict[person][i+1]["period"],
                          "dest_id":all_data_dict[person][i]["ID"], "dest_title":all_data_dict[person][i]["job_title"]})
    return edges


def createOldGraphFile(edges):
    text = ""
    for e in edges:
        text += e["source_title"].encode("utf-8")+"^"+e["dest_title"].encode("utf-8")+"^"+ str(e["weight"]) + "\n"
    f = open('old_graph_1', 'w')
    f.write(text)
    f.close()


def newGraph(all_edges, flat_clusters):
    new_edges=[]
    for e in all_edges:
        try:
            new_edges.append({"Source":flat_clusters[int(e["source_id"])], "Dest": flat_clusters[int(e["source_id"])], "Period":e["weight"] }) ## might need to be -1 CHECK!!!
        except:
            print
    return new_edges


def createNewGraphFile(edges):
    text = ""
    for e in edges:
        try:
            text += str(e['Source'])+"^"+str(e["Dest"])+"^"+ str(e['Period']) + "\n"
        except:
            text=text
    f = open('new_graph_1', 'w')
    f.write(text)
    f.close()
#all_data_dict = pickle.load(open("all_dict_1.p", "rb"))
#e= getEdges(all_data_dict)
#createOldGraphFile(e)
#pickle.dump( e, open( "all_edges_1.p", "wb" ))
#print e
#print len(e)
#print len(all_data_dict)

all_data_dict = pickle.load(open("all_dict_1.p", "rb"))
cluster =pickle.load(open("cluster_1000.p", "rb"))
ng = newGraph(getEdges(all_data_dict), cluster)
print ng
createNewGraphFile(ng)



