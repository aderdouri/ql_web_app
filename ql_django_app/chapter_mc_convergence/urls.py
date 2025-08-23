from django.urls import path
from . import views

app_name = 'chapter_mc_convergence'
urlpatterns = [
    path('', views.convergence_lab_view, name='convergence_lab'),
]