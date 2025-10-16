# urls.py

from django.urls import path
from .views import treasury_futures_lab_view, treasury_futures_description_view

app_name = 'treasury_futures'

urlpatterns = [
    path('', treasury_futures_description_view, name='description'),
    path('lab/', treasury_futures_lab_view, name='lab'),
]