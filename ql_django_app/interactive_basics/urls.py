from django.urls import path
from . import views

app_name = 'interactive_basics'

urlpatterns = [
    path('', views.interactive_lab_view, name='lab'),
]