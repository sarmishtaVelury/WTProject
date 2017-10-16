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