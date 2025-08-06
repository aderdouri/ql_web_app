from django.urls import path, include
from . import views

app_name = 'interest_rate_models'
urlpatterns = [
    path('', views.home, name='home'),
    # On connecte le chapitre "Swap" ici
    path('vanilla-swap/', include('swap.urls')),
]