from django.urls import path
from .views import convergence_lab_view, convergence_description_view

app_name = 'chapter16_mc_convergence'

urlpatterns = [
    path('', convergence_description_view, name='description'),
    path('lab/', convergence_lab_view, name='convergence_lab'),
]