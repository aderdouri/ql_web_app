# File: ql_web_app/chapter4_quotes/services.py
import QuantLib as ql
import numpy as np

def build_ns_curve_and_price_bond(ns_params: dict, bond_params: dict):
    """
    Builds a Nelson-Siegel yield curve from user parameters and prices a bond with it.
    """
    today = ql.Date(15, 1, 2015)
    ql.Settings.instance().evaluationDate = today
    day_count = ql.Actual365Fixed()
    calendar = ql.TARGET()

    # 1. Build the Nelson-Siegel curve with user parameters
    ns_curve = ql.NelsonSiegel(
        today,
        ns_params['beta0'],
        ns_params['beta1'],
        ns_params['beta2'],
        ns_params['tau'],
        day_count
    )
    ns_handle = ql.YieldTermStructureHandle(ns_curve)

    # 2. Extract points from the curve for the plot
    plot_points = []
    max_years = 30
    for yrs in np.arange(0, max_years + 0.25, 0.25):
        d = calendar.advance(today, ql.Period(int(yrs * 12), ql.Months))
        rate = ns_curve.zeroRate(d, day_count, ql.Compounded).rate() * 100
        plot_points.append({'x': yrs, 'y': round(rate, 4)})
        
    # 3. Build and price the bond
    bond_maturity = bond_params['bond_maturity_years']
    bond_coupon = bond_params['bond_coupon_rate'] / 100.0
    
    maturity_date = calendar.advance(today, ql.Period(bond_maturity, ql.Years))
    schedule = ql.Schedule(today, maturity_date, ql.Period(ql.Semiannual), calendar,
                           ql.Unadjusted, ql.Unadjusted, ql.DateGeneration.Backward, False)
    
    bond_to_price = ql.FixedRateBond(2, 100.0, schedule, [bond_coupon], day_count)
    
    engine = ql.DiscountingBondEngine(ns_handle)
    bond_to_price.setPricingEngine(engine)
    
    return {
        'bond_price': f"{bond_to_price.cleanPrice():.4f}",
        'plot_points': plot_points
    }