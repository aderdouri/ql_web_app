from django.urls import path
from . import views

app_name = 'chapter26_defining_rho'

urlpatterns = [
    path('', views.defining_rho_description_view, name='description'),
    path('lab/', views.defining_rho_lab_view, name='lab'),
]