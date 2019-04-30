# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 18:26:25 2019

@author: divya
"""
from collections import defaultdict
import pymongo as pym
multiple= [ {  "name" : "46797515834.jpg", "objDetTags" : { "bird" : 0.9995936751365662 }, "flickrTags" : {  } },
           {"name" : "47470744832.jpg", "objDetTags" : { "bird" : 0.9995936751365662 }, "flickrTags" : { "daffodil" : 1, "narcis" : 1, "voorjaarsbloeier" : 1, "lente" : 1, "spring" : 1, "vintage lens" : 1, "meyer-optik" : 1, "helioplan 40mm f4,5" : 1, "flare" : 1, "explored" : 1 } },
           { "name" : "46614463795.jpg", "objDetTags" : { "person" : 0.5942013263702393 }, "flickrTags" : { "aonb" : 1, "mist" : 1, "beautiful" : 1, "clouds" : 1, "corfe" : 1, "castle" : 1, "dorset" : 1, "dawn" : 1, "rural" : 1, "countryside" : 1, "village" : 1, "history" : 1, "iconic" : 1, "famous" : 1, "england" : 1, "god's" : 1, "rays" : 1, "crepuscular" : 1, "landscape" : 1, "natural" : 1, "purbecks" : 1, "ruins" : 1, "sky" : 1, "tokina 11-20" : 1, "sunrise" : 1 } },
           { "name" : "46803879754.jpg", "objDetTags" : { "bird" : 0.9989371299743652 }, "flickrTags" : { "merlo" : 1, "turdus" : 1, "merula" : 1, "val" : 1, "baganza" : 1, "coth5" : 1 } }]
client= pym.MongoClient('localhost', 27017)
collect=client.imageSearch.imageDB


#x = collect.insert_many(multiple)

#print list of the _id values of the inserted documents:
#print(x.inserted_ids) 


def insertImage(image, query,invertedIndex):
    client= pym.MongoClient('localhost', 27017)
    collect=client.imageSearch.imageDB
    collectIndex=client.imageSearch.imageIndex
    x=collect.find({"name":image})
    
    if x.count()==0:
        x = collect.insert(query)
        
        lstTags=list(set(list(query["objDetTags"].keys())+list(query["flickrTags"].keys())))
        for j in lstTags:
            print(x) 
            invertedIndex[str(j)].append(x)
            print(invertedIndex)
    
            #collectIndex.insert_one(invertedIndex)
            
        print("lstTags",lstTags)
        #print("lstFrTags",lstFrTags)
    return invertedIndex

i=0
invertedIndex=defaultdict(list)
for j in range(len(multiple)):
    i+=1
    print(i)
    invertedIndex=insertImage(multiple[j]["name"], multiple[j],invertedIndex)
   
    
    
    