import QuantLib as ql
import numpy as np

def calibrate_heston_and_get_smile(atm_vol_pct: float, smile_skew: float):
    """
    Dynamically generates a market volatility smile based on user input,
    calibrates the Heston model to it, and returns the results for plotting.
    """
    try:
        # --- 1. Setup ---
        today = ql.Date(6, 11, 2015)
        ql.Settings.instance().evaluationDate = today
        calendar = ql.TARGET()
        day_count = ql.Actual365Fixed()
        spot = 659.37
        risk_free_rate = 0.01
        dividend_rate = 0.0

        flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(today, risk_free_rate, day_count))
        dividend_ts = ql.YieldTermStructureHandle(ql.FlatForward(today, dividend_rate, day_count))
        
        maturity_date = today + ql.Period("1Y")
        strikes = [593.43, 626.40, 659.37, 692.34, 725.31]

        # --- Dynamically generate the market smile based on user parameters ---
        atm_vol = atm_vol_pct / 100.0
        # Simple quadratic formula to create a smile/skew
        market_vols = [
            atm_vol + smile_skew * (s/spot - 1) + 0.8 * (s/spot - 1)**2 
            for s in strikes
        ]
        
        # --- 2. Heston Model Calibration ---
        # We use a fixed, stable initial guess for the optimizer
        initial_params = {'v0': atm_vol**2, 'kappa': 3.0, 'theta': atm_vol**2, 'rho': -0.5, 'sigma': 0.5}
        
        # Ensure we are using a list, not a set or other unserializable type
        v0, kappa, theta, rho, sigma = list(initial_params.values())
        
        process = ql.HestonProcess(flat_ts, dividend_ts, ql.QuoteHandle(ql.SimpleQuote(spot)), v0, kappa, theta, sigma, rho)
        model = ql.HestonModel(process)
        engine = ql.AnalyticHestonEngine(model)
        
        helpers = []
        for s, vol in zip(strikes, market_vols):
            period = ql.Period(maturity_date - today, ql.Days)
            helper = ql.HestonModelHelper(period, calendar, spot, s, ql.QuoteHandle(ql.SimpleQuote(vol)), flat_ts, dividend_ts)
            helper.setPricingEngine(engine)
            helpers.append(helper)

        lm = ql.LevenbergMarquardt()
        model.calibrate(helpers, lm, ql.EndCriteria(100, 10, 1.0e-8, 1.0e-8, 1.0e-8))
        theta_cal, kappa_cal, sigma_cal, rho_cal, v0_cal = model.params()

        # --- 3. Prepare data for the IHM display ---
        bsm_process = ql.BlackScholesMertonProcess(ql.QuoteHandle(ql.SimpleQuote(spot)), dividend_ts, flat_ts, ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, calendar, 0.20, day_count)))

        errors_table = []
        for i, opt in enumerate(helpers):
            err = (opt.modelValue()/opt.marketValue() - 1.0)
            errors_table.append({'strike': strikes[i], 'market_price': f"{opt.marketValue():.4f}", 'model_price': f"{opt.modelValue():.4f}", 'rel_error_pct': f"{err*100:.2f}%"})

        strikes_grid = np.linspace(550, 750, 25)
        model_vols = []
        for s_grid in strikes_grid:
            payoff = ql.PlainVanillaPayoff(ql.Option.Call, s_grid)
            exercise = ql.EuropeanExercise(maturity_date)
            option = ql.VanillaOption(payoff, exercise)
            option.setPricingEngine(engine)
            price = option.NPV()
            try:
                implied_vol = option.impliedVolatility(price, bsm_process, 1.0e-4)
                model_vols.append(implied_vol)
            except RuntimeError:
                model_vols.append(np.nan)
        
        market_smile = [{'x': s, 'y': v*100} for s, v in zip(strikes, market_vols)]
        model_smile = [{'x': s, 'y': v*100} for s, v in zip(strikes_grid, model_vols) if not np.isnan(v)]
        
        return {
            'params': f"θ={theta_cal:.3f}, κ={kappa_cal:.3f}, σ={sigma_cal:.3f}, ρ={rho_cal:.3f}, v₀={v0_cal:.3f}",
            'errors_table': errors_table,
            'market_smile': market_smile,
            'model_smile': model_smile
        }
    except Exception as e:
        print(f"ERROR IN HESTON CALIBRATION SERVICE: {e}")
        return {'error': str(e)}