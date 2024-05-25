from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView


# Create your views here.

class HomeView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variable'] = 'Hello, World!'
        return context


class SerinLiveView(LoginRequiredMixin, TemplateView):
    template_name = 'main/serin_live.html'
    login_url = 'login'
    redirect_field_name = 'redirect_to'


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'main/settings.html'
    login_url = 'login'
    redirect_field_name = 'redirect_to'


class AboutView(TemplateView):
    template_name = 'main/about.html'


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)