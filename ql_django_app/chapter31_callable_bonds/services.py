import QuantLib as ql
import numpy as np
import datetime

def format_date_professional(ql_date):
    """Format QuantLib date to professional format like 'June 15th, 2017'"""
    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    day = ql_date.dayOfMonth()
    month = month_names[ql_date.month() - 1]
    year = ql_date.year()
    
    # Add ordinal suffix
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    
    return f"{month} {day}{suffix}, {year}"

def generate_dynamic_explanations(data, current_price, sigmas, prices):
    """Generate dynamic explanations based on the results"""
    explanations = {}
    
    # Bond price explanation
    if current_price < 100:
        explanations['price_analysis'] = f"The bond is trading at a discount (${current_price:.2f} vs $100 par value), indicating that the coupon rate ({data['coupon_rate']*100:.1f}%) is below the current market yield ({data['yield_curve_rate']*100:.1f}%)."
    elif current_price > 100:
        explanations['price_analysis'] = f"The bond is trading at a premium (${current_price:.2f} vs $100 par value), indicating that the coupon rate ({data['coupon_rate']*100:.1f}%) is above the current market yield ({data['yield_curve_rate']*100:.1f}%)."
    else:
        explanations['price_analysis'] = f"The bond is trading at par value (${current_price:.2f}), indicating that the coupon rate ({data['coupon_rate']*100:.1f}%) equals the current market yield ({data['yield_curve_rate']*100:.1f}%)."
    
    # Volatility sensitivity explanation
    price_change = prices[-1] - prices[0] if len(prices) > 1 else 0
    volatility_range = sigmas[-1] - sigmas[0] if len(sigmas) > 1 else 0
    
    if price_change < -5:
        explanations['volatility_impact'] = f"High sensitivity to volatility: Price decreases by ${abs(price_change):.2f} over the volatility range ({volatility_range*100:.1f}%). This indicates significant call risk."
    elif price_change < -2:
        explanations['volatility_impact'] = f"Moderate sensitivity to volatility: Price decreases by ${abs(price_change):.2f} over the volatility range ({volatility_range*100:.1f}%)."
    else:
        explanations['volatility_impact'] = f"Low sensitivity to volatility: Price changes by ${abs(price_change):.2f} over the volatility range ({volatility_range*100:.1f}%)."
    
    # Model parameters explanation
    explanations['model_parameters'] = f"Using Hull-White model with mean reversion of {data['mean_reversion']:.3f} and volatility of {data['volatility']:.3f}. The {data['grid_points']}-point tree provides {'high' if data['grid_points'] >= 50 else 'moderate'} accuracy."
    
    # Callability explanation
    explanations['callability'] = f"The bond has 24 quarterly call dates starting from September 15th, 2016, with a call price of $100. Higher volatility increases the probability of early redemption."
    
    return explanations

def price_callable_bond_and_analyze(data):
    """
    Prices a callable bond using the Hull-White model and analyzes its sensitivity to volatility.
    Based on the book's implementation.
    """
    try:
        # 1. Setup from form data - exactly like the book
        eval_date = data['evaluation_date']
        calc_date = ql.Date(eval_date.day, eval_date.month, eval_date.year)
        ql.Settings.instance().evaluationDate = calc_date

        # Compatibility with QuantLib < 1.22 (from the book)
        try:
            ql.BondPrice
        except:
            ql.BondPrice = ql.CallabilityPrice

        # 2. Construct the flat yield curve - exactly like the book
        day_count = ql.ActualActual(ql.ActualActual.Bond)
        rate = data['yield_curve_rate']
        ts = ql.FlatForward(calc_date, rate, day_count, ql.Compounded, ql.Semiannual)
        ts_handle = ql.YieldTermStructureHandle(ts)

        # 3. Create the callability schedule - using default values
        callability_schedule = ql.CallabilitySchedule()
        call_price = 100.0
        first_call_date = datetime.date(2016, 9, 15)
        call_frequency_months = 3
        number_of_calls = 24
        
        call_date = ql.Date(first_call_date.day, first_call_date.month, first_call_date.year)
        null_calendar = ql.NullCalendar()
        
        for i in range(0, number_of_calls):
            callability_price = ql.BondPrice(call_price, ql.BondPrice.Clean)
            callability_schedule.append(
                ql.Callability(callability_price, ql.Callability.Call, call_date)
            )
            call_date = null_calendar.advance(call_date, call_frequency_months, ql.Months)
            
        # 4. Create the bond schedule - using default values
        issue_date_data = datetime.date(2014, 9, 16)
        maturity_date_data = datetime.date(2022, 9, 15)
        
        issue_date = ql.Date(issue_date_data.day, issue_date_data.month, issue_date_data.year)
        maturity_date = ql.Date(maturity_date_data.day, maturity_date_data.month, maturity_date_data.year)
        calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
        tenor = ql.Period(ql.Quarterly)
        accrual_convention = ql.Unadjusted
        
        schedule = ql.Schedule(issue_date, maturity_date, tenor, calendar, 
                              accrual_convention, accrual_convention,
                              ql.DateGeneration.Backward, False)
        
        # 5. Create the callable bond - using default values
        settlement_days = 3
        face_amount = 100
        accrual_daycount = ql.ActualActual(ql.ActualActual.Bond)
        coupon = data['coupon_rate']
        
        bond = ql.CallableFixedRateBond(
            settlement_days, face_amount, schedule, [coupon], accrual_daycount,
            ql.Following, face_amount, issue_date, callability_schedule
        )

        # 6. Pricing function - exactly like the book
        def value_bond(a, s, grid_points, bond):
            model = ql.HullWhite(ts_handle, a, s)
            engine = ql.TreeCallableFixedRateBondEngine(model, grid_points)
            bond.setPricingEngine(engine)
            return bond
            
        # 7. Calculate current price
        mean_reversion = data['mean_reversion']
        volatility = data['volatility']
        grid_points = data['grid_points']
        
        bond_with_engine = value_bond(mean_reversion, volatility, grid_points, bond)
        current_price = bond_with_engine.cleanPrice()
        
        # 8. Generate sensitivity data - exactly like the book
        sigma_min = data['sigma_min']
        sigma_max = data['sigma_max']
        sigma_step = data['sigma_step']
        
        sigmas = np.arange(sigma_min, sigma_max, sigma_step)
        prices = [value_bond(mean_reversion, s, grid_points, bond).cleanPrice() for s in sigmas]

        # 9. Extract cashflows with professional date formatting
        cashflows_data = []
        for cf in bond.cashflows():
            cashflows_data.append({
                'date': format_date_professional(cf.date()),
                'amount': cf.amount()
            })

        # 10. Generate dynamic explanations
        explanations = generate_dynamic_explanations(data, current_price, sigmas, prices)

        return {
            'current_price': current_price,
            'sensitivity_chart_data': {
                'sigmas': sigmas.tolist(),
                'prices': prices
            },
            'cashflows': cashflows_data,
            'explanations': explanations
        }

    except Exception as e:
        return {'error': str(e)}