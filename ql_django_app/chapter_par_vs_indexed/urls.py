from django.urls import path
from . import views

app_name = 'chapter_par_vs_indexed'
urlpatterns = [
    path('', views.coupon_lab_view, name='coupon_lab'),
]