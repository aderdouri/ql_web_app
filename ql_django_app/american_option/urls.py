# filepath: /Users/aderdouri/Downloads/ql_web_app/ql_django_app/american_option/urls.py
from django.urls import path
from . import views

app_name = 'american_option'

urlpatterns = [
    path('price/', views.price_american_option, name='price_american_option'),
]