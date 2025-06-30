from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('meettheteam/', views.meettheteam, name='meettheteam'),
    path('contact/', views.contact, name='contact'),
    path('tutor/<int:pk>/', views.tutor_detail, name='tutor_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)