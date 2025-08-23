import QuantLib as ql
import numpy as np
from datetime import date

def calculate_european_option_metrics(
    option_type_str: str, 
    maturity_dt: date, 
    spot_price: float, 
    strike_price: float, 
    volatility_pct: float, 
    dividend_rate_pct: float, 
    risk_free_rate_pct: float,
    pricing_engine_name: str,    # <-- NEW PARAMETER
    binomial_steps: int = 200    # <-- NEW PARAMETER with a default value
) -> dict:
    """
    Calculates the price and Greeks of a European option using a specified QuantLib pricing engine.
    This function demonstrates the separation of Instrument and Pricing Engine.

    Args:
        option_type_str (str): 'Call' or 'Put'.
        maturity_dt (date): The maturity date of the option.
        spot_price (float): The current price of the underlying asset.
        strike_price (float): The strike price of the option.
        volatility_pct (float): The volatility in percent (e.g., 20 for 20%).
        dividend_rate_pct (float): The dividend rate in percent (e.g., 1.63 for 1.63%).
        risk_free_rate_pct (float): The risk-free rate in percent (e.g., 0.1 for 0.1%).
        pricing_engine_name (str): The name of the engine to use (e.g., 'AnalyticEuropeanEngine').
        binomial_steps (int): The number of steps for binomial tree models.

    Returns:
        dict: A dictionary containing the calculated price and Greeks.
    """
    
    # 1. Parameter Conversion and Setup
    option_type = ql.Option.Call if option_type_str == 'Call' else ql.Option.Put
    maturity_date_ql = ql.Date(maturity_dt.day, maturity_dt.month, maturity_dt.year)
    volatility = volatility_pct / 100
    dividend_rate = dividend_rate_pct / 100
    risk_free_rate = risk_free_rate_pct / 100

    day_count = ql.Actual365Fixed()
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    
    # Set the evaluation date (can be made dynamic later)
    calculation_date = ql.Date(8, 5, 2015)
    ql.Settings.instance().evaluationDate = calculation_date

    # 2. Construct the European Option (the "Instrument")
    # The instrument's definition does not change regardless of the pricing model.
    payoff = ql.PlainVanillaPayoff(option_type, strike_price)
    exercise = ql.EuropeanExercise(maturity_date_ql)
    european_option = ql.VanillaOption(payoff, exercise)

    # 3. Construct the Market Process
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))
    flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, risk_free_rate, day_count))
    dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, dividend_rate, day_count))
    flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, volatility, day_count))
    
    bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)

    # 4. Select and construct the "Pricing Engine" based on user's choice
    if pricing_engine_name == 'AnalyticEuropeanEngine':
        engine = ql.AnalyticEuropeanEngine(bsm_process)
    elif pricing_engine_name == 'BinomialCRR':
        engine = ql.BinomialVanillaEngine(bsm_process, 'crr', binomial_steps)
    elif pricing_engine_name == 'BinomialJR':
        engine = ql.BinomialVanillaEngine(bsm_process, 'jr', binomial_steps)
    else:
        raise ValueError(f"Unknown pricing engine: {pricing_engine_name}")
        
    # 5. Attach the engine to the instrument
    european_option.setPricingEngine(engine)

    # 6. Calculate and structure the results
    # Note: Greeks are only available for the analytic engine. For others, we return 'N/A'.
    # This is a key part of the demonstration for the user.
    can_calculate_greeks = (pricing_engine_name == 'AnalyticEuropeanEngine')
    
    results = {
        'price': np.round(european_option.NPV(), 4),
        'engine_used': pricing_engine_name,
        'delta': np.round(european_option.delta(), 4) if can_calculate_greeks else 'N/A',
        'gamma': np.round(european_option.gamma(), 4) if can_calculate_greeks else 'N/A',
        'vega': np.round(european_option.vega(), 4) if can_calculate_greeks else 'N/A',
        'theta': np.round(european_option.thetaPerDay(), 4) if can_calculate_greeks else 'N/A',
    }
    
    return results