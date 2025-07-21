# File: ql_web_app/european_option/urls.py (FINAL AND COMPLETE CODE)

from django.urls import path
from . import views

# Namespace for the application, used in templates for URL reversing
app_name = 'european_option'

urlpatterns = [
    # The empty path '' means this is the root URL for this app
    # The final URL will be determined by the main project's urls.py
    path('', views.price_european_option, name='pricer'),
]