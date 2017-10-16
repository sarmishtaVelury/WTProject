from django.shortcuts import render

import os
import logging
import httplib2

from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django_sample.plus.models import CredentialsModel
from django_sample import settings
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage

# Create your views here.
FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope='https://www.googleapis.com/auth/classroom.courses',
    redirect_uri='http://localhost:8000')

def index(request):
	return render(request, 'index.html')

def register(request):
	return render(request, 'register.html')	
