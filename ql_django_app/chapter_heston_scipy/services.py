# File: ql_web_app/chapter_heston_scipy/services.py

import QuantLib as ql
import numpy as np
from scipy.optimize import root, least_squares
import math

# --- Helper Functions (from the notebook) ---

def setup_helpers_and_model(spot, yield_ts, dividend_ts, calculation_date):
    """
    Creates a Heston model and a set of HestonModelHelper objects
    from a simplified market data set for calibration.
    """
    # Using a simpler vol surface for faster, more stable calibration
    expiration_dates = [calculation_date + ql.Period(y, ql.Years) for y in [1, 2, 3]]
    strikes = [593.43, 659.37, 725.31]
    data = [
        [0.35, 0.30, 0.33], 
        [0.34, 0.29, 0.32],
        [0.33, 0.28, 0.31]
    ]
    
    # Setup Heston model with a standard initial guess
    init_condition = (0.04, 0.2, 0.5, -0.75, 0.01) # theta, kappa, sigma, rho, v0
    theta, kappa, sigma, rho, v0 = init_condition
    process = ql.HestonProcess(yield_ts, dividend_ts, ql.QuoteHandle(ql.SimpleQuote(spot)), v0, kappa, theta, sigma, rho)
    model = ql.HestonModel(process)
    engine = ql.AnalyticHestonEngine(model)
    
    # Create a helper for each market data point
    helpers = []
    for i, date in enumerate(expiration_dates):
        for j, s in enumerate(strikes):
            t = (date - calculation_date)
            p = ql.Period(t, ql.Days)
            vols = data[i][j]
            helper = ql.HestonModelHelper(p, ql.TARGET(), spot, s, ql.QuoteHandle(ql.SimpleQuote(vols)), yield_ts, dividend_ts)
            helper.setPricingEngine(engine)
            helpers.append(helper)
            
    return model, helpers

def cost_function_generator(model, helpers, norm=False):
    """
    Returns a cost function for SciPy optimizers.
    This version includes safety checks to prevent crashes from invalid parameters.
    """
    def cost_function(params):
        try:
            if params[0] < 0 or params[1] < 0 or params[2] < 0 or params[4] < 0:
                return [1e6] * len(helpers)
            params_ = ql.Array(list(params))
            model.setParams(params_)
            error = [h.calibrationError() for h in helpers]
            if np.isnan(error).any():
                return [1e6] * len(helpers)
            return np.sqrt(np.sum(np.abs(error))) if norm else np.array(error)
        except Exception:
            return [1e6] * len(helpers)
    return cost_function

# --- Main Service Function ---

def run_calibration(optimizer_name: str):
    """
    Runs the Heston model calibration using a user-selected optimization algorithm.
    """
    day_count = ql.Actual365Fixed()
    calculation_date = ql.Date(6, 11, 2015)
    ql.Settings.instance().evaluationDate = calculation_date
    spot = 659.37
    yield_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, 0.01, day_count))
    dividend_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, 0.0, day_count))

    model, helpers = setup_helpers_and_model(spot, yield_ts, dividend_ts, calculation_date)
    initial_params = list(model.params())

    # Define realistic bounds for constrained optimizers
    # Parameters order: [theta, kappa, sigma, rho, v0]
    lower_bounds = [0.001, 0.01, 0.01, -1.0, 0.001]
    upper_bounds = [2.0, 20.0, 2.0, 1.0, 2.0]
    
    # Select and run the chosen optimizer
    if optimizer_name == 'QL Levenberg-Marquardt':
        lm = ql.LevenbergMarquardt(1e-8, 1e-8, 1e-8)
        # ==============================================================================
        # CORRECTION: We remove the constraint argument as it's not supported
        # by HestonModel.calibrate() in this simple way. This optimizer will run unconstrained.
        # ==============================================================================
        model.calibrate(helpers, lm, ql.EndCriteria(500, 300, 1e-8, 1e-8, 1e-8))
        
    elif optimizer_name == 'SciPy Levenberg-Marquardt':
        # Note: scipy.optimize.root with 'lm' method does not support bounds.
        cost_fun = cost_function_generator(model, helpers)
        root(cost_fun, initial_params, method="lm")
        
    elif optimizer_name == 'SciPy Least Squares':
        cost_fun = cost_function_generator(model, helpers)
        # We pass the bounds to this optimizer
        bounds = (lower_bounds, upper_bounds)
        least_squares(cost_fun, initial_params, bounds=bounds)
        
    else:
        raise ValueError(f"Optimizer '{optimizer_name}' not recognized.")

    # Calculate and format the results
    avg_err = 0.0
    for h in helpers:
        avg_err += abs(h.modelValue() / h.marketValue() - 1.0)
    avg_err = avg_err * 100.0 / len(helpers)
    
    params = model.params()
    param_string = f"θ={params[0]:.3f}, κ={params[1]:.3f}, σ={params[2]:.3f}, ρ={params[3]:.3f}, v₀={params[4]:.3f}"
    
    return {
        'optimizer': optimizer_name,
        'avg_error_pct': round(avg_err, 4),
        'params': param_string
    }