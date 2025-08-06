import QuantLib as ql
import numpy as np

def build_base_swap_and_curve():
    """
    Creates the base environment: a vanilla swap and its initial yield curve.
    Returns the swap, the base curve, and a relinkable handle to the curve.
    """
    today = ql.Date(8, ql.March, 2016)
    ql.Settings.instance().evaluationDate = today
    
    # --- 1. Build the initial yield curve from market data ---
    helpers = []
    # Simplified market data from the notebook
    for rate, tenor in [(0.424, 3), (0.762, 5), (1.584, 10), (2.037, 15), (2.187, 20), (2.256, 30)]:
        helpers.append(
            ql.SwapRateHelper(
                ql.QuoteHandle(ql.SimpleQuote(rate / 100)),
                ql.Period(tenor, ql.Years),
                ql.TARGET(),
                ql.Annual,
                ql.Unadjusted,
                ql.Thirty360(ql.Thirty360.BondBasis),
                ql.Euribor6M()
            )
        )
    
    rate_curve = ql.PiecewiseLogCubicDiscount(2, ql.TARGET(), helpers, ql.Actual365Fixed())
    
    # --- 2. Create a RELINKABLE handle to this curve ---
    # This is the key object that allows for dynamic curve switching.
    curve_handle = ql.RelinkableYieldTermStructureHandle(rate_curve)
    
    # --- 3. Build the swap, linking its index to the relinkable handle ---
    fixed_schedule = ql.Schedule(ql.Date(8, 4, 2016), ql.Date(8, 4, 2028), ql.Period(1, ql.Years), ql.TARGET(), ql.Following, ql.Following, ql.DateGeneration.Forward, False)
    floating_schedule = ql.Schedule(ql.Date(8, 4, 2016), ql.Date(8, 4, 2028), ql.Period(6, ql.Months), ql.TARGET(), ql.Following, ql.Following, ql.DateGeneration.Forward, False)
    
    swap = ql.VanillaSwap(
        ql.VanillaSwap.Payer, 10000.0,
        fixed_schedule, 0.02, ql.Thirty360(ql.Thirty360.BondBasis),
        floating_schedule, ql.Euribor6M(curve_handle), 0.0, ql.Actual360()
    )
    swap.setPricingEngine(ql.DiscountingSwapEngine(curve_handle))
    
    return swap, rate_curve, curve_handle


def analyze_sensitivity(shock_type: str, shock_size_bps: float):
    """
    Analyzes the sensitivity of a swap's NPV to a specified yield curve shock.
    """
    # 1. Get the base setup
    swap, base_curve, curve_handle = build_base_swap_and_curve()
    
    # 2. Price with the base curve
    base_price = swap.NPV()
    
    # 3. Create the shocked curve based on user's choice
    shocked_curve = None
    base_curve_handle = ql.YieldTermStructureHandle(base_curve) # Simple handle for the base curve

    if shock_type == 'parallel':
        spread_quote = ql.QuoteHandle(ql.SimpleQuote(shock_size_bps / 10000.0))
        shocked_curve = ql.ZeroSpreadedTermStructure(base_curve_handle, spread_quote)
    elif shock_type == 'tilt':
        spot_date = base_curve.referenceDate()
        dates = [spot_date + ql.Period(n, ql.Years) for n in range(21)]
        # Tilt: spread increases/decreases linearly with maturity around a pivot point (10 years)
        spread_quotes = [ql.QuoteHandle(ql.SimpleQuote((n - 10) * shock_size_bps / 10000.0)) for n in range(21)]
        shocked_curve = ql.SpreadedLinearZeroInterpolatedTermStructure(base_curve_handle, spread_quotes, dates)
    
    # 4. Link the relinkable handle to the new shocked curve
    # The swap is "observing" this handle and will reprice automatically.
    if shocked_curve:
        curve_handle.linkTo(shocked_curve)
    
    # 5. Get the new price
    shocked_price = swap.NPV()
    
    # 6. Prepare data for plotting
    plot_points = {'base': [], 'shocked': []}
    times = np.linspace(0.0, 15.0, 100)
    
    # The handle now points to the shocked curve, so we can use it for plotting
    shocked_curve_for_plot = curve_handle.currentLink()
    
    for t in times:
        plot_points['base'].append({'x': t, 'y': base_curve.zeroRate(t, ql.Continuous).rate() * 100})
        plot_points['shocked'].append({'x': t, 'y': shocked_curve_for_plot.zeroRate(t, ql.Continuous).rate() * 100})
        
    return {
        'base_price': round(base_price, 4),
        'shocked_price': round(shocked_price, 4),
        'sensitivity': round(shocked_price - base_price, 4),
        'plot_points': plot_points
    }