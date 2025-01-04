from django.db import models

class contactMessage(models.Model):
    level = [
        ('gcse', 'GCSE'),
        ('alevel', 'A Level')
    ]

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    message = models.TextField(max_length=400)
    subject = models.CharField(max_length=100)
    level = models.CharField(choices=level, max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})",

class Tutor(models.Model):
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=100)
    expertise = models.CharField(max_length=50)
    review = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='tutors_photos/')

    def __str__(self):
        return f"{self.name} - {self.expertise}"
    
class HomeContent(models.Model):
    title = models.CharField(max_length=100)
    paragraph = models.CharField(max_length=1000, blank=True)


