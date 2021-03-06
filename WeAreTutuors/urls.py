"""WeAreTutuors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from mainapp import views

urlpatterns = [
	url(r'^$', views.splashscreen),
    url(r'^create/$', views.createuser),
    url(r'^index/$', views.index),
    url(r'^blog/$', views.blog),
    url(r'^blogpost1/$', views.blogpage1),
    url(r'^blogpost2/$', views.blogpage2),
    url(r'^blogpost3/$', views.blogpage3),
	url(r'^courseform/$', views.courseform),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$',views.login),
    url(r'^logout/$', views.logout),
    url(r'^share/$',views.share),
    url(r'^search/$', views.search),
    url(r'^contact/$',views.contact),
    url(r'^course/$',views.courselist),
    url(r'^database/$', views.database_population),
    url(r'^makedatabase/$', views.makedatabase),
    url(r'^enroll/(?P<course_id>[\w{}.-]{1,40})/$', views.studentenroll, name = 'enroll'),
    url(r'^details/(?P<course_id>[0-9]+)/$', views.details, name='details')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

 