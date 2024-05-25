from django.contrib.auth.views import LogoutView
from django.urls import path

from main import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('serin-live/', views.SerinLiveView.as_view(), name='serin_live'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]

handler404 = 'main.views.custom_404'
