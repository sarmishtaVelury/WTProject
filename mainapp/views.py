from __future__ import print_function
import httplib2
import os
import csv

from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from django.shortcuts import render
from django.shortcuts import redirect
from .models import Course, usermodel

import logging

from googleapiclient.discovery import build
from googleapiclient import errors
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from mainapp.models import CredentialsModel
from django.conf import settings
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from WeAreTutuors.forms import CourseForm, EnrolForm, SearchForm, ContactForm
from mainapp.models import ContactModel

try:
    import argparse
    flags = tools.argparser.parse_args([])
except ImportError:
    flags = None

credentials = []


def splashscreen(request):
    return render(request, 'introindex.html')

# Create your views here.
def index(request):
    form = SearchForm()
    return render(request, 'index.html', {'form':form})

def search(request):
    if(request.method == 'POST'):
        form = CourseForm(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            print(Course.objects.annotate(search=SearchVector('course_name', 'course_description', 'course_domain'),).filter(search=cd['search_query']))
    return HttpResponse("hello")


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
                #'ownerId': 'me',
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
    recommendations = Course.objects.exclude(course_id = course.course_id).filter(course_description = course.course_description)[0:3]
    return render(request, 'detail.html', {'course':course, 'recommendations':recommendations})

def share(request):
    return render(request, 'test.html')

def courselist(request):
    courselist = Course.objects.all()
    print(len(courselist))
    return render(request, 'category-full1.html',{'courselist':courselist})

def studentenroll(request,course_id):
    credentials = get_teacher_credentials()
    if(request.method == 'GET'):

        try:
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('classroom', 'v1', http=http)
            course = service.courses().get(id=course_id).execute()
            course_id = course['id']#provided by teacher to student in person, we will get it from forms#provided by teacher to student in person, we will get it from forms
            student = {'userId': 'sammythesparkleberry@gmail.com'}
                
            try:
                student = service.invitations().create(body = {'courseId':course_id, 'role':'STUDENT', 'userId':'sammythesparkleberry@gmail.com'}).execute()
            except errors.HttpError as e:
                # error = simplejson.loads(e.content).get('error')
                # if(error.get('code') == 409):
                print (e)
                # else:
                #     raise
            print("\n\n\n")
            print(student)

        except errors.HttpError as e:
            error = simplejson.loads(e.content).get('error')
            if(error.get('code') == 404):
                print("course not found")
            else:
                raise

        return login(request)

def login(request):

    credentials = get_credentials()
    print(credentials)
    courses = get_courses(credentials)
    courselist = []
    for course in courses:
        print(course)
        coursename = course['name']
        courseid = course['id']
        coursedescription = course['descriptionHeading']
        try:
            course = Course.objects.get(course_id = courseid)
        except:
            course = Course.objects.create(course_name = coursename, course_id = courseid, course_description = coursedescription)

        courselist.append(course)

    print(len(courselist))
    return render(request, 'category-full.html',{'courselist':courselist})

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/classroom.googleapis.com-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/classroom.courses', 'https://www.googleapis.com/auth/classroom.rosters', 'https://www.googleapis.com/auth/classroom.coursework.me', 'https://www.googleapis.com/auth/classroom.coursework.students', 'https://www.googleapis.com/auth/classroom.announcements', 'https://www.googleapis.com/auth/classroom.profile.emails']
CLIENT_SECRET_FILE = 'clientID.json'
APPLICATION_NAME = 'WeAreTutors'

def logout(request):
    return redirect('/')

def contact(request):
    if request.method == 'POST':
        dta = ContactForm(request.POST or None)
        cd = dta.cleaned_data
        if dta.is_valid():
            fname =cd['firstname']
            lname = cd['lastname']
            email =cd['email']
            sub = cd['subject']
            msg = cd['message']

            obj = ContactModel.objects.create(firstname = fname, lastname = lname, email = email, subject = sub, message = msg)
            return render(request, 'index.html')
    else:
        return render(request, 'contact.html', {'form':ContactForm})

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
    credential_path = os.path.join(credential_dir, 'classroom.googleapis.com-python-quickstart.json')

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
    credential_path = os.path.join(credential_dir, 'classroom.googleapis.com-python-quickstart.json')

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

    results = service.courses().list(pageSize=1000).execute()
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
    credential_path = os.path.join(credential_dir, 'classroom.googleapis.com-python-quickstart.json')

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
            course_domain = row[1]
            course_name = row[2]
            course_description = row[3]

            course = {
                'name': course_name,
                'descriptionHeading': course_domain,
                'description': course_description,
                'room': '0',
                'ownerId': 'me',
            }

            http = credentials.authorize(httplib2.Http())
            service = discovery.build('classroom', 'v1', http=http)
            course = service.courses().create(body=course).execute()
        
    return courselist(request,credentials)
#def create_course(credentials):

def createuser(request):
    if(request.method == 'GET'):
        # form = UserCreateForm(request.POST or None)
        # cd = form.cleaned_data
        # if dta.is_valid():
        #     email =cd['email']
        obj = usermodel.objects.create(emailID = 'sarmishta1.velury@gmail.com')
        objects = usermodel.objects.all()
        return HttpResponse(objects)

    return HttpResponse("not made")