from django.urls import path
from . import views

app_name = 'chapter19_swap'
urlpatterns = [
    path('', views.swap_description_view, name='description'),
    path('pricer/', views.pricer_view, name='pricer'),
]