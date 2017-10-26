from django import forms
from django.contrib.auth.models import User
 
class CourseForm(forms.Form):
    name = forms.CharField(label = 'Course Name')
    descriptionHeading = forms.CharField(label = 'Course Description Heading')
    description = forms.CharField(label = 'Course Description')

