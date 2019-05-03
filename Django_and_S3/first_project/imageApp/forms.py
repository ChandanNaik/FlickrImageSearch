from django import forms

class imageForm(forms.Form):
	imageFile = forms.FileField(label="Choose File") 

class searchUploadForm(forms.Form):
	upload = forms.FileField(label="Choose File1")