from django.shortcuts import render

def home(request):
    return render(request, 'equity_models/home.html')

def valuing_options_view(request):
    return render(request, 'equity_models/valuing_options.html')