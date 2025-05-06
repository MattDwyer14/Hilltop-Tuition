from django.db import models
from django.utils import timezone

class ContactMessage(models.Model):
    LEVEL_CHOICES = [
        ('gcse', 'GCSE'),
        ('alevel', 'A Level')
    ]

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    message = models.TextField(max_length=400)
    subject = models.CharField(max_length=100)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


class HomeContent(models.Model):
    title = models.CharField(max_length=100)
    paragraph = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.title


class Expertise(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Expertise Area")

    def __str__(self):
        return self.name


class Tutor(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tutor Name")
    about = models.TextField(max_length=2000, blank=True)
    summary = models.CharField(
        max_length=500,  # Adjust max_length as needed
        verbose_name="Short Summary",
        blank=True,
        help_text="Enter a short summary (max 500 characters)."
    )
    created = models.DateTimeField(default=timezone.now, verbose_name="Date Joined")
    image = models.ImageField(
        upload_to='tutors/', 
        blank=True, 
        null=True, 
        verbose_name="Profile Image"
    )
    expertise = models.ManyToManyField(
        Expertise, 
        related_name='tutors', 
        blank=True,
        verbose_name="Areas of Expertise"
    )
    qualifications = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Qualifications",
        help_text="List the tutor’s qualifications (comma-separated or free text)."
    )
    
    def expertise_list(self):
        """Returns a comma-separated list of expertise names."""
        return ", ".join(e.name for e in self.expertise.all())

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
