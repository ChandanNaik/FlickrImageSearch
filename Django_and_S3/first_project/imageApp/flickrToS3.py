from django.shortcuts import render, redirect
from django.http import JsonResponse 
from django.urls import reverse
from .models import imageModel
from .forms import imageForm

import os
import csv
import json
import boto3
import datetime
import flickrapi
import urllib.request
from collections import defaultdict

import pymongo as pym

import logging

from imageai.Detection import ObjectDetection

def tagImage(detector):
	execution_path = os.getcwd()
	inputPath = os.path.join(execution_path , "imageApp", "temporary.jpg")
	outputPath = os.path.join(execution_path , "imageApp", "temporaryTagged.jpg")
	detections = detector.detectObjectsFromImage(input_image=inputPath, output_image_path=outputPath)
	listTags = []
	for eachObject in detections:
		listTags.append((eachObject["name"],eachObject["percentage_probability"]/100))

	return listTags


def initMlImageTagging():
	detector = ObjectDetection()
	detector.setModelTypeAsRetinaNet()
	execution_path = os.getcwd()
	logging.debug(os.path.join(execution_path , "imageApp", "resnet50_coco_best_v2.0.1.h5"))
	detector.setModelPath(os.path.join(execution_path , "imageApp", "resnet50_coco_best_v2.0.1.h5"))
	detector.loadModel()
	return detector

def insertImage(image, query):
	client= pym.MongoClient('localhost', 27017)
	collect=client.imageSearch.imageDB
	x=collect.find({"name":image})
	if x.count()==0:
		x = collect.insert_one(query)

def insertIndex(image, query):#,invertedIndex):
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

def performDumpFunction(request):
	#////////////////////////////////////////////////
	#Gets images from Flickr and dumps to S3 bucket//
	#////////////////////////////////////////////////

	#Create S3 Bucket
	s3_resource = boto3.resource('s3')
	our_bucket = s3_resource.Bucket(name='flickrbigdatacu')

	#Create Flickr object
	key='72867a4388924cd9840ae813f23a70cf'
	secret='49021d0404efb5c3'
	flickr = flickrapi.FlickrAPI(key,secret, format='parsed-json')

	#Specify start and end dates. 
	#For each date, 100 images are obtained by default. To change, vary "per_page".
	#Around 200 days for 100k photos if 500 photos per day

	#From date
	date1 = '2019-04-1' 
	#To date
	date2 = '2019-04-10' 
	start = datetime.datetime.strptime(date1, '%Y-%m-%d')
	end = datetime.datetime.strptime(date2, '%Y-%m-%d')
	step = datetime.timedelta(days=1)

	#Initialize ML Tagging Detector
	detector = initMlImageTagging()

	#For each date
	photoCnt=0
	while start <= end:

		logging.debug(start.date())
		
		#Get 2 most interesting photos for the this date
		apiResult = flickr.interestingness.getList(date = str(start.date()), per_page = '50') 
		photos = apiResult["photos"]["photo"]

		#Dump one by one in S3 bucket
		
		for photo in photos:

			imageURL = 'https://farm'+str(photo["farm"])+'.staticflickr.com/'+photo["server"]+'/'+photo["id"]+'_'+photo["secret"]+'.jpg'
			
			try:
				urllib.request.urlretrieve(imageURL, 'imageApp/temporary.jpg')
				image_dictionary={}

				#ML object detection 
				listName = tagImage(detector)

				#If tags are obtained, then store in dictionary and upload

				#Store in dictionary 
				#ML tags
				image_dictionary["name"]=photo["id"]+'.jpg' 
				#logging.debug("image_dictionary")
				#logging.debug(image_dictionary)

				mlTags = {}
				for k in range(len(listName)):
					tagname=listName[k][0].lower()
					mlTags[tagname]=listName[k][1]
			

				#logging.debug("mlTags")
				#logging.debug(mlTags)

				image_dictionary["objDetTags"]=mlTags  
				
				#Store in dictionary
				#Flickr tags
				fDict = {}
				
				tagResult = flickr.photos.getInfo(photo_id = str(photo["id"]))
				flickrTags = tagResult["photo"]["tags"]["tag"]
				print("Tags from Flickr for photo with ID ",str(photo["id"]))

				for fTag in flickrTags:
					tagname = fTag["raw"].lower()
					fDict[tagname] = 1
				
				#logging.debug("fDict")
				#logging.debug(fDict)
				
				image_dictionary["flickrTags"]=fDict


				
				#logging.debug(image_dictionary)

				insertIndex(image_dictionary['name'], image_dictionary)
				photoCnt+=1
				
				#Upload image to S3 Bucket
				our_bucket.upload_file(Filename='imageApp/temporary.jpg', Key=photo["id"]+'.jpg')
				logging.debug("SUCCESSfully dumped photo with ID: "+photo["id"])

			except:
				logging.debug("FAILED to dump photo with ID: "+photo["id"])

		start += step



	#our_bucket.download_file('testing.jpg','testing_download.jpg')

