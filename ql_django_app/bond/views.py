from django.shortcuts import render
from .forms import BondForm
import QuantLib as ql


def price_bond(request):
    price = None  # Default value for price
    error_message = None  # Placeholder for any error messages

    if request.method == 'POST':
        form = BondForm(request.POST)
        if form.is_valid():
            # Extract cleaned data from the form
            face = form.cleaned_data['face']
            coupon_rate = form.cleaned_data['coupon_rate'] / 100  # Convert to decimal
            maturity_years = form.cleaned_data['maturity_years']
            frequency = form.cleaned_data['frequency']
            yield_rate = form.cleaned_data['yield_rate'] / 100  # Convert to decimal

            try:
                # Set up calendar and dates
                calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
                settlement_date = ql.Date.todaysDate()
                ql.Settings.instance().evaluationDate = settlement_date

                maturity_date = calendar.advance(settlement_date, 
                                                 ql.Period(maturity_years, ql.Years))

                # Convert frequency to QuantLib-compatible format
                ql_frequency_mapping = {
                    'Annual': ql.Annual,
                    'Semiannual': ql.Semiannual,
                    'Quarterly': ql.Quarterly,
                    'Monthly': ql.Monthly
                }
                ql_frequency = ql_frequency_mapping.get(frequency, ql.Annual)

                # Schedule generation
                schedule = ql.Schedule(settlement_date,
                                       maturity_date,
                                       ql.Period(ql_frequency),
                                       calendar,
                                       ql.Following,
                                       ql.Following,
                                       ql.DateGeneration.Backward,
                                       False)

                # Create bond with ActualActual and Schedule
                bond = ql.FixedRateBond(
                    settlementDays=3,
                    faceAmount=face,
                    schedule=schedule,
                    coupons=[coupon_rate],
                    paymentDayCounter=ql.Thirty360(ql.Thirty360.BondBasis)  # Correct parameter name
                    )

                # Pricing engine with flat yield curve
                yield_curve = ql.FlatForward(settlement_date, 
                                             ql.QuoteHandle(ql.SimpleQuote(yield_rate)), 
                                             ql.Actual360())
                
                bond_engine = ql.DiscountingBondEngine(ql.YieldTermStructureHandle(yield_curve))
                bond.setPricingEngine(bond_engine)

                # Calculate bond price
                price = bond.cleanPrice()

            except Exception as e:
                error_message = f"An error occurred during bond pricing: {e}"
        else:
            error_message = "Invalid form submission. Please correct the errors and try again."

    else:
        form = BondForm()  # Initialize empty form for GET request

    # Render the template with the form, price, and any error messages
    return render(request, 'bond/price_bond.html', {
        'form': form,
        'price': price,
        'error_message': error_message
    })
