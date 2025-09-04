# interactive_basics/urls.py

from django.urls import path
from . import views

app_name = 'interactive_basics'

urlpatterns = [
    # CORRECTION : Utilisez un chemin vide ici.
    # Le préfixe 'quantlib-basics/' est déjà géré par un autre fichier urls.py
    path('', views.basics_lab_view, name='quantlib_basics_lab'),
]