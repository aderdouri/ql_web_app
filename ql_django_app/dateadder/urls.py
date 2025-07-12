from django.urls import path
from . import views
 
app_name = "dateadder"
 
urlpatterns = [
    path('', views.date_adder_view, name='date_adder'),
]