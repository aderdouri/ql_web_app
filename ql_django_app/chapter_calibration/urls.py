# Fichier : ql_web_app/chapter_calibration/urls.py
from django.urls import path
from . import views

# L'app_name est crucial pour le lien à 3 niveaux
app_name = 'chapter_calibration'

urlpatterns = [
    # Le 'name' doit être EXACTEMENT 'calibration_lab'
    path('', views.calibration_lab_view, name='calibration_lab'),
]