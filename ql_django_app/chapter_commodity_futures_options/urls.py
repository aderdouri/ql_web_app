from django.urls import path
from . import views

app_name = 'chapter_commodity_futures_options'

urlpatterns = [
    path('', views.commodity_futures_lab, name='commodity_futures_lab'),
]


