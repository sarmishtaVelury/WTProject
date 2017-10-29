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

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_domain = models.CharField(max_length=100)
    course_id = models.IntegerField()
    course_description = models.CharField(max_length=1000000)

    def __str__(self):
        return self.course_name