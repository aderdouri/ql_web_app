import QuantLib as ql
import numpy as np
from datetime import date 

def calculate_vanilla_swap_metrics(
    notional: float,
    maturity_years: int,
    fixed_rate_pct: float,
    floating_spread_bps: float,
    risk_free_rate_pct: float,
    libor_rate_pct: float,
    evaluation_date=None
) -> dict:
    
    # 1. Setup and parameter conversion - using dynamic date for interactive experience
    if evaluation_date is None:
        evaluation_date = date.today()
    
    calculation_date = ql.Date(evaluation_date.day, evaluation_date.month, evaluation_date.year)
    ql.Settings.instance().evaluationDate = calculation_date
    
    fixed_rate = fixed_rate_pct / 100.0
    floating_spread = floating_spread_bps / 10000.0
    risk_free_rate = risk_free_rate_pct / 100.0
    libor_rate = libor_rate_pct / 100.0

    # 2. Build the yield curve and index - exactly as in the book
    day_count = ql.Actual365Fixed()
    discount_curve = ql.YieldTermStructureHandle(
        ql.FlatForward(calculation_date, risk_free_rate, day_count)
    )
    libor_curve = ql.YieldTermStructureHandle(
        ql.FlatForward(calculation_date, libor_rate, day_count)
    )
    libor3M_index = ql.USDLibor(ql.Period(3, ql.Months), libor_curve)

    # 3. Create the instrument schedules - exactly as in the book
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    settle_date = calendar.advance(calculation_date, 5, ql.Days)
    maturity_date = calendar.advance(settle_date, maturity_years, ql.Years)
    
    # Fixed leg: 6 months (semiannual)
    fixed_leg_tenor = ql.Period(6, ql.Months)
    fixed_schedule = ql.Schedule(
        settle_date, maturity_date, fixed_leg_tenor, calendar,
        ql.ModifiedFollowing, ql.ModifiedFollowing, ql.DateGeneration.Forward, False
    )
    
    # Floating leg: 3 months (quarterly)
    float_leg_tenor = ql.Period(3, ql.Months)
    float_schedule = ql.Schedule(
        settle_date, maturity_date, float_leg_tenor, calendar,
        ql.ModifiedFollowing, ql.ModifiedFollowing, ql.DateGeneration.Forward, False
    )
    
    # 4. Create the Interest Rate Swap instrument - exactly as in the book
    fixed_leg_daycount = ql.Actual360()
    float_leg_daycount = ql.Actual360()
    
    ir_swap = ql.VanillaSwap(
        ql.VanillaSwap.Payer, 
        notional, 
        fixed_schedule,
        fixed_rate, 
        fixed_leg_daycount, 
        float_schedule,
        libor3M_index, 
        floating_spread, 
        float_leg_daycount
    )

    # 5. Set the pricing engine
    swap_engine = ql.DiscountingSwapEngine(discount_curve)
    ir_swap.setPricingEngine(swap_engine)

    # 6. Extract cash flows for both legs
    fixed_leg_cash_flows = []
    for cf in ir_swap.leg(0):
        fixed_leg_cash_flows.append({
            'date': cf.date().to_date(),
            'amount': round(cf.amount(), 6)
        })
    
    floating_leg_cash_flows = []
    for cf in ir_swap.leg(1):
        floating_leg_cash_flows.append({
            'date': cf.date().to_date(),
            'amount': round(cf.amount(), 6)
        })

    # 7. Calculate and return all relevant metrics - exactly as in the book
    results = {
        'npv': round(ir_swap.NPV(), 3),
        'fair_rate': round(ir_swap.fairRate(), 3),
        'fair_spread': round(ir_swap.fairSpread(), 3),
        'fixed_leg_bps': round(ir_swap.fixedLegBPS(), 3),
        'floating_leg_bps': round(ir_swap.floatingLegBPS(), 3),
        'fixed_leg_npv': round(ir_swap.fixedLegNPV(), 2),
        'floating_leg_npv': round(ir_swap.floatingLegNPV(), 2),
        'fixed_leg_cash_flows': fixed_leg_cash_flows,
        'floating_leg_cash_flows': floating_leg_cash_flows,
    }
    return results