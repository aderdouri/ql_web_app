from django.urls import path
from . import views

app_name = 'chapter27_day_count_conventions'

urlpatterns = [
    path('', views.day_count_conventions_description_view, name='description'),
    path('chapter/', views.day_count_conventions_chapter_view, name='chapter'),
]