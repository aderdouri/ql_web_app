from django.urls import path
from . import views

app_name = 'chapter_day_count_conventions'

urlpatterns = [
    path('', views.day_count_lab, name='day_count_lab'),
]











