# File: ql_web_app/chapter_2_lab/urls.py
from django.urls import path
from . import views

app_name = 'chapter_2_lab'

urlpatterns = [
    path('', views.lab_view, name='lab'),
]