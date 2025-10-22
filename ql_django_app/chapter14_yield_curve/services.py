import QuantLib as ql
from datetime import date

def build_treasury_curve(evaluation_dt: date, interpolation_str: str, market_rates: dict):
    """
    Builds a Treasury yield curve using market rates and parameters provided by the user.
    """
    eval_date = ql.Date(evaluation_dt.day, evaluation_dt.month, evaluation_dt.year)
    ql.Settings.instance().evaluationDate = eval_date
    
    # 1. Use the market rates from the form
    deposits_data = {
        ql.Period(6, ql.Months): market_rates['depo_6m_rate'] / 100.0,
    }
    bonds_data = {
        ql.Period(2, ql.Years): market_rates['bond_2y_rate'] / 100.0,
        ql.Period(5, ql.Years): market_rates['bond_5y_rate'] / 100.0,
        ql.Period(10, ql.Years): market_rates['bond_10y_rate'] / 100.0,
    }

    # 2. General parameters
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    day_count = ql.Actual365Fixed()
    settlement_days = 2
    
    # 3. Create Rate Helpers from the dynamic market data
    rate_helpers = []
    
    # Deposit helpers
    for tenor, rate in deposits_data.items():
        helper = ql.DepositRateHelper(ql.QuoteHandle(ql.SimpleQuote(rate)), tenor, settlement_days, calendar, ql.ModifiedFollowing, False, day_count)
        rate_helpers.append(helper)
        
    # Bond helpers
    for tenor, coupon_rate in bonds_data.items():
        maturity = calendar.advance(eval_date, tenor)
        schedule = ql.Schedule(eval_date, maturity, ql.Period(ql.Semiannual), calendar, ql.Unadjusted, ql.Unadjusted, ql.DateGeneration.Backward, False)
        helper = ql.FixedRateBondHelper(ql.QuoteHandle(ql.SimpleQuote(100.0)), settlement_days, 100.0, schedule, [coupon_rate], day_count, ql.Unadjusted)
        rate_helpers.append(helper)

    # 4. Build the curve with the user's chosen interpolation
    yield_curve = None
    if interpolation_str == 'log_cubic':
        yield_curve = ql.PiecewiseLogCubicDiscount(eval_date, rate_helpers, day_count)
    elif interpolation_str == 'linear_zero':
        yield_curve = ql.PiecewiseLinearZero(eval_date, rate_helpers, day_count)
    elif interpolation_str == 'cubic_zero':
        yield_curve = ql.PiecewiseCubicZero(eval_date, rate_helpers, day_count)
    else: # flat_forward
        yield_curve = ql.PiecewiseFlatForward(eval_date, rate_helpers, day_count)
    
    yield_curve.enableExtrapolation()

    # 5. Extract points for plotting
    plot_points = []
    max_years = 10
    for m in range(1, max_years * 12 + 1):
        yrs = m / 12.0
        d = calendar.advance(eval_date, ql.Period(m, ql.Months))
        try:
            rate = yield_curve.zeroRate(yrs, ql.Compounded, ql.Semiannual).rate() * 100
            plot_points.append({'x': d.ISO(), 'y': round(rate, 4)})
        except Exception:
            pass # Ignore points where the curve might be unstable
            
    return plot_points