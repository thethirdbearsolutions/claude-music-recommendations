
from rest_framework import serializers
from .models import Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'initial_message', 'created_at', 'updated_at']


# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MusicRecommendationViewSet

router = DefaultRouter()
router.register(r'music', MusicRecommendationViewSet, basename='music')

urlpatterns = [
    path('api/', include(router.urls)),
]