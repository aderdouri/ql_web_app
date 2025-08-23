import QuantLib as ql
from datetime import date

def analyze_cap_floor_parity(length_years, strike_pct, vol_pct, rate_pct, nominal):
    today = ql.Date(6, 8, 2025)
    ql.Settings.instance().evaluationDate = today
    
    strike = strike_pct / 100.0
    vol = vol_pct / 100.0
    rate = rate_pct / 100.0
    
    calendar = ql.TARGET()
    settlement_days = 2
    settlement_date = calendar.advance(today, settlement_days, ql.Days)
    term_structure = ql.YieldTermStructureHandle(ql.FlatForward(settlement_date, rate, ql.Actual360()))
    vol_handle = ql.OptionletVolatilityStructureHandle(
        ql.ConstantOptionletVolatility(settlement_days, calendar, ql.ModifiedFollowing, vol, ql.Actual365Fixed())
    )
    
    engine = ql.BlackCapFloorEngine(term_structure, vol_handle)
    
    maturity_date = settlement_date + ql.Period(length_years, ql.Years)
    tenor = ql.Period(ql.Semiannual)
    
    schedule = ql.Schedule(
        settlement_date, maturity_date, tenor, calendar,
        ql.ModifiedFollowing, ql.ModifiedFollowing, ql.DateGeneration.Forward, False
    )

    index = ql.Euribor6M(term_structure)
    leg = ql.IborLeg([nominal], schedule, index)

    cap = ql.Cap(leg, [strike])
    cap.setPricingEngine(engine)
    cap_npv = cap.NPV()

    floor = ql.Floor(leg, [strike])
    floor.setPricingEngine(engine)
    floor_npv = floor.NPV()
    
    collar = ql.Collar(leg, [strike], [strike])
    collar.setPricingEngine(engine)
    collar_npv = collar.NPV()
    
    swap = ql.VanillaSwap(
        ql.VanillaSwap.Payer, nominal,
        schedule, strike, ql.Thirty360(ql.Thirty360.BondBasis),
        schedule, index, 0.0, index.dayCounter()
    )
    swap.setPricingEngine(ql.DiscountingSwapEngine(term_structure))
    swap_npv = swap.NPV()
    
    collar_parity_check = (cap_npv - floor_npv) - collar_npv
    swap_parity_check = (cap_npv - floor_npv) - swap_npv
    
    return {
        'cap_npv': round(cap_npv, 2),
        'floor_npv': round(floor_npv, 2),
        'collar_npv': round(collar_npv, 2),
        'swap_npv': round(swap_npv, 2),
        'collar_parity_diff': round(collar_parity_check, 2),
        'swap_parity_diff': round(swap_parity_check, 2)
    }