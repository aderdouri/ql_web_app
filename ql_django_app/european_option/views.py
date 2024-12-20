from django.shortcuts import render
from .forms import EuropeanOptionForm
import QuantLib as ql
import numpy as np

def price_european_option(request):
    price = None
    error_message = None

    if request.method == 'POST':
        form = EuropeanOptionForm(request.POST)
        if form.is_valid():
            try:
                option_type = form.cleaned_data['option_type']
                maturity_date = form.cleaned_data['maturity_date']
                spot_price = form.cleaned_data['spot_price']
                strike_price = form.cleaned_data['strike_price']
                volatility = form.cleaned_data['volatility'] / 100
                dividend_rate = form.cleaned_data['dividend_rate'] / 100
                risk_free_rate = form.cleaned_data['risk_free_rate'] / 100

                # Option parameters
                option_type = ql.Option.Call if option_type == 'Call' else ql.Option.Put
                maturity_date = ql.Date(maturity_date.day, maturity_date.month, maturity_date.year)

                day_count = ql.Actual365Fixed()
                calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)

                calculation_date = ql.Date(8, 5, 2015)
                ql.Settings.instance().evaluationDate = calculation_date

                payoff = ql.PlainVanillaPayoff(option_type, strike_price)
                exercise = ql.EuropeanExercise(maturity_date)
                european_option = ql.VanillaOption(payoff, exercise)

                spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))

                flat_ts = ql.YieldTermStructureHandle(
                    ql.FlatForward(calculation_date, 
                                risk_free_rate, 
                                day_count)
                )
                dividend_yield = ql.YieldTermStructureHandle(
                    ql.FlatForward(calculation_date, 
                                dividend_rate, 
                                day_count)
                )
                flat_vol_ts = ql.BlackVolTermStructureHandle(
                    ql.BlackConstantVol(calculation_date, 
                                        calendar, 
                                        volatility, 
                                        day_count)
                )
                bsm_process = ql.BlackScholesMertonProcess(spot_handle, 
                                                        dividend_yield, 
                                                        flat_ts, 
                                                        flat_vol_ts)

                european_option.setPricingEngine(ql.AnalyticEuropeanEngine(bsm_process))
                price = np.round(european_option.NPV(), 4)

            except Exception as e:
                error_message = str(e)
        else:
            error_message = "Invalid form data. Please correct the errors below."
    else:
        form = EuropeanOptionForm()

    return render(request, 'european_option/price_european_option.html', {'form': form, 'price': price, 'error_message': error_message})