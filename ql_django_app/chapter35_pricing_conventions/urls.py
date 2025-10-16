from django.urls import path
from .views import convention_glitch_lab_view, pricing_conventions_description_view

app_name = 'pricing_conventions'

urlpatterns = [
    path('', pricing_conventions_description_view, name='description'),
    path('lab/', convention_glitch_lab_view, name='lab'),
]
