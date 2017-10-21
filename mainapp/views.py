from django.shortcuts import render
from django.shortcuts import redirect

import os
import logging
import httplib2

import quickstart

from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from mainapp.models import CredentialsModel
from django.conf import settings
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

def share(request):
	return render(request, 'test.html')

def login(request):
	quickstart.main()
	return redirect('/index/')

