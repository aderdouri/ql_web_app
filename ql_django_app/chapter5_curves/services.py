import QuantLib as ql
from datetime import date
import numpy as np

def build_and_analyze_curves(evaluation_dt: date, interpolation_str: str):
    eval_date = ql.Date(evaluation_dt.day, evaluation_dt.month, evaluation_dt.year)
    ql.Settings.instance().evaluationDate = eval_date
    
    # 1. Données de marché (du premier notebook)
    depo_rates = [5.25, 5.5]
    bond_rates = [5.75, 6.0, 6.25, 6.5, 6.75, 6.80, 7.00, 7.1, 7.15, 7.2, 7.3, 7.35, 7.4, 7.5, 7.6, 7.6, 7.7, 7.8]
    depo_maturities = [ql.Period(6, ql.Months), ql.Period(12, ql.Months)]
    bond_maturities = [ql.Period(6*i, ql.Months) for i in range(3, 21)]

    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    day_count = ql.Thirty360(ql.Thirty360.BondBasis)
    
    depo_helpers = [ql.DepositRateHelper(r/100, m, 0, calendar, ql.Unadjusted, True, day_count) for r, m in zip(depo_rates, depo_maturities)]
    bond_helpers = []
    for r, m in zip(bond_rates, bond_maturities):
        schedule = ql.Schedule(eval_date, eval_date+m, ql.Period(ql.Semiannual), calendar, ql.Unadjusted, ql.Unadjusted, ql.DateGeneration.Backward, True)
        bond_helpers.append(ql.FixedRateBondHelper(ql.QuoteHandle(ql.SimpleQuote(100)), 0, 100, schedule, [r/100], day_count, ql.Unadjusted))
    rate_helpers = depo_helpers + bond_helpers

    # 2. Construction de la courbe RELATIVE avec l'interpolation choisie
    relative_curve = None
    if interpolation_str == 'log_cubic':
        relative_curve = ql.PiecewiseLogCubicDiscount(eval_date, rate_helpers, day_count)
    elif interpolation_str == 'linear_zero':
        relative_curve = ql.PiecewiseLinearZero(eval_date, rate_helpers, day_count)
    elif interpolation_str == 'cubic_zero':
        relative_curve = ql.PiecewiseCubicZero(eval_date, rate_helpers, day_count)
    else: # flat_forward
        relative_curve = ql.PiecewiseFlatForward(eval_date, rate_helpers, day_count)
    relative_curve.enableExtrapolation()

    # 3. Construction de la courbe ABSOLUE (figée)
    dates, rates = zip(*relative_curve.nodes())
    absolute_curve = ql.ForwardCurve(dates, rates, day_count)
    absolute_curve.enableExtrapolation()

    # 4. Extraction des points pour les graphiques
    plot_points = {'relative': [], 'absolute': []}
    max_years = 10
    for m in range(0, max_years * 12 + 1):
        d = calendar.advance(eval_date, ql.Period(m, ql.Months))
        yrs = day_count.yearFraction(eval_date, d)
        
        rate_rel = relative_curve.zeroRate(yrs, ql.Compounded).rate() * 100
        plot_points['relative'].append({'x': d.ISO(), 'y': round(rate_rel, 4)})
        
        # Pour la courbe absolue, on doit utiliser la date, pas la durée
        if d <= absolute_curve.maxDate():
            rate_abs = absolute_curve.zeroRate(d, day_count, ql.Compounded).rate() * 100
            plot_points['absolute'].append({'x': d.ISO(), 'y': round(rate_abs, 4)})
            
    return plot_points