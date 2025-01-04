from django.shortcuts import render
from .models import Tutor, HomeContent, Review

def home(request):
    tutors = Tutor.objects.all()
    home_content = HomeContent.objects.all()
    reviews = Review.objects.all()
    context = {'tutors': tutors, 'home_content': home_content, 'reviews': reviews}
    return render(request, 'home/home.html', context)
