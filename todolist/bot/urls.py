from django.urls import path

from todolist.bot import views

urlpatterns = [
    path('verify', views.VerifcationView.as_view(), name='verify-bot'),
]