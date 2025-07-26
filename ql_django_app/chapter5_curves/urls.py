from django.urls import path
from . import views

app_name = 'chapter5_curves'

urlpatterns = [
    path('', views.curve_lab_view, name='curve_lab'),
]