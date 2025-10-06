# urls.py

from django.urls import path
from .views import option_valuation_description_view, option_valuation_lab_view

app_name = 'chapter_european_american_options'

urlpatterns = [
    path('', option_valuation_description_view, name='description'),
    path('lab/', option_valuation_lab_view, name='lab'),
]