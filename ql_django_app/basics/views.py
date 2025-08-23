from django.shortcuts import render

def home(request):
    return render(request, 'basics/base.html')

def quantlib_basics_view(request):
    return render(request, 'basics/quantlib_basics.html')

def instruments_engines_view(request):
    return render(request, 'basics/instruments_engines.html')

def numerical_greeks_view(request):
    return render(request, 'basics/numerical_greeks.html')

def market_quotes_view(request):
    return render(request, 'basics/market_quotes.html')

def term_structures_view(request):
    return render(request, 'basics/term_structures.html')

def pricing_over_range_view(request):
    return render(request, 'basics/pricing_over_range.html')

def random_numbers_view(request):
    return render(request, 'basics/random_numbers.html')