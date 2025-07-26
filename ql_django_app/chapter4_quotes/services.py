import QuantLib as ql
import numpy as np

bond_instrument = None
rate_quote = None

def setup_bond_and_market(coupon_rate_pct, maturity_years):
    """
    Creates and stores a bond and its underlying market rate quote.
    This function is called once to set up the lab.
    """
    global bond_instrument, rate_quote
    
    # 1. Market and Calculation Setup
    calculation_date = ql.Date(15, 1, 2016)
    ql.Settings.instance().evaluationDate = calculation_date
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    day_count = ql.Actual365Fixed()

    # 2. The Market Quote
    # This is the object we will change interactively.
    initial_rate = 0.02 # 2%
    rate_quote = ql.SimpleQuote(initial_rate)
    rate_handle = ql.QuoteHandle(rate_quote)
    
    # The yield curve is linked to the quote via the handle
    yield_curve = ql.YieldTermStructureHandle(
        ql.FlatForward(calculation_date, rate_handle, day_count)
    )

    # 3. The Instrument (a simple fixed-rate bond)
    settlement_days = 2
    face_amount = 100.0
    coupon_rate = coupon_rate_pct / 100
    
    issue_date = calculation_date
    maturity_date = calendar.advance(issue_date, ql.Period(maturity_years, ql.Years))
    
    schedule = ql.Schedule(
        issue_date, maturity_date, ql.Period('6M'), calendar,
        ql.ModifiedFollowing, ql.ModifiedFollowing, ql.DateGeneration.Forward, False
    )
    
    bond_instrument = ql.FixedRateBond(
        settlement_days, face_amount, schedule, [coupon_rate], day_count
    )
    
    # 4. The Pricing Engine
    # The engine is linked to the yield curve, which is linked to the quote.
    bond_engine = ql.DiscountingBondEngine(yield_curve)
    bond_instrument.setPricingEngine(bond_engine)
    
    # Return the initial state
    return {
        'initial_price': np.round(bond_instrument.cleanPrice(), 4),
        'initial_rate': initial_rate * 100
    }

def update_market_and_reprice(new_rate_pct):
    """
    Updates the market quote and returns the new bond price.
    This demonstrates the Observer pattern.
    """
    global bond_instrument, rate_quote
    
    if rate_quote is None or bond_instrument is None:
        return {'error': 'Bond and market not set up yet.'}
        
    # 1. UPDATE THE MARKET: This is the only action needed.
    rate_quote.setValue(new_rate_pct / 100)
    
    # 2. GET THE NEW PRICE: The bond reprices itself automatically
    # because it is "observing" the quote through the engine and curve.
    return {
        'new_price': np.round(bond_instrument.cleanPrice(), 4),
        'new_rate': new_rate_pct
    }