from django.urls import path
from . import views

app_name = 'chapter4_quotes'
urlpatterns = [
    path('', views.market_lab_view, name='market_lab'),
]