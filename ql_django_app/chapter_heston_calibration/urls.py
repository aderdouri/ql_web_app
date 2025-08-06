from django.urls import path
from . import views

app_name = 'chapter_heston_calibration'
urlpatterns = [
    path('', views.heston_calibration_lab_view, name='heston_calibration_lab'),
]