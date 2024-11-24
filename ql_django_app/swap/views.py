# views.py

import QuantLib as ql
from django.shortcuts import render
from .forms import SwapForm

def price_swap(request):
    price = None
    error_message = None
    if request.method == 'POST':
        form = SwapForm(request.POST)
        if form.is_valid():
            try:
                # Extract form data
                notional = int(form.cleaned_data['face'])
                fixed_rate = form.cleaned_data['fixed_rate'] / 100
                floating_rate = form.cleaned_data['floating_rate'] / 100
                maturity_years = form.cleaned_data['maturity_years']
                fixed_frequency = form.cleaned_data['fixed_frequency']
                floating_frequency = form.cleaned_data['floating_frequency']

                # Set up calendar and dates
                calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
                settlement_date = ql.Date.todaysDate()
                ql.Settings.instance().evaluationDate = settlement_date

                maturity_date = calendar.advance(
                    settlement_date, 
                    ql.Period(maturity_years, ql.Years)
                )

                # Mapping frequency strings to QuantLib frequencies
                ql_frequency_mapping = {
                    'Annual': ql.Annual,
                    'Semiannual': ql.Semiannual,
                    'Quarterly': ql.Quarterly,
                    'Monthly': ql.Monthly
                }
                ql_fixed_frequency = ql_frequency_mapping.get(fixed_frequency, ql.Annual)
                ql_floating_frequency = ql_frequency_mapping.get(floating_frequency, ql.Semiannual)


                risk_free_rate = 0.01
                day_count = ql.Actual365Fixed()

                discount_curve = ql.YieldTermStructureHandle(
                    ql.FlatForward(settlement_date, risk_free_rate, day_count)
                )

                libor_curve = ql.YieldTermStructureHandle(
                    ql.FlatForward(settlement_date, floating_rate, day_count)
                )
                libor_index = ql.USDLibor(ql.Period(ql_floating_frequency, ql.Months), libor_curve)

                calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
                settlement_date = calendar.advance(settlement_date, 5, ql.Days)

                fixed_leg_tenor = ql.Period(ql_fixed_frequency, ql.Months)
                fixed_schedule = ql.Schedule(settlement_date, 
                                             maturity_date, 
                                             fixed_leg_tenor, 
                                             calendar,
                                             ql.ModifiedFollowing, 
                                             ql.ModifiedFollowing,
                                             ql.DateGeneration.Forward, 
                                             False)

                float_leg_tenor = ql.Period(ql_floating_frequency, ql.Months)
                float_schedule = ql.Schedule(settlement_date, 
                                             maturity_date, 
                                            float_leg_tenor, 
                                            calendar,
                                            ql.ModifiedFollowing, 
                                            ql.ModifiedFollowing,
                                            ql.DateGeneration.Forward, 
                                            False)

                fixed_leg_daycount = ql.Actual360()
                float_spread = 0.004
                float_leg_daycount = ql.Actual360()

                ir_swap = ql.VanillaSwap(ql.VanillaSwap.Payer, 
                                         notional, 
                                         fixed_schedule, 
                                         fixed_rate, 
                                         fixed_leg_daycount, 
                                         float_schedule,
                                         libor_index, 
                                         float_spread, 
                                         float_leg_daycount)

                swap_engine = ql.DiscountingSwapEngine(discount_curve)
                ir_swap.setPricingEngine(swap_engine)

                # Calculate swap price
                price = ir_swap.NPV()
            except Exception as e:
                error_message = f"An error occurred during swap pricing: {str(e)}"
    else:
        form = SwapForm()
    return render(request, 'swap/price_swap.html', {
        'form': form, 
        'price': price, 
        'error_message': error_message
    })