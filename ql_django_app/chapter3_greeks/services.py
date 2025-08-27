# File: ql_web_app/chapter3_greeks/services.py
import QuantLib as ql
import numpy as np

def calculate_all_numerical_greeks(option_params: dict):
    """
    Calculates the price, main Greeks, and data for a price curve plot.
    """
    eval_dt = option_params['evaluation_dt']
    eval_date = ql.Date(eval_dt.day, eval_dt.month, eval_dt.year)
    ql.Settings.instance().evaluationDate = eval_date
    day_count = ql.Actual365Fixed()
    calendar = ql.TARGET()

    def get_option_price(spot, vol, rate, maturity_dt, strike):
        maturity = ql.Date(maturity_dt.day, maturity_dt.month, maturity_dt.year)
        if maturity <= eval_date: return 0.0

        risk_free_handle = ql.YieldTermStructureHandle(ql.FlatForward(eval_date, rate, day_count))
        dividend_handle = ql.YieldTermStructureHandle(ql.FlatForward(eval_date, 0.0, day_count))
        vol_handle = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(eval_date, calendar, vol, day_count))
        process = ql.BlackScholesMertonProcess(ql.QuoteHandle(ql.SimpleQuote(spot)), dividend_handle, risk_free_handle, vol_handle)
        
        option = ql.VanillaOption(ql.PlainVanillaPayoff(ql.Option.Call, strike), ql.EuropeanExercise(maturity))
        option.setPricingEngine(ql.AnalyticEuropeanEngine(process))
        return option.NPV()

    spot = option_params['spot_price']
    vol = option_params['volatility_pct'] / 100.0
    rate = option_params['risk_free_rate_pct'] / 100.0
    strike = option_params['strike_price']
    maturity = option_params['maturity_dt']
    bump = spot * 0.001

    base_price = get_option_price(spot, vol, rate, maturity, strike)
    
    p_up = get_option_price(spot + bump, vol, rate, maturity, strike)
    p_down = get_option_price(spot - bump, vol, rate, maturity, strike)
    delta = (p_up - p_down) / (2 * bump)
    gamma = (p_up - 2*base_price + p_down) / (bump**2)
    
    p_vol_up = get_option_price(spot, vol + 0.01, rate, maturity, strike)
    vega = p_vol_up - base_price
    
    p_rate_up = get_option_price(spot, vol, rate + 0.01, maturity, strike)
    rho = p_rate_up - base_price

    spot_range = np.linspace(spot * 0.8, spot * 1.2, 50)
    price_curve = [{'x': s, 'y': get_option_price(s, vol, rate, maturity, strike)} for s in spot_range]

    return {
        'price': f"{base_price:.4f}",
        'greeks': {
            'Delta': f"{delta:.4f}",
            'Gamma': f"{gamma:.4f}",
            'Vega (per 1%)': f"{vega:.4f}",
            'Rho (per 1%)': f"{rho:.4f}",
        },
        'plot_data': price_curve,
        'center_point': {'x': spot, 'y': base_price}

    }