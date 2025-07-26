import QuantLib as ql
import numpy as np

def calculate_numerical_greeks(option_params: dict, bump_size: float, evaluation_dt):
    """
    Demonstrates the numerical calculation of Delta using a user-defined evaluation date.
    """
    
    # 1. Use the evaluation date provided by the user
    calculation_date = ql.Date(evaluation_dt.day, evaluation_dt.month, evaluation_dt.year)
    ql.Settings.instance().evaluationDate = calculation_date
    
    def get_option_price(spot_price: float) -> float:
        """Helper function to price the option for a given spot price."""
        maturity_dt = option_params['maturity_dt']
        strike_price = option_params['strike_price']
        volatility = option_params['volatility_pct'] / 100
        risk_free_rate = option_params['risk_free_rate_pct'] / 100
        
        maturity_date = ql.Date(maturity_dt.day, maturity_dt.month, maturity_dt.year)
        
        # Safety check: if the option has expired, its price is zero
        if maturity_date <= calculation_date:
            return 0.0

        option_type = ql.Option.Call
        payoff = ql.PlainVanillaPayoff(option_type, strike_price)
        exercise = ql.EuropeanExercise(maturity_date)
        option = ql.VanillaOption(payoff, exercise)

        spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))
        day_count = ql.Actual365Fixed()
        calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
        
        flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, risk_free_rate, day_count))
        dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, 0.0, day_count))
        flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, volatility, day_count))
        
        bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)
        option.setPricingEngine(ql.AnalyticEuropeanEngine(bsm_process))
        
        return option.NPV()

    spot_initial = option_params['spot_price']
    
    price_initial = get_option_price(spot_initial)
    price_up = get_option_price(spot_initial + bump_size)
    price_down = get_option_price(spot_initial - bump_size)
    
    delta = 0.0
    if (2 * bump_size) > 1e-9:
        delta = (price_up - price_down) / (2 * bump_size)
    
    return {
        'evaluation_date': calculation_date.ISO(),
        'price_initial': np.round(price_initial, 4),
        'price_up': np.round(price_up, 4),
        'price_down': np.round(price_down, 4),
        'delta_numerical': np.round(delta, 4)
    }