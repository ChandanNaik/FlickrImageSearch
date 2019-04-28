from django.shortcuts import render, redirect
from django.http import JsonResponse 
from django.urls import reverse
from .models import imageModel
from .forms import imageForm

import csv
import json
import boto3
import datetime
import flickrapi
import urllib.request
from collections import defaultdict

import pymongo as pym

import logging

from imageApp.flickrToS3 import performDumpFunction



def search(request):
	if request.method == 'POST':
		form = imageForm(request.POST, request.FILES)
		if form.is_valid():
			imageModel.objects.all().delete()
			newImage = imageModel(imageFile = request.FILES['imageFile'])
			newImage.save()
			image = imageModel.objects.all()
			return render(request, 'imageApp/search.html', {'image':image, 'form':form})
			#return redirect('imageApp-home')
	else:
		if(imageModel.objects.all().count()>0):
			imageModel.objects.all().delete()
		form = imageForm()
		image = imageModel.objects.all()
		return render(request, 'imageApp/search.html', {'image':image, 'form':form})
	
def searchResults(request):
			#Image model object to search with/ get path of where user given image is
			imageToSearch = request.GET.get('imageToSearch', None)

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

def testDB(request):
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient["imagesAndTags"]
	mycol = mydb["imageData"]
	mydoc = mycol.find()
	for x in mydoc:
		logging.debug(x)
	return render(request, 'imageApp/dumpToBucket.html')