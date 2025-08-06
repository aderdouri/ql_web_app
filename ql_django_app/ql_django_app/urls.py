from django.contrib import admin
from django.urls import path, include
from . import views as home_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.home, name='home'),

    # On ne garde QUE les catégories qui existent et sont configurées
    path('basics/', include('basics.urls')),
    path('interest-rate-curves/', include('interest_rate_curves.urls')),
    path('interest-rate-models/', include('interest_rate_models.urls')),
]