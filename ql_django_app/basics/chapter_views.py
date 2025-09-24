# basics/chapter_views.py

from django.shortcuts import render

def chapter1_quantlib_basics(request):
    """Chapter 1: QuantLib Basics dedicated page"""
    context = {
        'chapter_title': 'Chapter 1: QuantLib Basics',
        'chapter_icon': 'bi-calendar-date',
        'chapter_description': 'Master the fundamental concepts of quantitative finance with interactive laboratories covering dates, calendars, schedules, and interest rates.'
    }
    return render(request, 'basics/chapter1_quantlib_basics.html', context)

def chapter2_instruments(request):
    """Chapter 2: Instruments and Pricing Engines dedicated page"""
    context = {
        'chapter_title': 'Chapter 2: Instruments & Pricing',
        'chapter_icon': 'bi-gear',
        'chapter_description': 'Learn about financial instruments and pricing engines in QuantLib. Master different pricing methodologies and their applications.'
    }
    return render(request, 'basics/chapter2_instruments.html', context)

def chapter3_greeks(request):
    """Chapter 3: Numerical Greeks dedicated page"""
    context = {
        'chapter_title': 'Chapter 3: Numerical Greeks',
        'chapter_icon': 'bi-graph-up',
        'chapter_description': 'Calculate option sensitivities using numerical differentiation methods for barrier options.'
    }
    return render(request, 'basics/chapter3_numerical_greeks.html', context)

def chapter4_quotes(request):
    """Chapter 4: Market Quotes dedicated page"""
    context = {
        'chapter_title': 'Chapter 4: Market Quotes',
        'chapter_icon': 'bi-currency-dollar',
        'chapter_description': 'Learn how to work with market quotes and build bond discount curves using QuantLib. Master Nelson-Siegel curve fitting and real-time quote updates.'
    }
    return render(request, 'basics/chapter4_quotes.html', context)

def chapter5_curves(request):
    """Chapter 5: Term Structures and their Reference Dates dedicated page"""
    context = {
        'chapter_title': 'Chapter 5: Term Structures and their Reference Dates',
        'chapter_icon': 'bi-graph-up-arrow',
        'chapter_description': 'Learn how to set up term structures so that they track (or don\'t track) the global evaluation date. Explore reference dates, curve construction, and the observer pattern.'
    }
    return render(request, 'basics/chapter5_curves.html', context)

def chapter6_pricing_range(request):
    """Chapter 6: Pricing Over Time dedicated page"""
    context = {
        'chapter_title': 'Chapter 6: Pricing Over Time',
        'chapter_icon': 'bi-calendar-range',
        'chapter_description': 'Learn to price instruments over a range of days and time periods for historical analysis and risk monitoring.'
    }
    return render(request, 'basics/chapter6_pricing_range.html', context)

def chapter7_random(request):
    """Chapter 7: Random Numbers dedicated page"""
    context = {
        'chapter_title': 'Chapter 7: Random Numbers',
        'chapter_icon': 'bi-shuffle',
        'chapter_description': 'Master random number generation for Monte Carlo simulations and advanced numerical methods in quantitative finance.'
    }
    return render(request, 'basics/chapter7_random.html', context)

