
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/music/recommendations/', views.get_recommendation, name='get_recommendation'),
    path('api/music/messages/', views.continue_conversation, name='continue_conversation'),
]
