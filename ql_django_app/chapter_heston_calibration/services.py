import QuantLib as ql
import numpy as np

def run_heston_calibration(initial_params: dict, max_iterations: int):
    """
    Calibre un modèle de Heston sur une surface de volatilité implicite.
    """
    
    # --- Setup de marché ---
    day_count = ql.Actual365Fixed()
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    calculation_date = ql.Date(6, 11, 2015)
    ql.Settings.instance().evaluationDate = calculation_date

    spot = 659.37
    risk_free_rate = 0.01
    dividend_rate = 0.0
    flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, risk_free_rate, day_count))
    dividend_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, dividend_rate, day_count))

    expiration_dates = [ql.Date(6,m,y) for y,m in [(2015,12), (2016,1), (2016,3), (2016,6), (2016,12), (2017,12)]]
    strikes = [527.50, 593.43, 626.40, 659.37, 692.34, 725.31, 758.28]
    data = [[0.37, 0.30, 0.27, 0.26, 0.25, 0.25, 0.26], [0.34, 0.29, 0.27, 0.26, 0.25, 0.25, 0.25],
            [0.37, 0.34, 0.32, 0.31, 0.30, 0.29, 0.29], [0.35, 0.33, 0.32, 0.31, 0.30, 0.30, 0.29],
            [0.35, 0.33, 0.32, 0.32, 0.31, 0.31, 0.31], [0.35, 0.34, 0.33, 0.32, 0.32, 0.31, 0.31]]

    implied_vols = ql.Matrix(len(strikes), len(expiration_dates))
    for i in range(len(strikes)):
        for j in range(len(expiration_dates)):
            implied_vols[i][j] = data[j][i]

    black_var_surface = ql.BlackVarianceSurface(calculation_date, calendar, expiration_dates, strikes, implied_vols, day_count)

    # --- Calibration du modèle ---
    v0, kappa, theta, sigma, rho = initial_params.values()
    process = ql.HestonProcess(flat_ts, dividend_ts, ql.QuoteHandle(ql.SimpleQuote(spot)), v0, kappa, theta, sigma, rho)
    model = ql.HestonModel(process)
    engine = ql.AnalyticHestonEngine(model)

    heston_helpers = []
    # ==============================================================================
    # On va aussi stocker les strikes et maturités correspondants à chaque helper
    # ==============================================================================
    helper_metadata = [] 
    
    black_var_surface.setInterpolation("bicubic")
    for i in range(len(expiration_dates)):
        for j in range(len(strikes)):
            t = (expiration_dates[i] - calculation_date)
            vol = implied_vols[j][i]
            helper = ql.HestonModelHelper(ql.Period(t, ql.Days), calendar, spot, strikes[j], ql.QuoteHandle(ql.SimpleQuote(vol)), flat_ts, dividend_ts)
            helper.setPricingEngine(engine)
            heston_helpers.append(helper)
            # On stocke les informations correspondantes
            helper_metadata.append({'strike': strikes[j], 'maturity': expiration_dates[i]})

    lm = ql.LevenbergMarquardt(1e-8, 1e-8, 1e-8)
    model.calibrate(heston_helpers, lm, ql.EndCriteria(max_iterations, 50, 1e-8, 1e-8, 1e-8))
    
    calibrated_params = {'theta': model.theta(), 'kappa': model.kappa(), 'sigma': model.sigma(), 'rho': model.rho(), 'v0': model.v0()}

    # --- Analyse de l'erreur ---
    errors = []
    # ==============================================================================
    # LA CORRECTION EST ICI : On boucle sur les helpers et leurs métadonnées en même temps
    # ==============================================================================
    for i, opt in enumerate(heston_helpers):
        err = (opt.modelValue() / opt.marketValue() - 1.0)
        
        # On récupère le strike et la maturité de notre liste de métadonnées
        meta = helper_metadata[i]
        
        errors.append({
            'strike': meta['strike'], 
            'maturity': meta['maturity'].ISO(),
            'market_vol': opt.marketValue() * 100, 
            'model_vol': opt.modelValue() * 100, 
            'error_pct': err * 100
        })

    return {'calibrated_params': calibrated_params, 'errors': errors}