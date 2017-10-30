from django import forms
from django.contrib.auth.models import User
 
class CourseForm(forms.Form):
    name = forms.CharField(label = 'Course Name')
    descriptionHeading = forms.CharField(label = 'Course Description Heading')
    description = forms.CharField(label = 'Course Description')

class EnrolForm(forms.Form):
	courseid = forms.CharField()
	enrolmentcode = forms.CharField()

class SearchForm(forms.Form):
	search_query = forms.CharField(label = 'Search')