"""Defines URL patterns for info_hubs."""

from django.urls import re_path

from . import views

app_name = 'info_hubs'

urlpatterns = [
    # Home page
    re_path('^$', views.index, name='index'),

    # Show all categories
    re_path('^categories/$', views.categories, name='categories'),

    # Detail page for a single topic
    # Show articles for each topic
    re_path('^categories/(?P<category_id>\d+)/$', views.category, name='category'),
]