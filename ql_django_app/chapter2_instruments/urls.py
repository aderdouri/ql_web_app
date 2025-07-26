from django.urls import path
from . import views

app_name = 'chapter2_instruments'

urlpatterns = [
    path('', views.pricer_lab_view, name='pricer_lab'),
]