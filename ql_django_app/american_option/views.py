# filepath: /Users/aderdouri/Downloads/ql_web_app/ql_django_app/american_option/views.py
from django.shortcuts import render
from .forms import AmericanOptionForm
import QuantLib as ql
import numpy as np

def price_american_option(request):
    price = None
    error_message = None

    if request.method == 'POST':
        form = AmericanOptionForm(request.POST)
        if form.is_valid():
            try:
                option_type = form.cleaned_data['option_type']
                maturity_date = form.cleaned_data['maturity_date']
                spot_price = form.cleaned_data['spot_price']
                strike_price = form.cleaned_data['strike_price']
                volatility = form.cleaned_data['volatility']/100
                dividend_rate = form.cleaned_data['dividend_rate']/100
                risk_free_rate = form.cleaned_data['risk_free_rate']/100

                # QuantLib setup
                #calculation_date = ql.Date.todaysDate()
                calculation_date = ql.Date(8, 5, 2015)
                ql.Settings.instance().evaluationDate = calculation_date

                # Option parameters
                maturity_date = ql.Date(maturity_date.day, maturity_date.month, maturity_date.year)

                payoff = ql.PlainVanillaPayoff(ql.Option.Call if option_type == 'Call' else ql.Option.Put, strike_price)

                # Market data
                spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))
                flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, risk_free_rate / 100, ql.Actual365Fixed()))
                dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, dividend_rate, ql.Actual365Fixed()))
                vol_handle = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, ql.NullCalendar(), volatility, ql.Actual365Fixed()))

                # Black-Scholes process
                bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, vol_handle)

                def binomial_price(option, bsm_process, steps):
                    binomial_engine = ql.BinomialVanillaEngine(bsm_process, "crr", steps)
                    option.setPricingEngine(binomial_engine)
                    return option.NPV()

                settlement = calculation_date
                am_exercise = ql.AmericanExercise(settlement, maturity_date)
                american_option = ql.VanillaOption(payoff, am_exercise)

                steps = range(2, 200, 1)
                prices = [binomial_price(american_option, bsm_process, step) for step in steps]

                # American option
                price = np.round(np.mean(prices), 4)

            except Exception as e:
                error_message = str(e)
        else:
            error_message = "Invalid form data. Please correct the errors below."
    else:
        form = AmericanOptionForm()

    return render(request, 'american_option/price_american_option.html', {'form': form, 'price': price, 'error_message': error_message})