from parser import parseFile

__author__ = 'yaelcohen'

### go over the folder parse each file
## manage global ids
## create big diction

import glob
import pickle


id = 0
all = {}
all_nodes = []
path = "/Users/yaelcohen/Documents/cvs/cvs_out/*.html"
for fname in glob.glob(path):
    #if (id > 1000):
    #    break
    print "working on " + fname
    cv, id = parseFile(fname,id);
    all_nodes += cv
    all[fname] = cv

print all
print id
pickle.dump( all, open( "all_dict_2.p", "wb" ))
pickle.dump( all_nodes, open( "all_nodes_2.p", "wb" ))

## all_nodes = pickle.load( open( "all_nodes.p", "rb" ) )
print "DONE"