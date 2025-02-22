from django.contrib import admin
from .models import Tutor, Expertise, ContactMessage, HomeContent, Review

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('name', 'expertise_list', 'created')
    filter_horizontal = ('expertise',)  # This widget makes selecting multiple expertise items easier

admin.site.register(Expertise)
admin.site.register(ContactMessage)
admin.site.register(HomeContent)
admin.site.register(Review)
