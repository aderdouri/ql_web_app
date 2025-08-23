from django.urls import path
from . import views

app_name = 'chapter_implied_curve'

urlpatterns = [
    path('', views.implied_curve_lab_view, name='implied_curve_lab'),
]