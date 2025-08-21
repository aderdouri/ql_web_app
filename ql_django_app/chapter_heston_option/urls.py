from django.urls import path
from . import views
app_name = 'chapter_heston_option'
urlpatterns = [
path('', views.heston_lab_view, name='heston_lab'),
]