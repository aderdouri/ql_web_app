# File: ql_web_app/chapter_2_lab/services.py
import QuantLib as ql
from datetime import date

def run_engine_comparison(
    spot_price: float, 
    strike_price: float, 
    maturity_dt: date, 
    volatility_pct: float, 
    risk_free_rate_pct: float,
    selected_engines: list
):
    """
    Prices a single European option instrument with multiple selected pricing engines.
    """
    # 1. Setup
    maturity_date = ql.Date(maturity_dt.day, maturity_dt.month, maturity_dt.year)
    volatility = volatility_pct / 100
    risk_free_rate = risk_free_rate_pct / 100
    
    # Utiliser la date du jour pour le calcul pour plus de réalisme
    calculation_date = ql.Date.todaysDate()
    ql.Settings.instance().evaluationDate = calculation_date
    day_count = ql.Actual365Fixed()
    calendar = ql.UnitedStates()

    # 2. Create the INSTRUMENT (once)
    payoff = ql.PlainVanillaPayoff(ql.Option.Call, strike_price)
    exercise = ql.EuropeanExercise(maturity_date)
    european_option = ql.VanillaOption(payoff, exercise)

    # 3. Create the Market Process (once)
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))
    flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, risk_free_rate, day_count))
    dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, 0.0, day_count)) # Pas de dividende
    flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, volatility, day_count))
    bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)

    # 4. Loop through selected engines, price, and collect results
    results_list = []
    for engine_name in selected_engines:
        engine = None # Initialiser l'engine
        if engine_name == 'AnalyticEuropeanEngine':
            engine = ql.AnalyticEuropeanEngine(bsm_process)
            notes = "Fastest, provides all Greeks."
        elif engine_name == 'BinomialCRR':
            engine = ql.BinomialVanillaEngine(bsm_process, 'crr', 200)
            notes = "Numerical method, converges to the analytic price."
        elif engine_name == 'BinomialJR':
            engine = ql.BinomialVanillaEngine(bsm_process, 'jr', 200)
            notes = "Another type of binomial tree."
        
        if engine:
            european_option.setPricingEngine(engine)
            results_list.append({
                'engine_name': engine_name.replace('Engine', ''),
                'price': round(european_option.NPV(), 5),
                'notes': notes
            })
            
    return results_list