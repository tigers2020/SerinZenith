import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import escape
from django.views import View
from django.views.generic import TemplateView

from SerinZenith import settings
from serin_zenith_settings.models import TextGeneration
from serin_zenith_settings.typing import ChatCompletionRequest, ChatCompletionResponse
from .models import ChatMessage, ChatGroup


# Create your views here.

class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_time = timezone.now()
        group_name = current_time.strftime('%Y-%m-%d %I:00 %p')
        chat_group, created = ChatGroup.objects.get_or_create(name=group_name)
        chat_groups = ChatGroup.objects.all().order_by('-name')
        chat_message = ChatMessage.objects.filter(group=chat_group).order_by('created_at')

        context['chat_groups'] = chat_groups
        context['chat_messages'] = chat_message

        return context


class LoadMessagesView(LoginRequiredMixin, View):
    def get(self, request, group_id):
        chat_group = ChatGroup.objects.get(id=group_id)
        chat_messages = ChatMessage.objects.filter(group=chat_group).order_by('created_at')
        messages_html = render_to_string('chat/messages.html', {'chat_messages': chat_messages})
        return JsonResponse({'messages_html': messages_html})


class SendMessageView(View):
    def post(self, request, *args, **kwargs):
        message_content = request.POST.get('message')
        chat_group_id = request.POST.get('group_id')

        chat_group = get_object_or_404(ChatGroup, id=chat_group_id)
        chat_message = ChatMessage.objects.create(user=request.user, group=chat_group, sender='user',
                                                  message=message_content)

        message = {
            'sender': request.user,
            'message': message_content
        }
        message_html = render_to_string('chat/user_message.html', {'message': message}, request=request)

        return JsonResponse({
            'user_message_html': message_html,
            'message_id': chat_message.id
        })


class GetAIResponseView(View):
    def __init__(self):
        super().__init__()
        self.response = None

    def post(self, request, *args, **kwargs):
        user = request.user
        message_id = request.POST.get('message_id')
        if not message_id:
            message_id = ChatMessage.objects.last().id

        messages = self.get_recent_messages()
        message_history = self.prepare_message_history(messages)
        # Fetch the appropriate TextGeneration settings
        preset = request.POST.get('preset', 'Yara')
        try:
            text_generation_settings = TextGeneration.objects.get(preset=preset)
        except TextGeneration.DoesNotExist:
            return JsonResponse({"error": f"Preset {preset} does not exist."}, status=400)
        # Prepare completion request using Pydantic schema
        completion_request = self.prepare_completion_request(text_generation_settings, message_history)
        serin_reply = self.get_ai_response(completion_request)

        chat_message = get_object_or_404(ChatMessage, id=message_id)
        chat_group = chat_message.group
        ChatMessage.objects.create(user=user, group=chat_group, sender='assistant', message=serin_reply)

        # Create the message dictionary with the required structure
        message = {
            'sender': 'Serin',
            'message': serin_reply
        }

        serin_reply_html = render(request, 'chat/serin_reply.html', {'message': message}).content.decode('utf-8')
        return JsonResponse({
            'serin_reply_html': serin_reply_html,
            'message_id': message_id
        })

    @staticmethod
    def get_recent_messages():
        return ChatMessage.objects.order_by('-created_at')[:20][::-1]

    @staticmethod
    def prepare_message_history(messages):
        return [{"role": message.sender, "content": escape(message.message)} for message in messages]

    @staticmethod
    def get_error_message_based_on_status_code(status_code, http_err):
        error_messages = {
            400: "It looks like there was a problem with the request. Please check the data and try again.",
            401: "Authorization failed. Please check your API key and permissions.",
            403: "Access forbidden. You don't have permission to access this resource.",
            404: "The requested resource was not found. Please check the URL and try again.",
            500: "There was an internal server error. Please try again later.",
            502: "Bad gateway. The server is currently unreachable. Please try again later.",
            503: "Service unavailable. The server is temporarily unable to handle the request. Please try again later.",
            504: "Gateway timeout. The server is taking too long to respond. Please try again later."
        }
        return error_messages.get(status_code, f"An HTTP error occurred: {http_err}. Please try again later.")

    def prepare_completion_request(self, text_generation_settings, message_history):
        # Map the TextGeneration settings to the ChatCompletionRequest schema
        completion_request = ChatCompletionRequest(
            messages=message_history,
            mode="chat",
            character="serin",
            top_a=text_generation_settings.sampling_parameters.top_a,
            temperature=text_generation_settings.generation_settings.temperature,
            max_tokens=text_generation_settings.generation_settings.max_new_tokens,
            max_tokens_second=text_generation_settings.generation_settings.max_tokens_second,
            skip_special_tokens=text_generation_settings.generation_settings.skip_special_tokens,
            repetition_penalty=text_generation_settings.penalties_and_filters.repetition_penalty,
            repetition_penalty_range=text_generation_settings.penalties_and_filters.repetition_penalty_range,
            penalty_alpha=text_generation_settings.penalties_and_filters.penalty_alpha,
            encoder_repetition_penalty=text_generation_settings.penalties_and_filters.encoder_repetition_penalty,
            no_repeat_ngram_size=text_generation_settings.penalties_and_filters.no_repeat_ngram_size,
            dynatemp_low=text_generation_settings.dynamic_adjustments.dynatemp_low,
            dynatemp_high=text_generation_settings.dynamic_adjustments.dynatemp_high,
            dynatemp_exponent=text_generation_settings.dynamic_adjustments.dynatemp_exponent,
            mirostat_mode=text_generation_settings.dynamic_adjustments.mirostat_mode,
            mirostat_tau=text_generation_settings.dynamic_adjustments.mirostat_tau,
            mirostat_eta=text_generation_settings.dynamic_adjustments.mirostat_eta,
            guidance_scale=text_generation_settings.advanced_settings.guidance_scale,
            negative_prompt=text_generation_settings.advanced_settings.negative_prompt,
            epsilon_cutoff=text_generation_settings.advanced_settings.epsilon_cutoff,
            eta_cutoff=text_generation_settings.advanced_settings.eta_cutoff,
            truncation_length=text_generation_settings.contextual_settings.truncation_length,
            prompt_lookup_num_tokens=text_generation_settings.contextual_settings.prompt_lookup_num_tokens,
            add_bos_token=text_generation_settings.contextual_settings.add_bos_token,
            ban_eos_token=text_generation_settings.contextual_settings.ban_eos_token,
            grammar_string=text_generation_settings.contextual_settings.grammar_string
        )
        return completion_request

    def get_ai_response(self, completion_request):
        api_url = settings.OPENAI_API_URL + "v1/chat/completions"
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        data = completion_request.json()

        try:
            self.response = requests.post(api_url, headers=headers, data=data, timeout=10)
            self.response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            response_data = self.response.json()
            ai_response = ChatCompletionResponse(**response_data)
            return ai_response.choices[0]['message']['content']
        except requests.exceptions.HTTPError as http_err:
            return GetAIResponseView.get_error_message_based_on_status_code(self.response.status_code, http_err)
        except requests.exceptions.ConnectionError:
            return "There was a network connection error. Please check your internet connection and try again."
        except requests.exceptions.Timeout:
            return "The request timed out. Please try again later."
        except requests.exceptions.RequestException as err:
            return f"An unexpected error occurred: {err}. Please try again later."
        except Exception as e:
            return f"An error occurred: {str(e)}. Please try again later."
