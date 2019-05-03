import os
from django.db import models
from django.core.files.storage import FileSystemStorage

execution_path = os.getcwd()
searchImagePath = os.path.join(execution_path , "imageApp/static/imageApp/searchUploads")

my_store = FileSystemStorage(location=searchImagePath)

uploadPath = os.path.join(execution_path , "imageApp/static/imageApp/uploads")
my_store_uploads = FileSystemStorage(location=uploadPath)

class imageModel(models.Model):
	imageFile = models.FileField(storage=my_store)

class searchUploadModel(models.Model):
	upload = models.FileField(storage=my_store_uploads)