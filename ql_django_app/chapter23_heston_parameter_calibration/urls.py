from django.urls import path
from . import views

app_name = 'heston_calibration_scipy'

urlpatterns = [
    path('', views.heston_parameter_calibration_description_view, name='description'),
    path('lab/', views.heston_calibration_lab_view, name='lab'),
    path('test/', views.test_solver_view, name='test'),
]


