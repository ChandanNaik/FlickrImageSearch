from django.db import models

class imageModel(models.Model):
	imageFile = models.FileField(upload_to='searchImages/')

