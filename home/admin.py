from django.contrib import admin
from .models import Tutor, contactMessage, HomeContent, Review

admin.site.register(Tutor)
admin.site.register(contactMessage)
admin.site.register(HomeContent)
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'created_at')
    search_fields = ('text',)
