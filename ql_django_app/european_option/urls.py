from django.urls import path
from . import views

app_name = 'european_option'

urlpatterns = [
    path('price/', views.price_european_option, name='price_european_option'),
]