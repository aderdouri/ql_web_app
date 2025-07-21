from django.urls import path, include
from . import views

app_name = 'interest_rate_curves'
urlpatterns = [
    path('', views.home, name='home'),
    path('term-structures-lab/', include('chapter5_curves.urls', namespace='term_structures_lab')),
]