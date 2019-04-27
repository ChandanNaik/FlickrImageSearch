from django import forms

class imageForm(forms.Form):
	imageFile = forms.FileField(label="Choose File") 