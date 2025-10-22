from django.urls import path
from . import views

app_name = 'chapter13_sensitivities'
urlpatterns = [
    path('', views.sensitivity_lab_view, name='sensitivity_lab'),
]