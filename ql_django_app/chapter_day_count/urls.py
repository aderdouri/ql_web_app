from django.urls import path
from . import views
app_name = 'chapter_day_count'
urlpatterns = [
path('', views.day_count_lab_view, name='day_count_lab'),
]