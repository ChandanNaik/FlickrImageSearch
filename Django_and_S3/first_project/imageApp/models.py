import os
from django.db import models
from django.core.files.storage import FileSystemStorage

execution_path = os.getcwd()
searchImagePath = os.path.join(execution_path , "imageApp/static/imageApp/searchUploads")

my_store = FileSystemStorage(location=searchImagePath)


class imageModel(models.Model):
	imageFile = models.FileField(storage=my_store)

