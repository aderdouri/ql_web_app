from django.urls import path
from . import views

app_name = 'chapter11_glitch_curve'

urlpatterns = [
    path('', views.glitch_lab_view, name='glitch_lab'),
]