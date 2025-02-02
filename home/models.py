from django.db import models
from django.utils import timezone

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
    about = models.CharField(max_length=200)
    expertise = models.CharField(max_length=50)
    review = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='tutors_photos/')

    def __str__(self):
        return f"{self.name} - {self.expertise}"
    
class HomeContent(models.Model):
    title = models.CharField(max_length=100)
    paragraph = models.CharField(max_length=1000, blank=True)

class Review(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
class Expertise(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Expertise Area")

    def __str__(self):
        return self.name

class Tutor(models.Model):
    title = models.CharField(max_length=100, verbose_name="Tutor Name")
    created = models.DateTimeField(default=timezone.now, verbose_name="Date Joined")
    image = models.ImageField(
        upload_to='tutors/', 
        blank=True, 
        null=True, 
        verbose_name="Profile Image"
    )
    description = models.TextField(verbose_name="Tutor Biography", blank=True)
    # A tutor may have more than one area of expertise.
    expertise = models.ManyToManyField(
        Expertise, 
        related_name='tutors', 
        blank=True,
        verbose_name="Areas of Expertise"
    )

    def expertise_list(self):
        """Returns a comma-separated list of expertise names."""
        return ", ".join(e.name for e in self.expertise.all())

    def __str__(self):
        return self.title