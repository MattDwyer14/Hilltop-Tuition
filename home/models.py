from django.db import models

class HomePageContent(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    position = models.PositiveIntegerField()

    class Meta:
        ordering = ['position']
