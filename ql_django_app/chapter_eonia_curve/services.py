import QuantLib as ql
from datetime import date
import numpy as np

def build_eonia_curve(interpolation_type: str, include_jump: bool, evaluation_dt, simulation_duration_years):
    """
    Builds an EONIA yield curve using different interpolations and potentially
    including a turn-of-year jump, handling potential numerical errors gracefully.
    """
    eval_date = ql.Date(evaluation_dt.day, evaluation_dt.month, evaluation_dt.year)
    ql.Settings.instance().evaluationDate = eval_date
    
    # --- Market Data (from the Cookbook example) ---
    deposits = {
        (1, ql.Days): 0.0013, (1, ql.Weeks): 0.0017, (2, ql.Weeks): 0.0018,
        (1, ql.Months): 0.0020, (2, ql.Months): 0.0023, (3, ql.Months): 0.0026,
        (4, ql.Months): 0.0028, (5, ql.Months): 0.0031, (6, ql.Months): 0.0034
    }
    ois_swaps = {
        (1, ql.Years): 0.0007, (2, ql.Years): 0.0012, (3, ql.Years): 0.0021,
        (5, ql.Years): 0.0059, (10, ql.Years): 0.0113, (15, ql.Years): 0.0152,
        (20, ql.Years): 0.01939, (25, ql.Years): 0.02003, (30, ql.Years): 0.02038
    }

    # --- Setup ---
    calendar = ql.TARGET()
    day_count = ql.Actual365Fixed()
    settlement_days = 2
    eonia_index = ql.Eonia()

    # --- Create Rate Helpers ---
    # The variable is correctly named 'rate_helpers'
    rate_helpers = []
    
    # 1. For short-term deposits
    for period, rate in deposits.items():
        tenor = ql.Period(period[0], period[1])
        helper = ql.DepositRateHelper(ql.QuoteHandle(ql.SimpleQuote(rate/100)), tenor, settlement_days, calendar, ql.ModifiedFollowing, False, day_count)
        rate_helpers.append(helper)
        
    # 2. For OIS swaps
    for period, rate in ois_swaps.items():
        tenor = ql.Period(period[0], period[1])
        helper = ql.OISRateHelper(settlement_days, tenor, ql.QuoteHandle(ql.SimpleQuote(rate/100)), eonia_index)
        rate_helpers.append(helper)

    # --- Handle the optional Turn-of-Year jump ---
    jumps, jump_dates = [], []
    if include_jump:
        B = 1.0 / (1.0 + 0.0030 * (ql.Date(2,1,2013)-ql.Date(31,12,2012))/360.0)
        jumps = [ql.QuoteHandle(ql.SimpleQuote(B))]
        jump_dates = [ql.Date(31, ql.December, 2012)]

    # --- Build the Curve ---
    eonia_curve = None
    try:
       
        if interpolation_type == 'log_cubic':
            eonia_curve = ql.PiecewiseLogCubicDiscount(0, calendar, rate_helpers, day_count, jumps, jump_dates)
        elif interpolation_type == 'flat_forward':
            eonia_curve = ql.PiecewiseFlatForward(0, calendar, rate_helpers, day_count, jumps, jump_dates)
        else:
            eonia_curve = ql.PiecewiseLinearZero(0, calendar, rate_helpers, day_count, jumps, jump_dates)

        eonia_curve.enableExtrapolation()
    except Exception as e:
        print(f"FATAL: Curve construction failed on {eval_date}: {e}")
        return {'error': f"Curve construction failed: {e}", 'plot_points': []}

    # --- Extract Points for Plotting ---
    plot_points = []
    max_years = min(simulation_duration_years, 30)
    
    for m in range(0, max_years * 12 + 1):
        d = calendar.advance(eval_date, ql.Period(m, ql.Months))
        try:
            rate = eonia_curve.zeroRate(d, day_count, ql.Compounded).rate() * 100
            plot_points.append({'x': d.ISO(), 'y': round(rate, 4)})
        except Exception as e:
            print(f"Could not get zero rate for date {d}, stopping plot generation. Error: {e}")
            break
            
    return plot_points