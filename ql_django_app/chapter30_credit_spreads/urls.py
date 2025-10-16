from django.urls import path
from . import views

app_name = 'chapter30_credit_spreads'

urlpatterns = [
    path('description/', views.description, name='description'),
    path('lab/', views.credit_spread_lab_view, name='lab'),
]
