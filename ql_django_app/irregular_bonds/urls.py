from django.urls import path
from . import views

urlpatterns = [
    path('', views.irregular_lab, name='irregular_lab'),
    path('calculate/', views.calculate_bond, name='calculate_bond'),
]
