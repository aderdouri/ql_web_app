from django.urls import path
from .views import frn_duration_lab_view, floating_duration_description_view

app_name = 'chapter33_floating_duration'

urlpatterns = [
    path('', floating_duration_description_view, name='description'),
    path('lab/', frn_duration_lab_view, name='lab'),
]
