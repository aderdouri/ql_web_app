# Fichier : ql_web_app/ql_django_app/ql_django_app/urls.py (VERSION CORRIGÉE ET MINIMALISTE)

from django.contrib import admin
from django.urls import path, include
# Assurez-vous que ce fichier views.py existe bien dans le même dossier
from . import views as home_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.home, name='home'),

    # ==============================================================================
    # LA CORRECTION EST ICI : On ajoute l'argument "namespace"
    # ==============================================================================
    # Ceci "enregistre" officiellement 'basics' comme un espace de noms.
    path('basics/', include('basics.urls', namespace='basics')),
    
    # Et on fait de même pour 'interest_rate_curves'.
    path('interest-rate-curves/', include('interest_rate_curves.urls', namespace='interest_rate_curves')),
]