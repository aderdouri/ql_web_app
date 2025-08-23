from django.urls import path
from . import views

app_name = 'american_option'

urlpatterns = [
    
    path('', views.pricer_view, name='pricer'), 
]