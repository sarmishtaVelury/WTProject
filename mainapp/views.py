from __future__ import print_function
import httplib2
import os
import csv

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from django.shortcuts import render
from django.shortcuts import redirect
from .models import Course

import logging

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from mainapp.models import CredentialsModel
from django.conf import settings
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from WeAreTutuors.forms import CourseForm, EnrolForm


try:
    import argparse
    flags = tools.argparser.parse_args([])
except ImportError:
    flags = None

credentials = []


# Create your views here.
def index(request):
    return render(request, 'index.html')

def courseform(request):

    if(request.method == 'POST'):
        credentials = get_credentials()
        form = CourseForm(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            course = {
                'name': cd['name'],
                'section': 'Period 0',
                'descriptionHeading': cd['descriptionHeading'],
                'description': cd['description'],
                'room': '0',
                'ownerId': 'me',
                'courseState': 'ACTIVE'
            }
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('classroom', 'v1', http=http)
            course = service.courses().create(body=course).execute()
            return courselist(request,credentials)
                #Course.objects.create(lender=cd['lender'],product_name=cd['product_name'],product_description=cd['product_description'])

    else:
        form = CourseForm()
        return render(request, 'register.html', {'form':form}) 

def details(request, course_id):
    course = Course.objects.get(course_id = course_id)
    return render(request, 'detail.html', {'course':course})

def share(request):
    return render(request, 'test.html')

def courselist(request, credentials):

    courses = get_courses(credentials)
    for course in courses:
        print(course)
        coursename = course['name']
        courseid = course['id']
        coursedescription = course['descriptionHeading']
        try:
            old_course = Course.objects.get(course_id = courseid)
        except:
            new_course = Course.objects.create(course_name = coursename, course_id = courseid, course_description = coursedescription)

    courselist = Course.objects.all()
    print(len(courselist))
    return render(request, 'category-full.html',{'courselist':courselist})

    return render(request, 'category-full.html', {'courselist':courselist})

def studentenroll(request,course_id):
    credentials = get_teacher_credentials()
    if(request.method == 'GET'):

        # try:
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('classroom', 'v1', http=http)
        course = service.courses().get(id=course_id).execute()
        print(course)
        course_id = course['id']#provided by teacher to student in person, we will get it from forms#provided by teacher to student in person, we will get it from forms
        student = {'userId': 'sammythesparkleberry@gmail.com'}
            
            # try:
        student = service.invitations().create(body = {'courseId':course_id, 'role':'STUDENT', 'userId':'sammythesparkleberry@gmail.com'}).execute()

        return courselist(request,credentials)
        #     except errors.HttpError as e:
        #         error = simplejson.loads(e.content).get('error')
        #         if(error.get('code') == 409):
        #             print ('You are already a member of this course.')
        #         else:
        #             raise

        # except errors.HttpError as e:
        #     error = simplejson.loads(e.content).get('error')
        #     if(error.get('code') == 404):
        #         print("course not found")
        #     else:
        #         raise

def login(request):

    credentials = get_credentials()
    print(credentials)
    return courselist(request,credentials)

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/classroom.googleapis.com-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/classroom.courses', 'https://www.googleapis.com/auth/classroom.rosters', 'https://www.googleapis.com/auth/classroom.coursework.me', 'https://www.googleapis.com/auth/classroom.coursework.students', 'https://www.googleapis.com/auth/classroom.announcements', 'https://www.googleapis.com/auth/classroom.profile.emails']
CLIENT_SECRET_FILE = 'clientID.json'
APPLICATION_NAME = 'WeAreTutors'

def logout(request):
    return redirect('/')

def contact(request):
    return render(request, 'contact.html')

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'clientID.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_teacher_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.teachercredentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'clientID.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_courses(credentials):
    """Shows basic usage of the Classroom API.

    Creates a Classroom API service object and prints the names of the first
    10 courses the user has access to.
    """
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('classroom', 'v1', http=http)

    results = service.courses().list(pageSize=10).execute()
    courses = results.get('courses', [])

    if not courses:
        print('No courses found.')
    else:
        print('Courses:')
        for course in courses:
            print(course['name'])

    return courses

def database_population(request):
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.databasecredentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'clientID.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    
    curr_dir = os.getcwd()
    csv_path = os.path.join(curr_dir, 'scraping/courseCatalog.csv')

    with open(csv_path) as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            course_id = row[0]
            course_name = row[1]
            course_description = row[2]

            try:
                old_course = Course.objects.get(course_id = course_id)
            except:
                new_course = Course.objects.create(course_name = course_name, course_id = course_id, course_description = course_description)

            course = {
                'name': course_name,
                'section': 'Period 0',
                'descriptionHeading': 'none',
                'description': course_description,
                'room': '0',
                'ownerId': 'me',
            }

            http = credentials.authorize(httplib2.Http())
            service = discovery.build('classroom', 'v1', http=http)
            course = service.courses().create(body=course).execute()
            return courselist(request,credentials)
#def create_course(credentials):