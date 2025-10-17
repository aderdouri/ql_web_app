from django.urls import path
from .views import hull_white_lab_view, hull_white_description_view

app_name = 'chapter15_hull_white'

urlpatterns = [
    path('', hull_white_description_view, name='description'),
    path('lab/', hull_white_lab_view, name='lab'),
    path('simulation/', hull_white_lab_view, name='simulation'),  # Compatibilité avec l'ancienne URL
]