# services.py

import QuantLib as ql
import datetime

def analyze_treasury_futures(data):
    """
    Reproduces the analysis from Chapter 34:
    1. Builds a yield curve.
    2. Prices a treasury future with a fictional deliverable.
    3. Finds the Cheapest-to-Deliver (CTD) bond.
    4. Re-prices the future using the CTD.
    """
    try:
        # 1. Setup from form data
        # Use the evaluation date from the form
        eval_date = data['evaluation_date']
        
        # Handle both datetime.date objects and string dates
        if hasattr(eval_date, 'day'):
            calc_date = ql.Date(eval_date.day, eval_date.month, eval_date.year)
        else:
            # If it's a string, parse it
            from datetime import datetime
            if isinstance(eval_date, str):
                eval_date = datetime.strptime(eval_date, '%Y-%m-%d').date()
            calc_date = ql.Date(eval_date.day, eval_date.month, eval_date.year)
        
        ql.Settings.instance().evaluationDate = calc_date
        
        futures_price = data['futures_price']
        
        day_count = ql.ActualActual(ql.ActualActual.ISDA)
        calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
        
        # 2. Build Yield Curve (using relative dates from evaluation date)
        # Make yield curve dynamic based on futures price
        base_prices = [99.9935, 99.9576, 99.8119, 99.5472, 99.8867, 100.0664, 99.8711, 100.0547, 100.3047, 100.2266]
        base_coupon_rates = [0.0000, 0.0000, 0.0000, 0.0000, 0.00875, 0.0125, 0.01625, 0.02, 0.0225, 0.03]
        
        # Adjust prices and coupons based on futures price
        futures_price_factor = futures_price / 127.0625  # Normalize to book's base price
        price_adjustment = (futures_price - 127.0625) * 0.01  # Small adjustment factor
        
        prices = [max(95.0, min(105.0, price + price_adjustment)) for price in base_prices]
        coupon_rates = [rate * (0.9 + 0.2 * futures_price_factor) for rate in base_coupon_rates]
        
        # Create relative maturity dates from evaluation date
        maturity_periods = [ql.Period(1, ql.Months), ql.Period(3, ql.Months), ql.Period(6, ql.Months), ql.Period(1, ql.Years),
                           ql.Period(2, ql.Years), ql.Period(3, ql.Years), ql.Period(5, ql.Years), ql.Period(7, ql.Years),
                           ql.Period(10, ql.Years), ql.Period(30, ql.Years)]
        maturity_dates = [calc_date + period for period in maturity_periods]
        
        # Create relative issue dates (assume bonds issued 6 months before maturity)
        issue_dates = [maturity - ql.Period(6, ql.Months) for maturity in maturity_dates]

        bond_helpers = []
        for coupon, issue_date, maturity_date, price in zip(coupon_rates, issue_dates, maturity_dates, prices):
            schedule = ql.Schedule(calc_date, maturity_date, ql.Period(6, ql.Months), calendar, ql.Following, ql.Following, ql.DateGeneration.Backward, False)
            helper = ql.FixedRateBondHelper(ql.QuoteHandle(ql.SimpleQuote(price)), 0, 100.0, schedule, [coupon], day_count, ql.Following)
            bond_helpers.append(helper)

        yield_curve = ql.PiecewiseCubicZero(calc_date, bond_helpers, day_count)
        yield_curve_handle = ql.YieldTermStructureHandle(yield_curve)
        
        # 3. Naive Calculation (with fictional deliverable)
        def create_tsy_security(issue_date, maturity_date, coupon_rate):
            schedule = ql.Schedule(issue_date, maturity_date, ql.Period(6, ql.Months), calendar, ql.ModifiedFollowing, ql.ModifiedFollowing, ql.DateGeneration.Forward, False)
            return ql.FixedRateBond(0, 100.0, schedule, [coupon_rate], day_count)

        fictional_bond = create_tsy_security(calc_date, calc_date + ql.Period(10, ql.Years), 0.06)
        fictional_bond.setPricingEngine(ql.DiscountingBondEngine(yield_curve_handle))
        
        # Use relative delivery date (1 month after evaluation date)
        delivery_date = calc_date + ql.Period(1, ql.Months)
        clean_price = ql.BondPrice(futures_price * yield_curve.discount(delivery_date), ql.BondPrice.Clean)
        z_spread_fictional = ql.BondFunctions.zSpread(fictional_bond, clean_price, yield_curve, day_count, ql.Compounded, ql.Semiannual, calc_date) * 10000

        # 4. Cheapest to Deliver (CTD) Calculation
        # Create dynamic bond basket based on futures price and evaluation date
        basket_maturities = [calc_date + ql.Period(5, ql.Years), calc_date + ql.Period(6, ql.Years), calc_date + ql.Period(7, ql.Years), 
                           calc_date + ql.Period(8, ql.Years), calc_date + ql.Period(9, ql.Years), calc_date + ql.Period(10, ql.Years)]
        
        # Make coupons dynamic based on futures price (higher futures price = higher coupons)
        base_coupons = [1.625, 1.75, 1.875, 2.0, 2.125, 2.25]
        futures_price_factor = futures_price / 127.0625  # Normalize to book's base price
        basket_coupons = [coupon * (0.8 + 0.4 * futures_price_factor) for coupon in base_coupons]
        
        # Make prices dynamic based on futures price and time to maturity
        base_prices = [97.921875, 98.546875, 99.375, 100.265625, 101.06250, 100.546875]
        basket_prices = []
        for i, (base_price, maturity) in enumerate(zip(base_prices, basket_maturities)):
            # Adjust price based on futures price and time to maturity
            time_factor = (maturity - calc_date) / 365.0  # Years to maturity
            price_adjustment = (futures_price - 127.0625) * 0.1 * time_factor
            adjusted_price = base_price + price_adjustment
            basket_prices.append(max(90.0, min(110.0, adjusted_price)))  # Keep prices reasonable
        
        basket = [(coupon, maturity, price) for coupon, maturity, price in zip(basket_coupons, basket_maturities, basket_prices)]
        
        min_basis = 100.0
        ctd_bond, ctd_cf, ctd_details = None, None, None
        
        for i, b in enumerate(basket):
            coupon, maturity, price = b
            issue = maturity - ql.Period(10, ql.Years)
            s = create_tsy_security(issue, maturity, coupon / 100.0)
            s.setPricingEngine(ql.DiscountingBondEngine(yield_curve_handle))
            
            cf = ql.BondFunctions.cleanPrice(s, 0.06, day_count, ql.Compounded, ql.Semiannual, calc_date) / 100.0
            adjusted_futures_price = futures_price * cf
            basis = price - adjusted_futures_price
            
            if basis < min_basis:
                min_basis = basis
                ctd_bond = s
                ctd_cf = cf
                # Format maturity date in readable format
                try:
                    # Use ISO format and parse it
                    iso_str = maturity.ISO()
                    year, month, day = iso_str.split('-')
                    day = int(day)
                    month = int(month)
                    year = int(year)
                    
                    month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                                  'July', 'August', 'September', 'October', 'November', 'December']
                    
                    # Add ordinal suffix to day
                    if 10 <= day % 100 <= 20:
                        suffix = 'th'
                    else:
                        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
                    
                    maturity_str = f"{month_names[month]} {day}{suffix}, {year}"
                except:
                    # Fallback to ISO format if formatting fails
                    try:
                        maturity_str = maturity.ISO()
                    except:
                        maturity_str = str(maturity)
                
                ctd_details = {'coupon': coupon, 'maturity': maturity_str, 'price': price, 'basis': min_basis}

        # 5. Final Pricing using CTD
        # Use relative futures maturity date (2 months after evaluation date)
        futures_maturity_date = calc_date + ql.Period(2, ql.Months)
        futures_contract = ql.BondForward(
            calc_date, futures_maturity_date, ql.Position.Long, 0.0, 0,
            day_count, calendar, ql.Following,
            ctd_bond, yield_curve_handle, yield_curve_handle
        )
        
        ctd_price = ql.BondPrice(ctd_details['price'], ql.BondPrice.Clean)
        model_futures_price = futures_contract.cleanForwardPrice() / ctd_cf
        implied_yield = futures_contract.impliedYield(ctd_price.amount()/ctd_cf, futures_price, calc_date, ql.Compounded, day_count).rate()
        z_spread_ctd = ql.BondFunctions.zSpread(ctd_bond, ctd_price, yield_curve, day_count, ql.Compounded, ql.Semiannual, calc_date)
        ytm_ctd = ql.BondFunctions.bondYield(ctd_bond, ctd_price, day_count, ql.Compounded, ql.Semiannual, calc_date)
        
        return {
            'z_spread_fictional': z_spread_fictional,
            'ctd_details': ctd_details,
            'ctd_conversion_factor': ctd_cf,
            'final_pricing': {
                'model_futures_price': model_futures_price,
                'market_futures_price': futures_price,
                'model_adjustment': model_futures_price - futures_price,
                'implied_yield_pct': implied_yield * 100,
                'forward_z_spread_bps': z_spread_ctd * 10000,
                'forward_ytm_pct': ytm_ctd * 100,
            }
        }
    except Exception as e:
        return {'error': str(e)}