from django.urls import path
from . import views

app_name = 'chapter3_greeks'
urlpatterns = [
    path('', views.greeks_lab_view, name='greeks_lab'),
]