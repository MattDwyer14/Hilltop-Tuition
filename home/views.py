from django.shortcuts import render
from .models import Tutor, HomeContent

def home(request):
    return render(request, 'home/home.html')

def home(request):
    tutors = Tutor.objects.all()
    home_content = HomeContent.objects.all()
    context = {'tutors': tutors, 'home_content': home_content}
    return render(request, 'home/home.html', context)
