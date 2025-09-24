from django.urls import path
from . import views

app_name = 'chapter4_quotes'

urlpatterns = [
    path('', views.bond_curve_lab_view, name='bond_curve_lab'),
    path('update-quotes/', views.update_quotes_ajax, name='update_quotes'),
    path('freeze-unfreeze/', views.freeze_unfreeze_ajax, name='freeze_unfreeze'),
]