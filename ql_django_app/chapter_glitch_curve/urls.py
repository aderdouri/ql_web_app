# Fichier : ql_web_app/chapter_glitch_curve/urls.py

from django.urls import path
from . import views

# CETTE LIGNE EST OBLIGATOIRE
app_name = 'chapter_glitch_curve'

urlpatterns = [
    # Le chemin est vide, et le nom est 'glitch_lab'
    path('', views.glitch_lab_view, name='glitch_lab'),
]