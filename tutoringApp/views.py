from django.shortcuts import render

# Create your views here.
from .models import users

def test(request):
    obj = users.objects.create(first_name='test', last_name = 'test', email = 'a@test.com')
    obj.save()
    return render(request, 'test.html')