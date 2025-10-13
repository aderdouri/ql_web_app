from django.urls import path
from . import views

app_name = 'chapter22_heston_calibration'
urlpatterns = [
    path('', views.calibration_description_view, name='calibration_description'),
    path('lab/', views.calibration_lab_view, name='calibration_lab'),
]