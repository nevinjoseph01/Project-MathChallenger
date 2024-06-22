from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView,LogoutView
from . import views
from mathchallenger import settings
from django.shortcuts import redirect, render

urlpatterns = [
    path('', views.home, name= 'landing-page'),
    path('register/', views.register, name= 'register-page'),
    path('login/', LoginView.as_view(template_name="quiz/login.html"), name="login-page"),
    path('logout/', LogoutView.as_view(next_page = settings.LOGOUT_REDIRECT_URL), name="logout-page"),
    path('skills/', views.skills, name = 'skills-page'),
    path('add_question/', views.add_question, name='add-question'),
    path('play_quiz/', views.play_quiz, name='play-quiz'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('teachersite/',views.teachersite, name='teachersite'),
    path('participants/',views.participants, name='participants')
]

