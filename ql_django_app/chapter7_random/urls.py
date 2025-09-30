from django.urls import path
from . import views

app_name = 'chapter7_random'

urlpatterns = [
    path('', views.random_numbers_view, name='random_lab'),
    path('api/calculate/', views.calculate_random_numbers_api, name='calculate_api'),
]

