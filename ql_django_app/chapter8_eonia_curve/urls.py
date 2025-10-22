from django.urls import path
from . import views
app_name = 'chapter8_eonia_curve'
urlpatterns = [
path('', views.eonia_lab_view, name='eonia_lab'),
]