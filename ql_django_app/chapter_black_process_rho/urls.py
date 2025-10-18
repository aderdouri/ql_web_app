from django.urls import path
from . import views

app_name = 'chapter_black_process_rho'

urlpatterns = [
    path('', views.black_process_rho_lab, name='black_process_rho_lab'),
]


















