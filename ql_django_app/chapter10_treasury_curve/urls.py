
from django.urls import path
from . import views

app_name = 'chapter10_treasury_curve'
urlpatterns = [
    path('', views.curve_lab_view, name='curve_lab'),
]