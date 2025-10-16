from django.urls import path
from .views import callable_bond_lab_view, callable_bonds_description_view

app_name = 'chapter31_callable_bonds'

urlpatterns = [
    path('', callable_bonds_description_view, name='description'),
    path('lab/', callable_bond_lab_view, name='lab'),
]