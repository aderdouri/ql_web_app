from django.urls import path
from . import views

app_name = 'swaption'

urlpatterns = [

    path('', views.pricer_view, name='pricer'),
]