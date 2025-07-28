import QuantLib as ql
from datetime import date
import numpy as np

def build_spreaded_curve(spread_bps: float, evaluation_dt: date):
    """
    Builds a base curve for a given evaluation date and derives a new curve 
    by adding a user-defined spread. Corrected to stay within curve bounds.
    """
    
    # 1. Set up evaluation date and market conventions
    today = ql.Date(evaluation_dt.day, evaluation_dt.month, evaluation_dt.year)
    ql.Settings.instance().evaluationDate = today
    
    # 2. Build the base (risk-free) curve
    # The nodes define the maximum date of the curve (today + 20 years)
    nodes = [today + ql.Period(i, ql.Years) for i in [0, 1, 3, 5, 10, 20]]
    rates = [0.01, 0.015, 0.02, 0.022, 0.025, 0.028]
    
    base_curve = ql.ZeroCurve(nodes, rates, ql.Actual365Fixed())
    base_curve_handle = ql.YieldTermStructureHandle(base_curve)
    
    # 3. Create the spreaded (corporate) curve
    spread = spread_bps / 10000.0 # Convert basis points to a decimal value
    spread_quote = ql.QuoteHandle(ql.SimpleQuote(spread))
    
    spreaded_curve = ql.ZeroSpreadedTermStructure(base_curve_handle, spread_quote)
    spreaded_curve.enableExtrapolation() # Enable extrapolation for stability

    # 4. Extract points from both curves for plotting
    plot_points = {'base': [], 'spreaded': []}
    calendar = ql.TARGET()
    max_years = 20
    
    for m in range(0, max_years * 12):
        d = calendar.advance(today, ql.Period(m, ql.Months))
        
        try:
            # We add a safety check, although the corrected loop should prevent errors.
            if d < base_curve.maxDate():
                rate_base = base_curve.zeroRate(d, ql.Actual365Fixed(), ql.Compounded).rate() * 100
                plot_points['base'].append({'x': d.ISO(), 'y': round(rate_base, 4)})
                
                rate_spreaded = spreaded_curve.zeroRate(d, ql.Actual365Fixed(), ql.Compounded).rate() * 100
                plot_points['spreaded'].append({'x': d.ISO(), 'y': round(rate_spreaded, 4)})
        except Exception as e:
            print(f"Could not get rate for date {d}: {e}")
            
    return plot_points