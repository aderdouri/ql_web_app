from django.urls import path
from . import views

app_name = 'chapter_heston_parameter_calibration'

urlpatterns = [
    path('', views.parameter_calibration_lab, name='parameter_calibration_lab'),
]


