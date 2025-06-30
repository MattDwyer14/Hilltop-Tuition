from django.shortcuts import render, redirect
from .models import Tutor, HomeContent, Review, Expertise
from .forms import ContactMessageForm
from django.contrib import messages
from django.core.mail import send_mail
import os
from django.shortcuts import get_object_or_404, render
from datetime import datetime


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

        # Honeypot field (named 'website' in form) to trap bots
        if request.POST.get('website'):
            messages.error(request, "Bot detected. Submission blocked.")
            return redirect('contact')

        # Timestamp validation to catch very fast submissions
        timestamp_str = request.POST.get('timestamp')
        if timestamp_str:
            try:
                form_time = datetime.fromisoformat(timestamp_str)
                if (datetime.now() - form_time).total_seconds() < 3:
                    messages.error(request, "Submission too fast. Bot suspected.")
                    return redirect('contact')
            except ValueError:
                pass

        # Keyword filtering (e.g., 'phoff', 'vag') in name or message
        banned_keywords = ['phoff', 'vag']
        name = request.POST.get('name', '').lower()
        message_content = request.POST.get('message', '').lower()
        if any(keyword in name or keyword in message_content for keyword in banned_keywords):
            messages.error(request, "Spam detected in content.")
            return redirect('contact')

        if form.is_valid():
            contact_message = form.save()

            # Construct and send email, including the form timestamp
            subject = f"Web Message from {contact_message.name}"
            message = f"""
Email: {contact_message.email}
Subject: {contact_message.subject}
Level: {contact_message.level}
Message: {contact_message.message}

Submitted at: {timestamp_str}

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

    # Prepare a timestamp for the form (ISO format)
    timestamp = datetime.now().isoformat()
    return render(request, 'home/contact.html', {'form': form, 'timestamp': timestamp})

def tutor_detail(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)
    reviews = tutor.reviews.order_by('-created_at')
    return render(request, 'home/tutor_detail.html', {
        'tutor': tutor,
        'reviews': reviews,
    })