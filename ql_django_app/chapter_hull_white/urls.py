from django.urls import path
from . import views

app_name = 'chapter_hull_white'

urlpatterns = [
    path('calibration/', views.short_rate_calibration_view, name='short_rate_calibration'),
    path('simulation/', views.hull_white_simulation_view, name='hull_white_simulation'),
]