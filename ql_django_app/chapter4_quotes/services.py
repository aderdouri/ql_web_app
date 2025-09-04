# chapter4_quotes/services.py

import QuantLib as ql
import numpy as np

price_history = []
def record_price_on_notification(bond):
    global price_history
    try: price_history.append(bond.cleanPrice())
    except Exception: pass

def build_curve_and_get_initial_state(eval_date, bond_prices):
    # ... (le code de cette fonction reste identique, il est déjà correct)
    today = ql.Date(eval_date.day, eval_date.month, eval_date.year)
    ql.Settings.instance().evaluationDate = today
    data = [ (2, 0.02), (4, 0.0225), (6, 0.025), (8, 0.0275), (10, 0.03), (12, 0.0325), (14, 0.035), (16, 0.0375), (18, 0.04), (20, 0.0425), (22, 0.045), (24, 0.0475), (26, 0.05), (28, 0.0525), (30, 0.055)]
    calendar = ql.TARGET()
    settlement = calendar.advance(today, 3, ql.Days)
    quotes = [ql.SimpleQuote(price) for price in bond_prices]
    helpers = []
    for i, (length, coupon) in enumerate(data):
        maturity = calendar.advance(settlement, length, ql.Years)
        schedule = ql.Schedule(settlement, maturity, ql.Period(ql.Annual), calendar, ql.ModifiedFollowing, ql.ModifiedFollowing, ql.DateGeneration.Backward, False)
        helpers.append(ql.FixedRateBondHelper(ql.QuoteHandle(quotes[i]), 3, 100.0, schedule, [coupon], ql.SimpleDayCounter(), ql.ModifiedFollowing))
    curve = ql.FittedBondDiscountCurve(0, calendar, helpers, ql.SimpleDayCounter(), ql.NelsonSiegelFitting())
    curve_handle = ql.YieldTermStructureHandle(curve)
    bond_schedule = ql.Schedule(today, calendar.advance(today, 15, ql.Years), ql.Period(ql.Semiannual), calendar, ql.ModifiedFollowing, ql.ModifiedFollowing, ql.DateGeneration.Backward, False)
    benchmark_bond = ql.FixedRateBond(3, 100.0, bond_schedule, [0.04], ql.Actual360())
    benchmark_bond.setPricingEngine(ql.DiscountingBondEngine(curve_handle))
    return quotes, benchmark_bond, curve

def run_simulation_optimised(quotes, bond, new_price, simulation_type):
    global price_history
    price_history = []
    try:
        for q in quotes:
            q.setValue(100.0)
        
        if simulation_type == 'naive':
            price_history.append(bond.cleanPrice())
            observer = ql.Observer(lambda: record_price_on_notification(bond))
            observer.registerWith(bond)
            for q in quotes:
                q.setValue(float(new_price))
            observer.unregisterWith(bond)
            unique_prices = price_history[::2] + price_history[-1:] if price_history else []
            return {'update_chart_data': unique_prices}
            
        elif simulation_type == 'pull':
            for q in quotes:
                q.setValue(float(new_price))
            final_price = bond.cleanPrice()
            return {'final_price': final_price}
    except Exception as e:
        return {'error': str(e)}