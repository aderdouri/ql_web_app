import QuantLib as ql
import numpy as np
from datetime import date

def compare_bsm_and_heston(option_params: dict, heston_params: dict, evaluation_dt: date):
    """
    Calculates the price of a European option with both BSM and Heston models,
    exactly matching the book's Chapter 21 implementation.
    """
    # 1. Set evaluation date (matching book)
    calculation_date = ql.Date(evaluation_dt.day, evaluation_dt.month, evaluation_dt.year)
    ql.Settings.instance().evaluationDate = calculation_date
    day_count = ql.Actual365Fixed()
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)

    # Unpack option parameters
    maturity_dt = option_params['maturity_dt']
    maturity_date = ql.Date(maturity_dt.day, maturity_dt.month, maturity_dt.year)
    spot_price = option_params['spot_price']
    strike_price = option_params['strike_price']
    dividend_rate = option_params['dividend_rate_pct'] / 100.0
    risk_free_rate = option_params['risk_free_rate_pct'] / 100.0
    
    # Handle option type
    option_type_str = option_params.get('option_type', 'call')
    option_type = ql.Option.Call if option_type_str == 'call' else ql.Option.Put

    # 2. Option parameters are now created separately for each model

    # 3. Setup market data handles (matching book)
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))
    flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, risk_free_rate, day_count))
    dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, dividend_rate, day_count))

    # --- Heston Model Calculation (matching book exactly) ---
    v0, kappa, theta, sigma, rho = heston_params.values()
    
    # Create Heston process with exact book parameters
    heston_process = ql.HestonProcess(flat_ts, dividend_yield, spot_handle, v0, kappa, theta, sigma, rho)
    heston_model = ql.HestonModel(heston_process)
    
    # Use exact engine parameters from book
    heston_engine_rate = option_params.get('heston_engine_rate', 0.01)
    heston_engine_steps = option_params.get('heston_engine_steps', 1000)
    
    # Create option exactly as in book
    heston_payoff = ql.PlainVanillaPayoff(option_type, strike_price)
    heston_exercise = ql.EuropeanExercise(maturity_date)
    heston_option = ql.VanillaOption(heston_payoff, heston_exercise)
    
    # Set engine with exact parameters
    heston_engine = ql.AnalyticHestonEngine(heston_model, heston_engine_rate, heston_engine_steps)
    heston_option.setPricingEngine(heston_engine)
    
    # Calculate price
    h_price = heston_option.NPV()
    
    # Round to match book precision (15 decimal places)
    h_price = round(h_price, 15)

    # --- Black-Scholes-Merton Model Calculation (matching book) ---
    volatility = option_params['volatility_pct'] / 100.0
    flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, volatility, day_count))
    bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)
    bsm_engine = ql.AnalyticEuropeanEngine(bsm_process)
    
    # Create a fresh option for BSM calculation
    bsm_payoff = ql.PlainVanillaPayoff(option_type, strike_price)
    bsm_exercise = ql.EuropeanExercise(maturity_date)
    bsm_option = ql.VanillaOption(bsm_payoff, bsm_exercise)
    
    bsm_option.setPricingEngine(bsm_engine)
    bs_price = bsm_option.NPV()
    
    # Round to match book precision (15 decimal places)
    bs_price = round(bs_price, 15)

    # Calculate difference (matching book output)
    difference = bs_price - h_price
    
    return {
        'heston_price': h_price,
        'bsm_price': bs_price,
        'difference': difference,
        'heston_price_formatted': f"{h_price:.15f}",
        'bsm_price_formatted': f"{bs_price:.15f}",
        'difference_formatted': f"{difference:.3f}"
    }