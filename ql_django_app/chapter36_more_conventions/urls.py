# urls.py

from django.urls import path
from .views import short_coupon_lab_view, more_conventions_description_view

app_name = 'short_coupon_glitch'

urlpatterns = [
    path('', more_conventions_description_view, name='description'),
    path('lab/', short_coupon_lab_view, name='lab'),
]
