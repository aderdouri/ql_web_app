# File: ql_web_app/interactive_basics/urls.py
from django.urls import path
from . import views

app_name = 'interactive_basics'
urlpatterns = [
    path('', views.date_lab_view, name='date_lab'),
    path('api/create-date/', views.api_create_date, name='api_create_date'),
    path('api/add-period/', views.api_add_period, name='api_add_period'),
    path('api/advance-days/', views.api_advance_days, name='api_advance_days'),
    path('api/create-schedule/', views.api_create_schedule, name='api_create_schedule'),
    path('api/create-rate/', views.api_create_rate, name='api_create_rate'),
]