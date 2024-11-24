from django.shortcuts import render
from .forms import SwaptionForm
import QuantLib as ql

def price_swaption(request):
    price = None
    if request.method == 'POST':
        form = SwaptionForm(request.POST)
        if form.is_valid():
            # Extract form data
            option_type = form.cleaned_data['option_type']
            strike = form.cleaned_data['strike']
            maturity = form.cleaned_data['maturity']
            tenor = form.cleaned_data['tenor']
            notional = form.cleaned_data['notional']
            fixed_rate = form.cleaned_data['fixed_rate']
            volatility = form.cleaned_data['volatility']

            # QuantLib Swaption Pricing
            calendar = ql.UnitedStates()
            settlement_date = ql.Date.todaysDate()
            ql.Settings.instance().evaluationDate = settlement_date

            # Swap details
            swap_maturity_date = calendar.advance(settlement_date, ql.Period(tenor, ql.Years))
            fixed_schedule = ql.Schedule(settlement_date, swap_maturity_date, ql.Period(ql.Annual),
                                        calendar, ql.ModifiedFollowing, ql.ModifiedFollowing,
                                        ql.DateGeneration.Backward, False)
            floating_schedule = ql.Schedule(settlement_date, swap_maturity_date, ql.Period(ql.Semiannual),
                                           calendar, ql.ModifiedFollowing, ql.ModifiedFollowing,
                                           ql.DateGeneration.Backward, False)
            libor_index = ql.USDLibor(ql.Period(ql.Semiannual))
            swap = ql.VanillaSwap(ql.VanillaSwap.Payer, notional,
                                 fixed_schedule, fixed_rate, ql.ActualActual(),
                                 floating_schedule, libor_index, 0.0, ql.ActualActual())

            # Swaption details
            exercise_date = calendar.advance(settlement_date, ql.Period(maturity, ql.Years))
            option_exercise = ql.EuropeanExercise(exercise_date)
            swaption_type = ql.VanillaSwaption.OptionType.Call if option_type == 'Call' else ql.VanillaSwaption.OptionType.Put
            swaption = ql.VanillaSwaption(swap, option_exercise, swaption_type)

            # Yield and volatility curves
            flat_yield = ql.FlatForward(settlement_date, 0.05, ql.ActualActual(), ql.Compounded, ql.Annual)
            yield_curve = ql.YieldTermStructureHandle(flat_yield)
            flat_vol = ql.BlackConstantVol(settlement_date, calendar, volatility, ql.ActualActual())
            vol_curve = ql.BlackVolTermStructureHandle(flat_vol)

            # Pricing engine
            engine = ql.BlackSwaptionEngine(yield_curve, vol_curve)
            swaption.setPricingEngine(engine)

            price = swaption.NPV()
    else:
        form = SwaptionForm()
    return render(request, 'swaption/price_swaption.html', {'form': form, 'price': price})