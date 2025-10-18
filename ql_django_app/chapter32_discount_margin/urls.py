from django.urls import path
from .views import discount_margin_lab_view, discount_margin_description_view

app_name = 'chapter32_discount_margin'

urlpatterns = [
    path('', discount_margin_description_view, name='description'),
    path('lab/', discount_margin_lab_view, name='lab'),
]










