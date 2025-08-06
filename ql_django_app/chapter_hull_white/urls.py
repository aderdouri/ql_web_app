from django.urls import path
from . import views

app_name = 'chapter_hull_white' # <-- Vérifier cet app_name
urlpatterns = [
    path('', views.hull_white_lab_view, name='hull_white_lab'), # <-- Vérifier ce name
]