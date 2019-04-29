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

from django.core.cache import cache

from imageai.Detection import ObjectDetection

from imageApp.flickrToS3 import performDumpFunction


def search(request):
	if request.method == 'POST':
		form = imageForm(request.POST, request.FILES)

		if form.is_valid():
			imageModel.objects.all().delete()
			newImage = imageModel(imageFile = request.FILES['imageFile'])
			newImage.save()
			image = imageModel.objects.all()

			#Generate ML tags for the user uploaded image
			execution_path = os.getcwd()
			if not search.detector: 
				search.detector = ObjectDetection()
				search.detector.setModelTypeAsRetinaNet()
				search.detector.setModelPath(os.path.join(execution_path , "imageApp", "resnet50_coco_best_v2.0.1.h5"))
				search.detector.loadModel()

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
			listTags = cache.get('searchTags')

			logging.debug("***^^^@@@")
			logging.debug(listTags)

			#Call to function which returns names of 20 most similar images

			#Returns a list of images that can be put into this dictionary 
			data = {
				'resultImageNames' : ['32528972147.jpg','40524736923.jpg','47427566762.jpg','33615774948.jpg', '47449061351.jpg']
			}
			return JsonResponse(data)

def dumpToBucket(request):
	return render(request, 'imageApp/dumpToBucket.html')


def performDump(request):

	performDumpFunction(request)

	return render(request, 'imageApp/dumpToBucket.html')
