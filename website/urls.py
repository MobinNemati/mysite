
from django.contrib import admin
from django.urls import path, re_path
from website.views import *
from django.contrib.auth import views as auth_views

app_name = 'website'

urlpatterns = [
    path('', index_view, name='index'),
    path('about', about_view, name='about'),
    path('contact', contact_view, name='contact'),
    path('newsletter', newsletter_view, name='newsletter'),
]

