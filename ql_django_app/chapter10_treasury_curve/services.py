import QuantLib as ql
from datetime import date
import numpy as np

def build_treasury_curve(evaluation_dt: date):
    """
    Construit une courbe de taux du Trésor à partir de données de marché simulées,
    comme décrit dans le Chapitre 10 du Cookbook.
    """
    eval_date = ql.Date(evaluation_dt.day, evaluation_dt.month, evaluation_dt.year)
    ql.Settings.instance().evaluationDate = eval_date
    
    # Données de marché (obligations et bons du Trésor)
    deposits_data = {
        (1, ql.Weeks): 0.0382,
        (1, ql.Months): 0.0372,
        (3, ql.Months): 0.0363,
        (6, ql.Months): 0.0353,
    }
    
    bonds_data = [
        (date(2005, 5, 15), 2.0),
        (date(2006, 5, 15), 2.25),
        (date(2007, 5, 15), 2.5),
        (date(2008, 5, 15), 2.75)
    ]

    # Préparation
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    day_count = ql.Actual365Fixed()
    settlement_days = 2
    face_amount = 100
    
    # Création des Rate Helpers
    rate_helpers = []
    
    # Pour les dépôts
    for period, rate in deposits_data.items():
        tenor = ql.Period(period[0], period[1])
        helper = ql.DepositRateHelper(ql.QuoteHandle(ql.SimpleQuote(rate/100)), tenor, settlement_days, calendar, ql.ModifiedFollowing, False, day_count)
        rate_helpers.append(helper)
        
    # Pour les obligations
    for maturity_dt, coupon_rate in bonds_data:
        maturity = ql.Date(maturity_dt.day, maturity_dt.month, maturity_dt.year)
        schedule = ql.Schedule(eval_date, maturity, ql.Period(ql.Semiannual), calendar, ql.Unadjusted, ql.Unadjusted, ql.DateGeneration.Backward, False)
        helper = ql.FixedRateBondHelper(ql.QuoteHandle(ql.SimpleQuote(face_amount)), settlement_days, face_amount, schedule, [coupon_rate/100], day_count, ql.Unadjusted)
        rate_helpers.append(helper)

    # Construction de la courbe
    yield_curve = ql.PiecewiseLogCubicDiscount(eval_date, rate_helpers, day_count)
    yield_curve.enableExtrapolation()

    # Extraction des points pour le graphique
    plot_points = []
    for year in np.arange(0, 5, 0.25):
        d = calendar.advance(eval_date, ql.Period(int(year * 12), ql.Months))
        rate = yield_curve.zeroRate(d, day_count, ql.Compounded).rate() * 100
        plot_points.append({'year': year, 'rate': round(rate, 4)})
        
    return plot_points