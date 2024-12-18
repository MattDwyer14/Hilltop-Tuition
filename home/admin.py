from django.contrib import admin
from .models import HomePageContent

@admin.register(HomePageContent)
class HomePageContent(admin.ModelAdmin):
    list_display = ('title', 'position')
    list_editable = ('position',)
