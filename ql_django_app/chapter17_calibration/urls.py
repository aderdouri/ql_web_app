from django.urls import path
from . import views

app_name = 'chapter17_calibration'

urlpatterns = [
    path('', views.calibration_description_view, name='description'),
    path('lab/', views.calibration_lab_view, name='calibration_lab'),
]