from django import forms
from django.contrib.auth.models import User
 
class CourseForm(forms.Form):
    name = forms.CharField()
    descriptionHeading = forms.CharField()
    description = forms.CharField()
    ownerID = forms.CharField()

