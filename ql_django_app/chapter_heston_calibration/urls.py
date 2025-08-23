from django.urls import path
from . import views

app_name = 'chapter_heston_calibration'
urlpatterns = [
    path('', views.calibration_lab_view, name='calibration_lab'),
]