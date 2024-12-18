from django.shortcuts import render
from .models import HomePageContent

def home(request):
    text_entries = list(HomePageContent.objects.all())
    
    image_paths = [f'home/media/image ({n}).jpg' for n in range(1, len(text_entries) + 1)]
    combined_content = []
    for text, image in zip(text_entries, image_paths):
        combined_content.append({'type': 'text', 'content': text})
        combined_content.append({'type': 'image', 'content': image})

    return render(request, 'home/home.html', {'combined_content': combined_content})
