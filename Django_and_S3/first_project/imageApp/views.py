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
import datetime
import flickrapi
import urllib.request
from collections import defaultdict

import pymongo as pym

import logging

from django.core.cache import cache

from imageai.Detection import ObjectDetection

from imageApp.flickrToS3 import performDumpFunction

#detectorGlobal = None

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
			#Image model object to search with/ get path of where user given image is
			imageToSearch = request.GET.get('imageToSearch', None)

			#Tags of image
			listTags = cache.get('prettySearchTags')

			logging.debug("***^^^@@@")
			logging.debug(listTags)

			#Call to function which returns names of 20 most similar images

			#Returns a list of images that can be put into this dictionary 
			data = {
				'resultImageNames' : ['33736561448.jpg', '32637487007.jpg', '33792464088.jpg', '40633928313.jpg', '46650222305.jpg', '46742603185.jpg', '47636140071.jpg', '46818395984.jpg']
			}
			return JsonResponse(data)

def dumpToBucket(request):
	return render(request, 'imageApp/dumpToBucket.html')


def performDump(request):

	performDumpFunction(request)

	return render(request, 'imageApp/dumpToBucket.html')

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
		listTags = []
		for eachObject in detections:
			listTags.append((eachObject["name"],eachObject["percentage_probability"]/100))

		cache.clear()
		cache.set('prettySearchTags', listTags)		


	return render(request, 'imageApp/index.html')

tagUploadedImage.detector1 = None

def results(request):
	return render(request, 'imageApp/result.html')	
