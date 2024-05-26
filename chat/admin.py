from mailbox import Message

from django.contrib import admin

from chat.models import ChatGroup, ChatMessage

# Register your models here.

admin.site.register(ChatGroup)
admin.site.register(ChatMessage)
