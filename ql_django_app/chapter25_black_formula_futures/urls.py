# urls.py

from django.urls import path
from .views import black_formula_futures_description_view, black_formula_lab_view

app_name = 'chapter25_black_formula_futures'

urlpatterns = [
    path('', black_formula_futures_description_view, name='description'),
    path('lab/', black_formula_lab_view, name='lab'),
]