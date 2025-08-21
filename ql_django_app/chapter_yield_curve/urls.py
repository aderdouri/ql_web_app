# Fichier : chapter_yield_curve/urls.py
from django.urls import path
from . import views

# On met à jour l'app_name
app_name = 'chapter_yield_curve'

urlpatterns = [
    path('', views.curve_lab_view, name='curve_lab'),
]