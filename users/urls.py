"""Defines URL patterns for users"""

from django.contrib.auth.views import LoginView
from django.urls import re_path

from . import views

app_name = 'users'

urlpatterns = [
    # Login page LoginView.as_view(template_name='users/login.html')
    #     re_path(r'^login/$', login, views.categories, name='categories'),
    re_path('^login/$', LoginView.as_view(template_name='users/login.html'), name='login'),

    # Logout page
    re_path('^logout/$', views.logout_view, name='logout'),

    # Registration page
    re_path('^register/$', views.register, name='register'),
]