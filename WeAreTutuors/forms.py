from django import forms
from django.contrib.auth.models import User
 
class CourseForm(forms.Form):
    name = forms.CharField()
    descriptionHeading = forms.CharField()
    description = forms.CharField()
    ownerID = forms.CharField()

class EnrolForm(forms.Form):
	courseid = forms.CharField()
	enrolmentcode = forms.CharField()
