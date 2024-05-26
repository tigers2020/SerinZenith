from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView


# Create your views here.

class HomeView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variable'] = 'Hello, World!'
        return context


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'main/settings.html'
    login_url = 'login'
    redirect_field_name = 'redirect_to'


class AboutView(TemplateView):
    template_name = 'main/about.html'


class CustomRegisterView(CreateView):
    template_name = 'registration/register.html'


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


class FAQView(TemplateView):
    template_name = 'main/FAQ.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faq'] = 'Frequently Asked Questions'
        return context


class ContactView(TemplateView):
    template_name = 'main/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PrivacyView(TemplateView):
    template_name = 'main/privacy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TermsView(TemplateView):
    template_name = 'main/Term.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
