from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from todolist.core.views import SignUpView, LoginView, ProfileView, UpdatePasswordView

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('update_password', UpdatePasswordView.as_view(), name='update_password')
]