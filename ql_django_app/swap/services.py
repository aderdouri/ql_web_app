# File: ql_web_app/swap/services.py
import QuantLib as ql
import numpy as np

def calculate_vanilla_swap_metrics(
    notional: float,
    maturity_years: int,
    fixed_rate_pct: float,
    floating_spread_bps: float,
    discount_curve_rate_pct: float
) -> dict:
    
    # 1. Setup and parameter conversion
    today = ql.Date.todaysDate()
    ql.Settings.instance().evaluationDate = today
    
    fixed_rate = fixed_rate_pct / 100.0
    floating_spread = floating_spread_bps / 10000.0 # Convert bps to decimal
    discount_rate = discount_curve_rate_pct / 100.0

    # 2. Build the yield curve and index
    day_count = ql.Actual365Fixed()
    discount_curve = ql.YieldTermStructureHandle(
        ql.FlatForward(today, discount_rate, day_count)
    )
    # For simplicity, we use the same curve for forecasting
    forecast_curve = ql.YieldTermStructureHandle(
        ql.FlatForward(today, discount_rate, day_count)
    )
    libor_index = ql.Euribor6M(forecast_curve)

    # 3. Create the instrument schedules
    calendar = ql.TARGET()
    settle_date = calendar.advance(today, ql.Period('2D'))
    maturity_date = calendar.advance(settle_date, ql.Period(maturity_years, ql.Years))

    fixed_schedule = ql.Schedule(
        settle_date, maturity_date, ql.Period('1Y'), calendar,
        ql.Unadjusted, ql.Unadjusted, ql.DateGeneration.Forward, False
    )
    float_schedule = ql.Schedule(
        settle_date, maturity_date, ql.Period('6M'), calendar,
        ql.ModifiedFollowing, ql.ModifiedFollowing, ql.DateGeneration.Forward, False
    )
    
    # 4. Create the Interest Rate Swap instrument
    # We use the 'notional' provided by the user here
    vanilla_swap = ql.VanillaSwap(
        ql.VanillaSwap.Payer, 
        notional,
        fixed_schedule, 
        fixed_rate, 
        ql.Thirty360(ql.Thirty360.BondBasis),
        float_schedule, 
        libor_index, 
        floating_spread, 
        libor_index.dayCounter()
    )

    # 5. Set the pricing engine
    swap_engine = ql.DiscountingSwapEngine(discount_curve)
    vanilla_swap.setPricingEngine(swap_engine)

    # 6. Calculate and return all relevant metrics
    results = {
        'npv': np.round(vanilla_swap.NPV(), 2),
        'fair_rate': np.round(vanilla_swap.fairRate() * 100, 4), # in %
        'fair_spread': np.round(vanilla_swap.fairSpread() * 10000, 2), # in bps
        'fixed_leg_npv': np.round(vanilla_swap.fixedLegNPV(), 2),
        'floating_leg_npv': np.round(vanilla_swap.floatingLegNPV(), 2),
    }
    return results