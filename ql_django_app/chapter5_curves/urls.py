# Fichier : ql_web_app/chapter5_curves/urls.py
from django.urls import path
from . import views

app_name = 'chapter5_curves'

urlpatterns = [
    path('', views.curve_lab_view, name='curve_lab'),
]