import json

import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import escape
from django.views import View
from django.views.generic import TemplateView

from SerinZenith import settings
from .models import ChatGroup, ChatMessage


# Create your views here.

class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_time = timezone.now()
        group_name = current_time.strftime('%Y-%m-%d %I:00 %p')
        chat_group, created = ChatGroup.objects.get_or_create(name=group_name)
        print(chat_group.id)
        chat_groups = ChatGroup.objects.all().order_by('-name')
        chat_message = ChatMessage.objects.filter(group=chat_group).order_by('created_at')

        print(chat_message)
        context['chat_groups'] = chat_groups
        context['chat_messages'] = chat_message

        return context


class SendMessageView(View):
    def post(self, request, *args, **kwargs):
        message_content = request.POST.get('message')
        chat_group_id = request.POST.get('group_id')

        chat_group = get_object_or_404(ChatGroup, id=chat_group_id)
        chat_message = ChatMessage.objects.create(user=request.user, group=chat_group, sender='user',
                                                  message=message_content)
        message = {
            'user': request.user,
            'message': message_content
        }
        message_html = render_to_string('chat/user_message.html', {'message': message}, request=request)

        return JsonResponse({
            'user_message_html': message_html,
            'message_id': chat_message.id
        })


class GetAIResponseView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        message_id = request.POST.get('message_id')
        if not message_id:
            message_id = ChatMessage.objects.last().id

        messages = ChatMessage.objects.order_by('-created_at')[:20][::-1]

        # Prepare the message history for the OpenAI API
        message_history = [{"role": message.sender, "content": escape(message.message)} for message in messages]
        api_url = settings.OPENAI_API_URL + "v1/chat/completions"
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        data = {
            "mode": "chat",
            "character": "serin",
            "messages": message_history,
        }

        try:
            response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
            response_data = response.json()
            serin_reply = response_data['choices'][0]['message']['content']
        except Exception as e:
            serin_reply = f"Error: {str(e)}"
        chat_message = get_object_or_404(ChatMessage, id=message_id)
        chat_group = ChatMessage.objects.get(id=message_id).group
        ChatMessage.objects.create(user=user, group=chat_group, sender='assistant', message=serin_reply)

        # Create the message dictionary with the required structure
        message = {
            'user': 'Serin',
            'message': serin_reply
        }

        serin_reply_html = render(request, 'chat/serin_reply.html', {'message': message}).content.decode('utf-8')
        print(serin_reply_html)
        return JsonResponse({
            'serin_reply_html': serin_reply_html,
            'message_id': message_id
        })
