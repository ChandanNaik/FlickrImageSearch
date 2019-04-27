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

import pymongo

import logging



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
	#////////////////////////////////////////////////
	#Gets images from Flickr and dumps to S3 bucket//
	#Author: thanika							   //
	#////////////////////////////////////////////////


	#Create S3 Bucket
	s3_resource = boto3.resource('s3')
	our_bucket = s3_resource.Bucket(name='flickrbigdatacu')

	#Create Flickr object
	key='72867a4388924cd9840ae813f23a70cf'
	secret='49021d0404efb5c3'
	flickr = flickrapi.FlickrAPI(key,secret, format='parsed-json')

	#Dictionary to store image path in S3 and its tags
	#{"id1": {"filename", "tag1", "tag2", "tag3"}, "id2": {"filename", "tag1", "tag2", "tag3"}, "id3": {"filename", "tag1", "tag2", "tag3"}}
	image_dictionary = defaultdict(dict)

	#Specify start and end dates. 
	#For each date, 100 images are obtained by default. To change, vary "per_page".
	#Around 200 days for 100k photos if 500 photos per day
	#From date
	date1 = '2019-03-20' 
	#To date
	date2 = '2019-04-01' 
	start = datetime.datetime.strptime(date1, '%Y-%m-%d')
	end = datetime.datetime.strptime(date2, '%Y-%m-%d')
	step = datetime.timedelta(days=1)

	#For each date
	while start <= end:

		logging.debug(start.date())
		
		#Get 2 most interesting photos for the this date
		apiResult = flickr.interestingness.getList(date = str(start.date()), per_page = '2') 
		photos = apiResult["photos"]["photo"]

		#Dump one by one in S3 bucket
		for photo in photos:

			imageURL = 'https://farm'+str(photo["farm"])+'.staticflickr.com/'+photo["server"]+'/'+photo["id"]+'_'+photo["secret"]+'.jpg'
			
			try:
				urllib.request.urlretrieve(imageURL, 'temporary.jpg')

				#ML object detection here - gives three tags for the image
				#/////////////////////////////////////////////////////////

				#If tags are obtained, then store in dictionary and upload

				#Store in dictionary
				image_dictionary[photo["id"]]["filename"] = photo["id"]+'.jpg'
				image_dictionary[photo["id"]]["tag1"] = 'TAG 1'
				image_dictionary[photo["id"]]["tag2"] = 'TAG 2'
				image_dictionary[photo["id"]]["tag3"] = 'TAG 3'

				#Upload image to S3 Bucket
				our_bucket.upload_file(Filename='temporary.jpg', Key=photo["id"]+'.jpg')
				logging.debug("SUCCESSfully dumped photo with ID: "+photo["id"])

			except:
				logging.debug("FAILED to dump photo with ID: "+photo["id"])

		start += step

	#Dump into json file
	json.dump(image_dictionary, open("image_dictionary.json","w"))

	#our_bucket.download_file('testing.jpg','testing_download.jpg')
	return render(request, 'imageApp/dumpToBucket.html')

def testDB(request):
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient["imagesAndTags"]
	mycol = mydb["imageData"]
	mydoc = mycol.find()
	for x in mydoc:
		logging.debug(x)
	return render(request, 'imageApp/dumpToBucket.html')