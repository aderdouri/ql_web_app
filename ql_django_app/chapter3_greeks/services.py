# File: ql_web_app/chapter3_greeks/services.py (VERSION COMPLETE ET CORRIGEE)

import QuantLib as ql
import numpy as np
from datetime import date

def calculate_numerical_greeks(option_params: dict, bump_size: float) -> dict:
    """
    Demonstrates the numerical calculation of Delta by bumping the spot price.
    
    It calculates the option price at three points: the initial spot, spot + bump, 
    and spot - bump. It then uses these values to approximate the derivative.

    Args:
        option_params (dict): A dictionary containing the option's parameters.
        bump_size (float): The small amount by which to change the spot price.

    Returns:
        dict: A dictionary containing all intermediate and final calculation values.
    """
    
    # This is an inner "helper" function. It contains all the QuantLib logic
    # to price the option for a single, given spot price.
    def get_option_price(spot_price: float) -> float:
        """Helper function to price the option for a given spot."""
        
        # Unpack parameters
        maturity_dt = option_params['maturity_dt']
        strike_price = option_params['strike_price']
        volatility = option_params['volatility_pct'] / 100
        risk_free_rate = option_params['risk_free_rate_pct'] / 100
        
        # Set up dates and conventions
        maturity_date = ql.Date(maturity_dt.day, maturity_dt.month, maturity_dt.year)
        calculation_date = ql.Date(8, 5, 2015) # Fixed date for consistent results
        ql.Settings.instance().evaluationDate = calculation_date
        
        # ==============================================================================
        # LA CORRECTION EST ICI : On spécifie un marché pour le calendrier
        # ==============================================================================
        calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
        day_count = ql.Actual365Fixed()

        # Build the instrument
        option_type = ql.Option.Call
        payoff = ql.PlainVanillaPayoff(option_type, strike_price)
        exercise = ql.EuropeanExercise(maturity_date)
        option = ql.VanillaOption(payoff, exercise)

        # Build the market process
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))
        flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, risk_free_rate, day_count))
        dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, 0.0, day_count))
        flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, volatility, day_count))
        
        bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)
        
        # Set the engine and return the price (NPV)
        option.setPricingEngine(ql.AnalyticEuropeanEngine(bsm_process))
        
        return option.NPV()

    # --- Main logic of the service function starts here ---

    # 1. Get base parameters from the input
    spot_initial = option_params['spot_price']
    
    # 2. Calculate the three required prices by calling the helper function
    price_initial = get_option_price(spot_initial)
    price_up = get_option_price(spot_initial + bump_size)
    price_down = get_option_price(spot_initial - bump_size)
    
    # 3. Calculate numerical Delta using the central difference formula
    delta = (price_up - price_down) / (2 * bump_size)
    
    # 4. Return all values in a dictionary for a clear demonstration in the template
    return {
        'spot_initial': spot_initial,
        'price_initial': np.round(price_initial, 4),
        'spot_up': spot_initial + bump_size,
        'price_up': np.round(price_up, 4),
        'spot_down': spot_initial - bump_size,
        'price_down': np.round(price_down, 4),
        'bump_size': bump_size,
        'delta_numerical': np.round(delta, 4)
    }