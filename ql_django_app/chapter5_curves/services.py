# Fichier : ql_web_app/chapter5_curves/services.py
import QuantLib as ql
from datetime import date
import numpy as np

def build_and_get_curve_data(market_rates: dict, evaluation_dt: date):
    evaluation_date = ql.Date(evaluation_dt.day, evaluation_dt.month, evaluation_dt.year)
    ql.Settings.instance().evaluationDate = evaluation_date
    calendar = ql.TARGET()
    day_count = ql.Actual360()

    rate_helpers = []
    for tenor_str, rate in market_rates.items():
        tenor_period = ql.Period(tenor_str)
        quote = ql.QuoteHandle(ql.SimpleQuote(rate / 100))
        if tenor_period.units() == ql.Years and tenor_period.length() >= 2:
            rate_helpers.append(
                ql.SwapRateHelper(quote, tenor_period, calendar, ql.Annual, ql.Unadjusted, day_count, ql.Euribor6M())
            )

    yield_curve = ql.PiecewiseLogCubicDiscount(evaluation_date, rate_helpers, ql.Actual365Fixed())
    yield_curve.enableExtrapolation()

    plot_points = []
    for year in np.arange(0, 15.25, 0.25):
        d = calendar.advance(evaluation_date, ql.Period(int(year * 12), ql.Months))
        rate = yield_curve.zeroRate(d, ql.Actual365Fixed(), ql.Compounded).rate() * 100
        plot_points.append({'year': year, 'rate': round(rate, 4)})
        
    return {
        'plot_points': plot_points,
        'evaluation_date': evaluation_date.ISO()
    }