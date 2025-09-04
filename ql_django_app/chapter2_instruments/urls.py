# chapter2_instruments/urls.py (VERSION FINALE)

from django.urls import path
from .views import pricer_lab_view

# Le nom de cet espace de noms est 'chapter2_instruments'
app_name = 'chapter2_instruments'

urlpatterns = [
    # URL /basics/chapter2/pricer-lab/ -> Appelle la vue pricer_lab_view
    path('pricer-lab/', pricer_lab_view, name='pricer_lab'),
]