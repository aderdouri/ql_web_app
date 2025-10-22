from django.urls import path
from . import views

app_name = 'chapter22_heston_calibration'
urlpatterns = [
    path('', views.heston_calibration_description_view, name='description'),
    path('lab/', views.volatility_smile_lab_view, name='volatility_smile_lab'),
]