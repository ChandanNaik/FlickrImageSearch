# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 18:26:25 2019

@author: divya
"""
from collections import defaultdict
import pymongo as pym
multiple= [ {  "name" : "46797515834.jpg", "objDetTags" : { "bird" : 0.9995936751365662 }, "flickrTags" : {  } },
           {"name" : "47470744832.jpg", "objDetTags" : { "bird" : 0.9995936751365662 }, "flickrTags" : { "daffodil" : 1, "narcis" : 1, "voorjaarsbloeier" : 1, "lente" : 1, "spring" : 1, "vintage lens" : 1, "meyer-optik" : 1, "helioplan 40mm f4,5" : 1, "flare" : 1, "explored" : 1 } },
           { "name" : "46614463795.jpg", "objDetTags" : { "person" : 0.5942013263702393 }, "flickrTags" : { "aonb" : 1, "what" : 1, "beautiful" : 1, "clouds" : 1, "corfe" : 1, "castle" : 1, "dorset" : 1, "dawn" : 1, "rural" : 1, "countryside" : 1, "village" : 1, "history" : 1, "iconic" : 1, "famous" : 1, "england" : 1, "god's" : 1, "rays" : 1, "crepuscular" : 1, "landscape" : 1, "natural" : 1, "purbecks" : 1, "ruins" : 1, "sky" : 1, "tokina 11-20" : 1, "sunrise" : 1 } },
           { "name" : "46803879754.jpg", "objDetTags" : { "bird1" : 0.9989371299743652 }, "flickrTags" : { "merlo" : 1, "narcis" : 1, "voorjaarsbloeier" : 1, "val" : 1, "baganza" : 1, "coth5" : 1 } }]
client= pym.MongoClient('localhost', 27017)
collect=client.imageSearch.imageDB

def update_tags(ref, new_tag):
    collectIndex=client.imageSearch.imageIndex
    collectIndex.update({'ref': ref}, {'$push': {'tags': new_tag}})

def insertImage(image, query):#,invertedIndex):
    client= pym.MongoClient('localhost', 27017)
    collect=client.imageSearch.imageDB
    collectIndex=client.imageSearch.imageIndex
    x=collect.find({"name":image})
    
    if x.count()==0:
        x = collect.insert(query)        
        lstTags=list(set(list(query["objDetTags"].keys())+list(query["flickrTags"].keys())))
        for j in lstTags:
            y=collectIndex.find({"tag":str(j)})
            if y.count()==0:
                print({'tag':str(j),str(j):[x]})
                collectIndex.insert({'tag':str(j),str(j):[x]})              
            else:
                collectIndex.update({'tag':str(j)},{'$push': {str(j): x}})         
    return 


invertedIndex=defaultdict(list)
for j in range(len(multiple)):
    insertImage(multiple[j]["name"], multiple[j])#,invertedIndex)
######################################################################################3
userImage={ "name" : "46803879754.jpg", "objDetTags" : { "bird" : 0.9989371299743652 }, "flickrTags" : { "merlo" : 1, "narcis" : 1, "voorjaarsbloeier" : 1, "val" : 1, "baganza" : 1, "coth5" : 1 }}
    
def indexRetrieval(userTagList):
    locationLst=[]
    client= pym.MongoClient('localhost', 27017)
    collectIndex=client.imageSearch.imageIndex
    for i in userTagList:
        x=collectIndex.find({"tag":i})
        for y in x:
            locationLst=locationLst+y[i]
    return set(locationLst)

userTagList=list(userImage["objDetTags"].keys())+list(userImage["flickrTags"].keys())
requiredIndex=indexRetrieval(userTagList)


from bson.objectid import ObjectId
def imageVectorDict(requiredIndex):
    client= pym.MongoClient('localhost', 27017)
    collect=client.imageSearch.imageDB
    lst=[]
    for obj_id_to_find in requiredIndex:
        lst+=[i for i in collect.find({"_id": ObjectId(obj_id_to_find)})]
    return lst

iVD=imageVectorDict(requiredIndex)

userImage={ "name" : "46803879754.jpg", "objDetTags" : { "bird" : 0.9989371299743652 }, "flickrTags" : { "merlo" : 1, "narcis" : 1, "voorjaarsbloeier" : 1, "val" : 1, "baganza" : 1, "coth5" : 1 }}

def cosineEq(vec1,vec2):
    v1,v2={},{}
    v1.update(vec1['objDetTags'])
    v1.update(vec1['flickrTags'])
    
    v2.update(vec2['objDetTags'])
    v2.update(vec2['flickrTags'])
    
    num = sum(v1[key]*v2.get(key, 0) for key in v1)
    dnum= np.linalg.norm(list(v1.values())) * np.linalg.norm(list(v2.values()))
    if num == 0:
        return 0
    return float(num/dnum)

cosineEq(userImage,iVD[0])

import operator
def rankImage(img,imgList,rank):
    confdict={}
    v1=img
    for i in imgList:
        print(i['name'])
        confdict[i['name']]=cosineEq(v1,i)
    conf=sorted(confdict.items() ,key = operator.itemgetter(1),reverse=True)[:rank]
    return conf    
 
rankImage(userImage,iVD,10)    












    if key in syn_wd.keys():
        syn_wd[key]=1
    
    for i,item in enumerate(jow):        
        wd1=dict(jow.get(item))
        if key in wd1.keys():
            wd1[key]=1
        cos_sim=cosine_sim(syn_wd,wd1)
        confdict[item]= cos_sim
    conf=sorted(confdict.items() ,key = operator.itemgetter(1),reverse=True)[:rank_cutoff]
    




























def cosine_sim(v1, v2):
    num = sum(v1[key]*v2.get(key, 0) for key in v1)
    dnum= np.linalg.norm(list(v1.values())) * np.linalg.norm(list(v2.values()))
    if num == 0:
        return 0
    return float(num/dnum)


def wdimp(jow,wd,rank_cutoff):
    confdict={}
    key='rare'
    
    syn_wd=dict(jow.get(wd))
    if key in syn_wd.keys():
        syn_wd[key]=1
    
    for i,item in enumerate(jow):        
        wd1=dict(jow.get(item))
        if key in wd1.keys():
            wd1[key]=1
        cos_sim=cosine_sim(syn_wd,wd1)
        confdict[item]= cos_sim
    conf=sorted(confdict.items() ,key = operator.itemgetter(1),reverse=True)[:rank_cutoff]
    ##conf=sorted(confdict.items(),key = confdict.get,reverse=True)
    ##covert to dictionary??
    return conf  







collectIndex=client.imageSearch.imageIndex
collectIndex.insert(invertedIndex)

new_tag= ObjectId('5cc7c885d48679e59052123c')
   
    