from django.urls import path
from . import views

app_name = 'chapter7_random'
urlpatterns = [
    path('', views.random_lab_view, name='random_lab'),
]