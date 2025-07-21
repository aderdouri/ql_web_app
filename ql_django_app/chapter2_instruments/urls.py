# File: ql_web_app/chapter2_instruments/urls.py

from django.urls import path
from . import views

# Define the namespace for this specific application.
# This is crucial for creating links in templates with the {% url %} tag.
# It allows us to refer to this URL as 'chapter2_instruments:pricer_lab'.
app_name = 'chapter2_instruments'

urlpatterns = [
    # The path is an empty string ('') because the prefix ('instruments-engines/')
    # is already handled by the category's urls.py file (basics/urls.py).
    # This pattern will match the final part of the URL.
    path('', views.pricer_lab_view, name='pricer_lab'),
]