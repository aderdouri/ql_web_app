from django.urls import path
from . import views

app_name = 'chapter_heston_scipy'
urlpatterns = [
    path('', views.scipy_lab_view, name='scipy_lab'),
]