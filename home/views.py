from django.shortcuts import render
from .models import Tutor, HomeContent, Review, Expertise

def meettheteam(request):
    expertise_qs = Expertise.objects.all()
    
    selected_tise = request.GET.getlist('expertise')
    
    tutors = Tutor.objects.all()
    if selected_tise:
        tutors = tutors.filter(expertise__name__in=selected_tise).distinct()
    
    context = {
        'team': tutors,
        'expertise': expertise_qs,
        'selected_tise': selected_tise,
    }
    return render(request, 'home/meettheteam.html', context)

def home(request):
    tutors = Tutor.objects.all()
    home_content = HomeContent.objects.all()
    reviews = Review.objects.all()
    context = {'tutors': tutors, 'home_content': home_content, 'reviews': reviews}
    return render(request, 'home/home.html', context)
