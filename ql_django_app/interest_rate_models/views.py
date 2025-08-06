from django.shortcuts import render

def home(request):
    return render(request, 'interest_rate_models/base.html')