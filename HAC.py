__author__ = 'yaelcohen'

import fastcluster
from scipy import cluster
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt
import pickle

## linkage return matrix format:
# A 4 by (n-1) matrix Z is returned. At the i-th iteration, clusters with indices Z[i, 0] and Z[i, 1]
# are combined to form cluster n + i. A cluster with an index less than n corresponds to one of the
# original observations. The distance between clusters Z[i, 0] and Z[i, 1] is given by Z[i, 2].
# The fourth value Z[i, 3] represents the number of original observations in the newly formed cluster.


## Adds the values to the branches in the dendogram
def augmented_dendrogram(*args, **kwargs):
    ddata = cluster.hierarchy.dendrogram(*args, **kwargs)
    if not kwargs.get('no_plot', False):
        for i, d in zip(ddata['icoord'], ddata['dcoord']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            plt.plot(x, y, 'ro')
            plt.annotate("%.3g" % y, (x, y), xytext=(0, -8),
                         textcoords='offset points',
                         va='top', ha='center')

    return ddata

def clusterAndDendogrgam(Metrix):
    out =  fastcluster.linkage(Metrix, method='single', metric='euclidean', preserve_input=True)
    plt.plot()
    dend = augmented_dendrogram(out, p=30, truncate_mode=None, color_threshold=None, get_leaves=True,
                                orientation='top', labels=None, count_sort=False, distance_sort=False,
                                show_leaf_counts=True, no_plot=False, no_labels=False, color_list=None,
                                leaf_font_size=None, leaf_rotation=None, leaf_label_func=None, no_leaves=False,
                                show_contracted=False, link_color_func=None)
    plt.show()
    return out

def GetClusterIds(linkage_matrix, threshold):
    return cluster.hierarchy.fcluster(linkage_matrix, threshold)

input = pickle.load(open("features_text_company_profile.p", "rb"))
#input = pickle.load(open("features_text.p", "rb"))
b = clusterAndDendogrgam(input)
print "Im back"
cluster = GetClusterIds(b,1.1)
print cluster
pickle.dump( cluster, open( "cluster_text_company_profile_1.1.p", "wb" ))
print "Done"

#X = [["a",0.2,2,3,10],["b",0.8,1,3,1],["c",0.1,2,7,8]]

#X = [[0.2,2,3,10],[0.8,1,3,1],[0.1,2,7,8],[0.3,2,3,10],[0.8,2,3,1],[0.1,2,7,2]]
#X=[[0,0.1,0.3,0.7,0.8],[0.1,0,0.35,0.9,0.8],[0.3,0.35,0,0.4,0.4],[0.7,0.9,0.4,0,0.05],[0.8,0.8,0.4,0.05,0]]
#b = clusterAndDendogrgam(X)
#print GetClusterIds(b,0.8)
#print b



#out =  fastcluster.linkage(X, method='single', metric='euclidean', preserve_input=True)
#print out
#plt.plot()
#dend = augmented_dendrogram(out, p=30, truncate_mode=None, color_threshold=None, get_leaves=True, orientation='top', labels=None, count_sort=False, distance_sort=False, show_leaf_counts=True, no_plot=False, no_labels=False, color_list=None, leaf_font_size=None, leaf_rotation=None, leaf_label_func=None, no_leaves=False, show_contracted=False, link_color_func=None)
#print cluster.hierarchy.dendrogram(out)
#cluster.hierarchy.dendrogram(out)
#print "Done# "
#plt.show()