from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from oauth2client.contrib.django_util.models import CredentialsField

# Create your models here.
class CredentialsModel(models.Model):
  id = models.ForeignKey(User, primary_key=True)
  credential = CredentialsField()


class CredentialsAdmin(admin.ModelAdmin):
    pass

class ContactModel(models.Model):
	firstname = models.CharField(max_length=100)
	lastname = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	subject = models.CharField(max_length=100)
	message = models.CharField(max_length=1000)

class Course(models.Model):
    course_id = models.AutoField(primary_key = True)
    course_name = models.CharField(max_length=100)
    course_domain = models.CharField(max_length=100, default='software-development')
    course_description = models.CharField(max_length=1000000, default='This a course on how to develop software well.')
    course_website = models.CharField(max_length = 100, default = 'Coursera')
    def __str__(self):
        return self.course_name

class usermodel(models.Model):
    emailID = models.EmailField(unique = True)
    user_id = models.AutoField(primary_key=True)
