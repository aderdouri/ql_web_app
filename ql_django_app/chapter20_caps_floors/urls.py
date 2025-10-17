from django.urls import path
from . import views

app_name = 'chapter20_caps_floors'

urlpatterns = [
    path('', views.caps_floors_description_view, name='description'),
    path('lab/', views.caps_floors_lab_view, name='lab'),
]