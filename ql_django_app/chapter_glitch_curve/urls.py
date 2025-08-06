from django.urls import path
from . import views


urlpatterns = [
    path('', views.glitch_lab_view, name='glitch_lab'),
]