from django.urls import path
from . import views

app_name = 'chapter_caps_floors' 
urlpatterns = [
    path('', views.parity_lab_view, name='parity_lab'), 
]