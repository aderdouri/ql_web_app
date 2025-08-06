import QuantLib as ql
import numpy as np

def calculate_vanilla_swap_metrics(
    notional: float, maturity_years: int, fixed_rate_pct: float, 
    float_spread_bps: float, curve_rate_pct: float
):
    today = ql.Date(15, 1, 2016)
    ql.Settings.instance().evaluationDate = today
    
    fixed_rate = fixed_rate_pct / 100.0
    float_spread = float_spread_bps / 10000.0
    curve_rate = curve_rate_pct / 100.0

    day_count = ql.Actual365Fixed()
    discount_curve = ql.YieldTermStructureHandle(ql.FlatForward(today, curve_rate, day_count))
    
    calendar = ql.TARGET()
    settle_date = calendar.advance(today, ql.Period('2D'))
    maturity_date = calendar.advance(settle_date, ql.Period(maturity_years, ql.Years))

    fixed_schedule = ql.Schedule(settle_date, maturity_date, ql.Period('6M'), calendar, ql.ModifiedFollowing, ql.ModifiedFollowing, ql.DateGeneration.Forward, False)
    float_schedule = ql.Schedule(settle_date, maturity_date, ql.Period('3M'), calendar, ql.ModifiedFollowing, ql.ModifiedFollowing, ql.DateGeneration.Forward, False)
    
    libor_index = ql.USDLibor(ql.Period('3M'), discount_curve)

    vanilla_swap = ql.VanillaSwap(
        ql.VanillaSwap.Payer, notional,
        fixed_schedule, fixed_rate, ql.Thirty360(ql.Thirty360.BondBasis),
        float_schedule, libor_index, float_spread, ql.Actual360()
    )

    swap_engine = ql.DiscountingSwapEngine(discount_curve)
    vanilla_swap.setPricingEngine(swap_engine)

    return {
        'npv': round(vanilla_swap.NPV(), 4),
        'fair_rate': round(vanilla_swap.fairRate() * 100, 4),
        'fair_spread': round(vanilla_swap.fairSpread() * 10000, 2),
    }