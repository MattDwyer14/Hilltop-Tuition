from django.shortcuts import render, redirect
from .models import Tutor, HomeContent, Review, Expertise
from django.contrib import messages
from .forms import ContactMessageForm
import os
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages


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

def contact(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            subject = f"Web Message from {contact_message.name}"
            message = f"""
Email: {contact_message.email}
Subject: {contact_message.subject}
Level: {contact_message.level}
Message: {contact_message.message}

{contact_message.name}
            """
            from_email = os.getenv('EMAIL_HOST_USER')
            recipient = os.getenv('EMAIL_RECIPIENT') 

            send_mail(subject, message, from_email, [recipient])

            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
        else:
            messages.error(request, "There was an error with your submission. Please check the form and try again.")
    else:
        form = ContactMessageForm()
    print("EMAIL_HOST_USER:", os.getenv('EMAIL_HOST_USER'))
    print("EMAIL_RECIPIENT:", os.getenv('EMAIL_RECIPIENT'))

    return render(request, 'home/contact.html', {'form': form})