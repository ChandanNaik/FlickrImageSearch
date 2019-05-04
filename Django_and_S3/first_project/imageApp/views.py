from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from .models import imageModel
from .forms import imageForm
from .models import searchUploadModel
from .forms import searchUploadForm
from django.views.decorators.csrf import csrf_exempt

import os
import csv
import json
import boto3
import shutil
import operator
import datetime
import flickrapi
import urllib.request
from collections import defaultdict

import numpy as np

import pymongo as pym

import logging

from django.core.cache import cache

from imageai.Detection import ObjectDetection

from imageApp.flickrToS3 import performDumpFunction

from bson.objectid import ObjectId



def search(request):
	execution_path = os.getcwd()
	if request.method == 'POST':
		form = imageForm(request.POST, request.FILES)

		if form.is_valid():
			imageModel.objects.all().delete()
			newImage = imageModel(imageFile = request.FILES['imageFile'])
			newImage.save()
			image = imageModel.objects.all()

			#Generate ML tags for the user uploaded image
			outputPath = os.path.join(execution_path , "imageApp/static/imageApp/searchUploads", "taggedSearchImage.jpg")
			inputPath = os.path.join(execution_path , "imageApp/static/imageApp/searchUploads", image[0].imageFile.name)

			detections = search.detector.detectObjectsFromImage(input_image=inputPath, output_image_path=outputPath)

			listTags = []
			for eachObject in detections:
				listTags.append((eachObject["name"],eachObject["percentage_probability"]/100))

			cache.clear()
			cache.set('searchTags', listTags)

			return render(request, 'imageApp/search.html', {'image':image, 'form':form, 'imagePath':"/static/imageApp/searchUploads/"+ image[0].imageFile.name})

	else:
		if not search.detector:
			search.detector = ObjectDetection()
			search.detector.setModelTypeAsRetinaNet()
			search.detector.setModelPath(os.path.join(execution_path , "imageApp", "resnet50_coco_best_v2.0.1.h5"))
			search.detector.loadModel()
		if(imageModel.objects.all().count()>0):
			imageModel.objects.all().delete()
		form = imageForm()
		image = imageModel.objects.all()
		return render(request, 'imageApp/search.html', {'image':image, 'form':form})

search.detector = None

def searchResults(request):

	userImage = cache.get('prettySearchTags')
	logging.debug('********')
	logging.debug(userImage)

	userTagList=list(userImage["objDetTags"].keys())+list(userImage["flickrTags"].keys())

	requiredIndex=indexRetrieval(userTagList)

	iVD=imageVectorDict(requiredIndex)

	rankedImages = rankImage(userImage,iVD,10)
	lst=[]
	for i in rankedImages:
		lst.append(i[0])

	logging.debug("**^^&&")
	logging.debug(rankedImages)

	#Call to function which returns names of 20 most similar images

	#Returns a list of images that can be put into this dictionary
	data = {
		'resultImageNames' : lst #['33736561448.jpg', '32637487007.jpg', '33792464088.jpg', '40633928313.jpg', '46650222305.jpg', '46742603185.jpg', '47636140071.jpg', '46818395984.jpg']
	}
	return JsonResponse(data)

def dumpToBucket(request):
	return render(request, 'imageApp/dumpToBucket.html')


def performDump(request):

	performDumpFunction(request)

	return render(request, 'imageApp/dumpToBucket.html')

#///////////////////////////////////////////////////////////////////////////////////
#/////////////////////////Similar Image Retrieval///////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////
def indexRetrieval(userTagList):
    locationLst=[]
    client= pym.MongoClient('localhost', 27017)
    collectIndex=client.imageSearch.imageIndex
    for i in userTagList:
        x=collectIndex.find({"tag":i})
        for y in x:
            locationLst=locationLst+y[i]
    return set(locationLst)

def imageVectorDict(requiredIndex):
    client= pym.MongoClient('localhost', 27017)
    collect=client.imageSearch.imageDB
    lst=[]
    for obj_id_to_find in requiredIndex:
        lst+=[i for i in collect.find({"_id": ObjectId(obj_id_to_find)})]
    return lst

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

def rankImage(img,imgList,rank):
    confdict={}
    v1=img
    for i in imgList:
        confdict[i['name']]=cosineEq(v1,i)
    conf=sorted(confdict.items() ,key = operator.itemgetter(1),reverse=True)[:rank]
    return conf
#///////////////////////////////////////////////////////////////////////////////////
#/////////////////////////Functions with pretty HTML////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////
def searchPretty(request):

	return render(request, 'imageApp/index.html')

#search.detector = None

@csrf_exempt
def tagUploadedImage(request):

	if not tagUploadedImage.detector1:
		logging.debug("Initializing detector *@!")
		execution_path = os.getcwd()
		tagUploadedImage.detector1 = ObjectDetection()
		tagUploadedImage.detector1.setModelTypeAsRetinaNet()
		tagUploadedImage.detector1.setModelPath(os.path.join(execution_path , "imageApp", "resnet50_coco_best_v2.0.1.h5"))
		tagUploadedImage.detector1.loadModel()

	if request.method == 'POST':
		#Ensure only one image is in the model
		if(searchUploadModel.objects.all().count()>0):
			searchUploadModel.objects.all().delete()
		form = searchUploadForm(request.POST, request.FILES)
		if form.is_valid():
			searchUploadModel.objects.all().delete()
			newImage = searchUploadModel(upload = request.FILES['upload'])

			#Clear folder
			execution_path = os.getcwd()
			folder = os.path.join(execution_path , "imageApp/static/imageApp/uploads")
			for root, dirs, files in os.walk(folder):
				for f in files:
					os.unlink(os.path.join(root, f))
				for d in dirs:
					shutil.rmtree(os.path.join(root, d))
			newImage.save()
			image = searchUploadModel.objects.all()
			inputPath = os.path.join(execution_path , "imageApp/static/imageApp/uploads", image[0].upload.name)
			newInputPath = os.path.join(execution_path , "imageApp/static/imageApp/uploads", "uploadedImage.jpg")
			os.rename(inputPath, newInputPath)

		#Tag image using ML model
		outputPath = os.path.join(execution_path , "imageApp/static/imageApp/results", "taggedSearchImage.jpg")
		inputPath = os.path.join(execution_path , "imageApp/static/imageApp/uploads", "uploadedImage.jpg")
		detections = tagUploadedImage.detector1.detectObjectsFromImage(input_image=inputPath, output_image_path=outputPath)

		userTagsCombined = dict()
		userTagsCombined["name"]='uploadedImage.jpg'

		mlTags = {}
		for eachObject in detections:
			mlTags[eachObject["name"]]=eachObject["percentage_probability"]/100

		userTagsCombined["objDetTags"]=mlTags

		userlistTag=["abs","efe","hejhe"]

		userTags={}
		for i in userlistTag:
			userTags[i]=1

		userTagsCombined["flickrTags"]=userTags


		cache.clear()
		cache.set('prettySearchTags', userTagsCombined)



	return render(request, 'imageApp/index.html')

tagUploadedImage.detector1 = None

def results(request):
	return render(request, 'imageApp/result.html')

def about(request):
	return render(request, 'imageApp/about.html')

def gallery(request):
	return render(request, 'imageApp/gallery.html')
