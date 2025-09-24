from django.urls import path
from . import views

app_name = 'chapter5_curves'

urlpatterns = [
    path('', views.curve_lab_view, name='curve_lab'),
    path('api/calculate/', views.calculate_term_structures_api, name='calculate_api'),
]