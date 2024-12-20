import numpy as np
import QuantLib as ql
from django.shortcuts import render
from .forms import SwapForm

def price_swap(request):
    price = None
    fair_spread = None
    fair_rate = None
    fixed_leg_bps = None
    floating_leg_bps = None
    error_message = None

    if request.method == 'POST':
        form = SwapForm(request.POST)
        if form.is_valid():
            try:
                # Extract form data
                notional = int(form.cleaned_data['notional'])
                fixed_rate = form.cleaned_data['fixed_rate'] / 100
                floating_rate = form.cleaned_data['floating_rate'] / 100
                maturity_years = form.cleaned_data['maturity_years']
                fixed_frequency = form.cleaned_data['fixed_frequency']
                floating_frequency = form.cleaned_data['floating_frequency']


                calculation_date = ql.Date(20, 10, 2015)
                ql.Settings.instance().evaluationDate = calculation_date

                # Mapping frequency strings to QuantLib frequencies
                ql_frequency_mapping = {
                    'Annual': 12,
                    'Semiannual': 6,
                    'Quarterly': 3,
                    'Monthly': 1
                }

                ql_fixed_frequency = ql_frequency_mapping.get(fixed_frequency)
                ql_floating_frequency = ql_frequency_mapping.get(floating_frequency)

                risk_free_rate = 0.01
                libor_rate = floating_rate
                day_count = ql.Actual365Fixed()

                discount_curve = ql.YieldTermStructureHandle(
                    ql.FlatForward(calculation_date, risk_free_rate, day_count)
                )

                libor_curve = ql.YieldTermStructureHandle(
                    ql.FlatForward(calculation_date, libor_rate, day_count)
                )
                libor3M_index = ql.USDLibor(ql.Period(3, ql.Months), libor_curve)
                
                calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
                settle_date = calendar.advance(calculation_date, 5, ql.Days)
                maturity_date = calendar.advance(settle_date, maturity_years, ql.Years)

                fixed_leg_tenor = ql.Period(ql_fixed_frequency, ql.Months)
                fixed_schedule = ql.Schedule(settle_date, maturity_date, 
                                            fixed_leg_tenor, calendar,
                                            ql.ModifiedFollowing, ql.ModifiedFollowing,
                                            ql.DateGeneration.Forward, False)

                float_leg_tenor = ql.Period(ql_floating_frequency, ql.Months)
                float_schedule = ql.Schedule(settle_date, maturity_date, 
                                            float_leg_tenor, calendar,
                                            ql.ModifiedFollowing, ql.ModifiedFollowing,
                                            ql.DateGeneration.Forward, False)
                
                fixed_leg_daycount = ql.Actual360()
                float_spread = 0.004
                float_leg_daycount = ql.Actual360()

                ir_swap = ql.VanillaSwap(ql.VanillaSwap.Payer, notional, fixed_schedule, 
                                        fixed_rate, fixed_leg_daycount, float_schedule,
                                        libor3M_index, float_spread, float_leg_daycount)
                

                swap_engine = ql.DiscountingSwapEngine(discount_curve)
                ir_swap.setPricingEngine(swap_engine)
                

                # Calculate swap price
                price = np.round(ir_swap.NPV(), 4)
                fair_spread = np.round(ir_swap.fairSpread(), 4)
                fair_rate = np.round(ir_swap.fairRate(), 4)
                fixed_leg_bps = np.round(ir_swap.fixedLegBPS(), 4)
                floating_leg_bps = np.round(ir_swap.floatingLegBPS(), 4)

            except Exception as e:
                error_message = f"An error occurred during swap pricing: {str(e)}"
    else:
        form = SwapForm()
    return render(request, 'swap/price_swap.html', {
        'form': form,
        'price': price,
        'fair_spread': fair_spread,
        'fair_rate': fair_rate,
        'fixed_leg_bps': fixed_leg_bps,
        'floating_leg_bps': floating_leg_bps,
        'error_message': error_message
    })