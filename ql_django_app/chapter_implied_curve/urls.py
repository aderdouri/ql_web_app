from django.urls import path
from . import views

# This is mandatory for namespacing
app_name = 'chapter_implied_curve'

urlpatterns = [
    path('', views.implied_curve_lab_view, name='implied_curve_lab'),
]