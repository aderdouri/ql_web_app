import QuantLib as ql
import numpy as np
from datetime import date

# The function now accepts the evaluation_dt from the view
def compare_bsm_and_heston(option_params: dict, heston_params: dict, evaluation_dt: date):
    """
    Calculates the price of a European option with both BSM and Heston models,
    using a user-defined evaluation date.
    """
    # 1. Use the user-provided evaluation date
    today = ql.Date(evaluation_dt.day, evaluation_dt.month, evaluation_dt.year)
    ql.Settings.instance().evaluationDate = today
    day_count = ql.Actual365Fixed()
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)

    # Unpack option parameters
    maturity_dt = option_params['maturity_dt']
    maturity_date = ql.Date(maturity_dt.day, maturity_dt.month, maturity_dt.year)
    spot_price = option_params['spot_price']
    strike_price = option_params['strike_price']
    dividend_rate = option_params['dividend_rate_pct'] / 100.0
    risk_free_rate = option_params['risk_free_rate_pct'] / 100.0
    option_type = ql.Option.Call

    # 2. Build the instrument (the option)
    payoff = ql.PlainVanillaPayoff(option_type, strike_price)
    exercise = ql.EuropeanExercise(maturity_date)
    option = ql.VanillaOption(payoff, exercise)

    # 3. Setup market data handles
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))
    flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(today, risk_free_rate, day_count))
    dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(today, dividend_rate, day_count))

    # --- Heston Model Calculation ---
    v0, kappa, theta, sigma, rho = heston_params.values()
    heston_process = ql.HestonProcess(flat_ts, dividend_yield, spot_handle, v0, kappa, theta, sigma, rho)
    heston_model = ql.HestonModel(heston_process)
    heston_engine = ql.AnalyticHestonEngine(heston_model)
    option.setPricingEngine(heston_engine)
    h_price = option.NPV()

    # --- Black-Scholes-Merton Model Calculation ---
    volatility = option_params['volatility_pct'] / 100.0
    flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, calendar, volatility, day_count))
    bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)
    bsm_engine = ql.AnalyticEuropeanEngine(bsm_process)
    option.setPricingEngine(bsm_engine)
    bs_price = option.NPV()

    return {
        'heston_price': round(h_price, 4),
        'bsm_price': round(bs_price, 4),
        'difference': round(bs_price - h_price, 4)
    }