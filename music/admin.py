
from django.contrib import admin
from .models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'initial_message', 'created_at', 'updated_at')
    search_fields = ('initial_message',)
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('content',)
    readonly_fields = ('id', 'created_at')
