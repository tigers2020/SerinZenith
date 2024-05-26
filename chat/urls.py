from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chat import views
from chat.views import ChatView, SendMessageView, GetAIResponseView

urlpatterns = [
    path('', ChatView.as_view(), name='chat'),
    path('send_message/', SendMessageView.as_view(), name='send_message'),
    path('get_ai_response/', GetAIResponseView.as_view(), name='get_ai_response'),
]