#//////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////Dump images with those specific 80 tags/////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////
def performDumpFunction1(request):
	#////////////////////////////////////////////////
	#Gets images from Flickr and dumps to S3 bucket//
	#////////////////////////////////////////////////

	#Create S3 Bucket
	s3_resource = boto3.resource('s3')
	our_bucket = s3_resource.Bucket(name='flickrbigdatacu')

	#Create Flickr object
	key='72867a4388924cd9840ae813f23a70cf'
	secret='49021d0404efb5c3'
	flickr = flickrapi.FlickrAPI(key,secret, format='parsed-json')

	#Initialize ML Tagging Detector
	detector = initMlImageTagging()

	#For each date
	photoCnt=0


	#List of tags
	tagsAll = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]
	tag = "toothbrush"
	
	logging.debug("@@@Starting tag "+tag)
	#Get 2 most interesting photos for the this date
	apiResult = flickr.photos.search(tags = tag, per_page = '20') 
	photos = apiResult["photos"]["photo"]

	#Dump one by one in S3 bucket
	
	for photo in photos:

		imageURL = 'https://farm'+str(photo["farm"])+'.staticflickr.com/'+photo["server"]+'/'+photo["id"]+'_'+photo["secret"]+'.jpg'
		
		try:
			urllib.request.urlretrieve(imageURL, 'imageApp/temporary.jpg')
			image_dictionary={}

			#ML object detection 
			listName = tagImage(detector)

			#If tags are obtained, then store in dictionary and upload

			#Store in dictionary 
			#ML tags
			image_dictionary["name"]=photo["id"]+'.jpg' 
			#logging.debug("image_dictionary")
			#logging.debug(image_dictionary)

			mlTags = {}
			for k in range(len(listName)):
				tagname=listName[k][0].lower()
				mlTags[tagname]=listName[k][1]
		

			#logging.debug("mlTags")
			#logging.debug(mlTags)

			image_dictionary["objDetTags"]=mlTags  
			
			#Store in dictionary
			#Flickr tags
			fDict = {}
			
			tagResult = flickr.photos.getInfo(photo_id = str(photo["id"]))
			flickrTags = tagResult["photo"]["tags"]["tag"]
			print("Tags from Flickr for photo with ID ",str(photo["id"]))

			for fTag in flickrTags:
				tagname = fTag["raw"].lower()
				fDict[tagname] = 1
			
			#logging.debug("fDict")
			#logging.debug(fDict)
			
			image_dictionary["flickrTags"]=fDict


			
			#logging.debug(image_dictionary)

			insertIndex(image_dictionary['name'], image_dictionary)
			photoCnt+=1
			
			#Upload image to S3 Bucket
			our_bucket.upload_file(Filename='imageApp/temporary.jpg', Key=photo["id"]+'.jpg')
			logging.debug("SUCCESSfully dumped photo with ID: "+photo["id"])

		except:
			logging.debug("FAILED to dump photo with ID: "+photo["id"])
		logging.debug("@@@Finished tag "+tag)
