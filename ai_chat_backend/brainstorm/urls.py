from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_brainstorm, name='submit_brainstorm'),
    path('story/<int:pk>/', views.get_story, name='get_story'),
] 