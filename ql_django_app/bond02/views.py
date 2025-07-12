from django.shortcuts import render
from .forms import BondPricingForm
import numpy as np
import QuantLib as ql


def price_bond(request):
    price = None  # Default value for price
    error_message = None  # Placeholder for any error messages

    if request.method == 'POST':
        form = BondPricingForm(request.POST)
        if form.is_valid():
            # Extract cleaned data from the form
            face_value = form.cleaned_data['face']
            coupon_rate = form.cleaned_data['coupon_rate'] / 100  # Convert to decimal
            maturity_years = form.cleaned_data['maturity_years']
            coupon_frequency = form.cleaned_data['coupon_frequency']
            yield_rate = form.cleaned_data['yield_rate'] / 100  # Convert to decimal

            try:
                ql_frequency_mapping = {
                    'Annual': ql.Annual,
                    'Semiannual': ql.Semiannual,
                    'Quarterly': ql.Quarterly,
                    'Monthly': ql.Monthly
                }
                coupon_frequency = ql_frequency_mapping.get(coupon_frequency)

                print('coupon_frequency', coupon_frequency)
                issue_date = ql.Date.todaysDate()
                calc_date = ql.Date.todaysDate() + 11 # 11 days from today
                ql.Settings.instance().evaluationDate = calc_date

                flat_rate = ql.SimpleQuote(yield_rate)
                rate_handle = ql.QuoteHandle(flat_rate)
                day_count = ql.Actual360()
                calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
                ts_yield = ql.FlatForward(calc_date, rate_handle, day_count)
                ts_handle = ql.YieldTermStructureHandle(ts_yield)

                maturity_date = issue_date + ql.Period(maturity_years * 12, ql.Months)

                tenor = ql.Period(int(coupon_frequency))
                calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
                business_convention = ql.Unadjusted
                date_generation = ql.DateGeneration.Backward
                month_end = False
                schedule = ql.Schedule(issue_date, 
                                    maturity_date,
                                    tenor, 
                                    calendar,
                                    business_convention,
                                    business_convention,
                                    date_generation,
                                    month_end)

                day_count = ql.Thirty360(ql.Thirty360.BondBasis)
                coupons = [coupon_rate]

                # Now lets construct the FixedRateBond
                settlement_days = 0
                fixed_rate_bond = ql.FixedRateBond(
                    settlement_days,
                    face_value,
                    schedule,
                    coupons,
                    day_count)

                bond_engine = ql.DiscountingBondEngine(ts_handle)
                fixed_rate_bond.setPricingEngine(bond_engine)
                price = np.round(fixed_rate_bond.NPV())

            except Exception as e:
                error_message = f"An error occurred during bond pricing: {e}"
        else:
            error_message = "Invalid form submission. Please correct the errors and try again."

    else:
        form = BondPricingForm()  # Initialize empty form for GET request

    # Render the template with the form, price, and any error messages
    return render(request, 'bond02/bond_price.html', {
        'form': form,
        'price': price,
        'error_message': error_message
    })
