from django.shortcuts import render
from .models import Tutor

def home(request):
    return render(request, 'home/home.html')

def home(request):
    tutors = Tutor.objects.all()
    context = {'tutors': tutors}
    return render(request, 'home/home.html', context)
