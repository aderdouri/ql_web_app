# File: ql_web_app/chapter2_instruments/services.py
import QuantLib as ql
import numpy as np

def price_option_with_engine(option_params: dict, engine_choice: str):
    """
    Creates a European option, prices it with the selected engine, and simulates
    the beginning of the binomial tree for visualization.
    """
    # 1. Setup and parameter conversion
    today = ql.Date(8, 5, 2015)
    ql.Settings.instance().evaluationDate = today
    day_count = ql.Actual365Fixed()
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    
    maturity_date = ql.Date(option_params['maturity_dt'].day, option_params['maturity_dt'].month, option_params['maturity_dt'].year)
    spot_price = option_params['spot_price']
    strike_price = option_params['strike_price']
    volatility = option_params['volatility_pct'] / 100.0
    dividend_rate = option_params['dividend_rate_pct'] / 100.0
    risk_free_rate = option_params['risk_free_rate_pct'] / 100.0
    option_type = ql.Option.Call

    # 2. Build Instrument and Market Process
    payoff = ql.PlainVanillaPayoff(option_type, strike_price)
    exercise = ql.EuropeanExercise(maturity_date)
    european_option = ql.VanillaOption(payoff, exercise)
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))
    flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(today, risk_free_rate, day_count))
    dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(today, dividend_rate, day_count))
    flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, calendar, volatility, day_count))
    bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)

    # 3. Select Engine and prepare visualization data
    engine = None
    engine_name = ""
    plot_data = None
    
    if engine_choice == 'analytic':
        engine = ql.AnalyticEuropeanEngine(bsm_process)
        engine_name = "Analytic Black-Scholes Formula"
    
    elif engine_choice == 'binomial_crr':
        steps_for_pricing = 200
        engine = ql.BinomialVanillaEngine(bsm_process, "crr", steps_for_pricing)
        engine_name = f"Binomial Tree CRR ({steps_for_pricing} steps)"
        
        maturity_time = day_count.yearFraction(today, maturity_date)
        dt = maturity_time / steps_for_pricing
        u = np.exp(volatility * np.sqrt(dt))
        d = 1.0 / u
        
        nodes = []
        steps_for_plot = 15
        min_price, max_price = spot_price, spot_price
        
        for i in range(steps_for_plot + 1):
            for j in range(i + 1):
                price = spot_price * (u**j) * (d**(i-j))
                nodes.append({'x': i, 'y': price})
                if price < min_price: min_price = price
                if price > max_price: max_price = price

        plot_data = {
            'nodes': nodes,
            'min_price': min_price * 0.98,
            'max_price': max_price * 1.02
        }

    elif engine_choice == 'monte_carlo':
        steps = 100
        num_paths = 10000
        engine = ql.MCEuropeanEngine(bsm_process, "PseudoRandom", timeSteps=steps, requiredSamples=num_paths, seed=42)
        engine_name = f"Monte Carlo ({num_paths} paths)"
    
    # This line must be outside the if/elif blocks
    european_option.setPricingEngine(engine)
    
    return {
        'price': np.round(european_option.NPV(), 4),
        'engine_used': engine_name,
        'plot_data': plot_data 
    }