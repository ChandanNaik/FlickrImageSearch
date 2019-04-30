# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 21:00:01 2019

@author: divya
"""

import pymongo as pym
client= pym.MongoClient('localhost', 27017)

## you can access any of the databases 
showdbs=client.database_names()
print(client.database_names())

##get restaurants db
db = client.restaurants

##Collection Names
print(client.restaurants.collection_names())
collect=client.restaurants.MenuService

##############################################################
##Insert into DB
##############################################################
##Insert one record
test={"price" : 6, "name" : "Chicken Burger", 
 "description" : "chicken, onions, tomatoes, lettuce and oodles of cheese", 
 "calories" : 135 }

x = collect.insert_one(test)

## "_id" value
print(x.inserted_id) 

##Insert Multiple records
listRescords = [  { "price": 3, "name": "cat food", "description":"cat's food",
   "calories":20},
   { "price": 20, "name": "dog food", "description":"dog's food",
   "calories":34},
    { "price": 40, "name": "dummy food", "description":"dummy's food",
   "calories":46}]
x=collect.insert_many(listRescords)
print(x)

###########################################################
##Find in MOngoDB
#########################################################
## Find the first record
x = collect.find_one()
print(x) 

#### Find all records
x=collect.find()
for y in x:
  print(y) 

#### Return only some fields
x=collect.find({"price": 1, "name": 1 })
for x in y:
  print(x) 
  
#########################################################
##Query in MongoDB
#########################################################
myquery = { "name": "dummy food" }
x = collect.find(myquery)

for y in x:
  print(y) 

##Find documents where the name starts with the letter "d" or higher:

myquery = { "name": { "$lt": "d" } }
y = collect.find(myquery)

for x in y:
  print(x) 

##Sort the result alphabetically by name:
x = collect.find().sort("price")
for y in x:
  print(y)   
  
x = collect.find().sort("price",-1)
for y in x:
  print(y)   
  
  
## Delete

##Delete One from DB
myquery = { "name": "dummy food" }
collect.delete_one(myquery) 

##Delete many
myquery = { "name": {"$regex": "dum"} }
x = collect.delete_many(myquery)
print(x.deleted_count, " documents deleted.") 

##Delete All
x = collect.delete_many({})
print(x.deleted_count, " documents deleted.") 

##Delete Collecttion
collect.drop()


#################################################
##Update
###################################################
oldquery = { "name": "dummy food" }
newquery = { "$set": { "price": "12" } }
y=collect.update_one(oldquery, newquery)

for x in collect.find():
  print(x) 
print(y.modified_count, "documents updated.") 

######################################################
##Limit resultd
####################################################

result = collect.find().limit(5)
#print the result:
for x in result:
  print(x) 
  
  
######################################################
##Insert Update
#####################################################
  
def insertImage(image, query, collect):
    x=collect.find({"name":image})
    if x.count()==0:
       x = collect.insert_one(query)
       

        
 
for y in x:
  print(y)   