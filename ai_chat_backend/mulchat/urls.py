from django.urls import path
from . import views

urlpatterns = [
    path('', views.multi_chat, name='multi_chat'),
] 