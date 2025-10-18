from django.urls import path
from . import views

app_name = 'chapter18_par_indexed_coupons'

urlpatterns = [
    path('', views.par_indexed_coupons_description_view, name='description'),
    path('lab/', views.par_indexed_coupons_lab_view, name='par_indexed_coupons_lab'),
]




