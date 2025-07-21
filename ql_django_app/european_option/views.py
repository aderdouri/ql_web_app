# File: ql_web_app/european_option/views.py (FINAL AND COMPLETE CODE)

from django.shortcuts import render
from django.contrib import messages
from .forms import EuropeanOptionForm
from . import services

def price_european_option(request):
    """
    Handles the web request, form processing, and calls the calculation service.
    """
    form = EuropeanOptionForm()
    results = None

    if request.method == 'POST':
        form = EuropeanOptionForm(request.POST)
        if form.is_valid():
            try:
                # Call the service with the cleaned data from the form
                results = services.calculate_european_option_metrics(
                    option_type_str=form.cleaned_data['option_type'],
                    maturity_dt=form.cleaned_data['maturity_date'],
                    spot_price=form.cleaned_data['spot_price'],
                    strike_price=form.cleaned_data['strike_price'],
                    volatility_pct=form.cleaned_data['volatility'],
                    dividend_rate_pct=form.cleaned_data['dividend_rate'],
                    risk_free_rate_pct=form.cleaned_data['risk_free_rate'],
                    pricing_engine_name=form.cleaned_data['pricing_engine'],
                    binomial_steps=form.cleaned_data.get('binomial_steps', 200)
                )
            except Exception as e:
                # Display a user-friendly error message if the calculation fails
                messages.error(request, f"QuantLib Calculation Error: {e}")
        else:
            messages.warning(request, "Invalid form data. Please correct the errors below.")
            
    context = {
        'form': form, 
        'results': results
    }
    return render(request, 'european_option/pricer.html', context)