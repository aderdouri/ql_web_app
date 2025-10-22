from django.urls import path
from . import views

app_name = 'chapter9_euribor_curve'
urlpatterns = [
    path('', views.euribor_lab_view, name='euribor_lab'),
]