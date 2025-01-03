from django.db import models

class contactMessage(models.Model):
    level = [
        ('gcse', 'GCSE'),
        ('alevel', 'A Level')
    ]

    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    subject = models.CharField(max_length=100)
    level = models.CharField(choices=level )
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

class HomePageContent(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    position = models.PositiveIntegerField()

    class Meta:
        ordering = ['position']
