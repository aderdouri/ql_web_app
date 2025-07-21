# File: ql_web_app/chapter2_instruments/services.py

import QuantLib as ql
import numpy as np
from datetime import date

def price_option_with_selected_engine(engine_choice: str, option_params: dict) -> dict:
    """
    Creates a European option and prices it using a user-selected pricing engine.
    This serves as an interactive demonstration of the concepts in Chapter 2 of the Cookbook.

    This function is a pure "service": it takes simple Python data as input
    (strings, numbers, dates) and returns a Python dictionary with the results.
    It has no knowledge of Django.

    Args:
        engine_choice (str): The identifier for the chosen engine ('analytic', 'binomial_crr', 'monte_carlo').
        option_params (dict): A dictionary containing all the necessary parameters for the option.

    Returns:
        dict: A dictionary containing the calculated price and the name of the engine used.
    """
    
    # 1. Prepare parameters from the input dictionary
    maturity_dt = option_params['maturity_dt']
    maturity_date = ql.Date(maturity_dt.day, maturity_dt.month, maturity_dt.year)
    spot_price = option_params['spot_price']
    strike_price = option_params['strike_price']
    volatility = option_params['volatility_pct'] / 100
    risk_free_rate = option_params['risk_free_rate_pct'] / 100
    
    # For this example, we simplify to a Call option with no dividends
    option_type = ql.Option.Call
    dividend_rate = 0.0

    # 2. Set up market conventions and evaluation date
    day_count = ql.Actual365Fixed()
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    calculation_date = ql.Date(8, 5, 2015)  # Using a fixed date for consistency
    ql.Settings.instance().evaluationDate = calculation_date

    # 3. Create the financial INSTRUMENT (the contract)
    # This part remains the same regardless of the engine used.
    payoff = ql.PlainVanillaPayoff(option_type, strike_price)
    exercise = ql.EuropeanExercise(maturity_date)
    european_option = ql.VanillaOption(payoff, exercise)

    # 4. Build the market data process (used by all engines)
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))
    flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, risk_free_rate, day_count))
    dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, dividend_rate, day_count))
    flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, volatility, day_count))
    bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)

    # 5. Select and create the PRICING ENGINE based on user's choice
    # This is the core of the Chapter 2 demonstration.
    engine = None
    engine_name = ""
    if engine_choice == 'analytic':
        engine = ql.AnalyticEuropeanEngine(bsm_process)
        engine_name = "Analytic Black-Scholes Formula"
    elif engine_choice == 'binomial_crr':
        steps = 200  # Number of steps for the binomial tree
        engine = ql.BinomialVanillaEngine(bsm_process, "crr", steps)
        engine_name = "Binomial Tree (Cox-Ross-Rubinstein)"
    elif engine_choice == 'monte_carlo':
        steps = 100
        required_samples = 10000
        engine = ql.MCEuropeanEngine(bsm_process, "PseudoRandom", timeSteps=steps, requiredSamples=required_samples, seed=42)
        engine_name = "Monte Carlo Simulation"
    else:
        # If the choice is not recognized, raise an error
        raise ValueError(f"Unknown pricing engine choice: {engine_choice}")

    # 6. Attach the selected engine to the instrument
    european_option.setPricingEngine(engine)

    # 7. Calculate and return the results in a clean dictionary
    return {
        'price': np.round(european_option.NPV(), 4),
        'engine_used': engine_name
    }