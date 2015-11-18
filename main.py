__author__ = 'yaelcohen'
import pickle


input = pickle.load(open("all_nodes.p", "rb"))
cluster = pickle.load(open("cluster_text_company_profile_1.1.p", "rb"))
print input
print "-----------"

print cluster
for i in range(999):
    print input[i]["job_title"],"==",input[i]["company"], '==', input[i]["period"],  "---", cluster[i]
