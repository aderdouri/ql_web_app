from django.urls import path
from . import views

app_name = 'chapter29_irregular_bonds'

urlpatterns = [
    path('description/', views.description, name='description'),
    path('lab/', views.irregular_lab_view, name='lab'),
]