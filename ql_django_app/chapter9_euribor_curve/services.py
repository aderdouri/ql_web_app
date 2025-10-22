import QuantLib as ql
from datetime import date
import numpy as np

def build_euribor_curves(base_spread_bps: float, evaluation_dt: date, simulation_duration_years: int):
    """
    Construit deux courbes Euribor 6M (naïve et améliorée) pour une date d'évaluation
    et une durée de simulation données par l'utilisateur.
    """
    
    # On utilise la date choisie par l'utilisateur comme point de départ
    today = ql.Date(evaluation_dt.day, evaluation_dt.month, evaluation_dt.year)
    ql.Settings.instance().evaluationDate = today
    
    # --- 1. Construction de la courbe de discount Eonia (robuste) ---
    # Les données de marché sont fixes, mais la courbe est construite "aujourd'hui"
    eonia_helpers = [
        ql.DepositRateHelper(ql.QuoteHandle(ql.SimpleQuote(rate/100)), ql.Period(1,ql.Days), fixingDays, ql.TARGET(), ql.Following, False, ql.Actual360())
        for rate, fixingDays in [(0.04, 0), (0.04, 1), (0.04, 2)]
    ]
    eonia = ql.Eonia()
    eonia_helpers += [
        ql.OISRateHelper(2, ql.Period(*tenor), ql.QuoteHandle(ql.SimpleQuote(rate/100)), eonia)
        for rate, tenor in [(0.070, (1,ql.Weeks)), (0.069, (2,ql.Weeks)), (0.078, (3,ql.Weeks)), (0.074, (1,ql.Months))]
    ]
    # NOTE: Les DatedOISRateHelper ont des dates absolues. Pour une simulation réaliste,
    # il faudrait une base de données de marché. Ici, nous les gardons pour la stabilité.
    eonia_helpers += [
        ql.DatedOISRateHelper(ql.Date(16,1,2013), ql.Date(13,2,2013), ql.QuoteHandle(ql.SimpleQuote(0.046/100)), eonia)
    ]
    eonia_curve = ql.PiecewiseLinearZero(today, eonia_helpers, ql.Actual365Fixed())
    discount_handle = ql.YieldTermStructureHandle(eonia_curve)

    # --- 2. Construction de la courbe Euribor 6M "naïve" ---
    euribor6m = ql.Euribor6M(discount_handle)
    helpers_naive = [ql.DepositRateHelper(ql.QuoteHandle(ql.SimpleQuote(0.312/100)), ql.Period(6,ql.Months), 2, ql.TARGET(), ql.Following, False, ql.Actual360())]
    helpers_naive += [
        ql.SwapRateHelper(ql.QuoteHandle(ql.SimpleQuote(rate/100)), ql.Period(tenor, ql.Years), ql.TARGET(), ql.Annual, ql.Unadjusted, ql.Thirty360(ql.Thirty360.BondBasis), euribor6m, ql.QuoteHandle(), ql.Period(0, ql.Days))
        for rate, tenor in [(0.424, 3), (0.762, 5), (1.584, 10), (2.187, 20), (2.256, 30)]
    ]
    euribor_curve_naive = ql.PiecewiseLinearZero(today, helpers_naive, ql.Actual365Fixed())

    # --- 3. Construction des helpers synthétiques (interactifs) ---
    alpha = base_spread_bps / 10000.0
    
    synth_helpers = []
    for n, units in [(1, ql.Weeks), (1, ql.Months), (2, ql.Months), (3, ql.Months), (4, ql.Months), (5, ql.Months)]:
        try:
            # On calcule le taux forward à partir de la courbe Eonia que nous avons construite
            forward_eonia = eonia_curve.forwardRate(today, ql.TARGET().advance(today, n, units), ql.Actual360(), ql.Simple).rate()
            # On y ajoute le spread de l'utilisateur pour créer le taux synthétique
            synthetic_euribor_rate = forward_eonia + alpha
            synth_helpers.append(
                ql.DepositRateHelper(ql.QuoteHandle(ql.SimpleQuote(synthetic_euribor_rate)), 
                                     ql.Period(n, units), 2, ql.TARGET(), ql.Following, False, ql.Actual360())
            )
        except Exception as e:
            # Si le calcul d'un forward échoue, on l'ignore pour ne pas faire planter l'application
            print(f"Could not calculate synthetic helper for {n} {units}: {e}")

    # --- 4. Construction de la courbe Euribor 6M "améliorée" ---
    euribor_curve_improved = ql.PiecewiseLinearZero(today, helpers_naive + synth_helpers, ql.Actual365Fixed())

    # --- 5. Extraction des points pour le graphique, en utilisant la durée de l'utilisateur ---
    end_date = today + ql.Period(simulation_duration_years, ql.Years)
    dates = [today + ql.Period(m, ql.Months) for m in range(0, simulation_duration_years * 12 + 1)]
    
    rates_naive = [euribor_curve_naive.zeroRate(d, ql.Actual365Fixed(), ql.Compounded).rate() * 100 for d in dates]
    rates_improved = [euribor_curve_improved.zeroRate(d, ql.Actual365Fixed(), ql.Compounded).rate() * 100 for d in dates]

    plot_points_naive = [{'x': d.ISO(), 'y': round(r, 4)} for d, r in zip(dates, rates_naive)]
    plot_points_improved = [{'x': d.ISO(), 'y': round(r, 4)} for d, r in zip(dates, rates_improved)]

    return {
        'naive_curve': plot_points_naive,
        'improved_curve': plot_points_improved
    }