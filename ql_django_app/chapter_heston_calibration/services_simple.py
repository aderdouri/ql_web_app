import QuantLib as ql
import numpy as np
from scipy.optimize import root, least_squares, differential_evolution, basinhopping
from datetime import date

def calibrate_heston_parameters(calibration_data):
    """
    Simple and robust Heston calibration
    """
    try:
        # Parse input data
        spot = calibration_data['spot_price']
        risk_free_rate = calibration_data['risk_free_rate_pct'] / 100.0
        dividend_rate = calibration_data['dividend_rate_pct'] / 100.0
        calc_date = calibration_data['calculation_date']
        solver_method = calibration_data['solver_method']
        
        # Get initial parameters
        theta_init = max(0.01, min(0.5, calibration_data['initial_theta']))
        kappa_init = max(0.1, min(20, calibration_data['initial_kappa']))
        sigma_init = max(0.1, min(2.0, calibration_data['initial_sigma']))
        rho_init = max(-0.99, min(0.99, calibration_data['initial_rho']))
        v0_init = max(0.01, min(0.5, calibration_data['initial_v0']))
        
        # Ensure Feller condition
        if 2 * kappa_init * theta_init < sigma_init * sigma_init:
            kappa_init = max(0.1, sigma_init * sigma_init / (2 * theta_init) + 0.1)
        
        print(f"DEBUG: Initial params: θ={theta_init}, κ={kappa_init}, σ={sigma_init}, ρ={rho_init}, v₀={v0_init}")
        
        # Setup QuantLib
        calc_date_ql = ql.Date(calc_date.day, calc_date.month, calc_date.year)
        ql.Settings.instance().evaluationDate = calc_date_ql
        
        day_count = ql.Actual365Fixed()
        calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
        
        flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(calc_date_ql, risk_free_rate, day_count))
        dividend_ts = ql.YieldTermStructureHandle(ql.FlatForward(calc_date_ql, dividend_rate, day_count))
        
        # Use simple data structure (single maturity)
        expiration_dates = [ql.Date(6, 11, 2016)]  # Single maturity
        strikes = [527.50, 560.46, 593.43, 626.40, 659.37, 692.34, 725.31, 758.28]
        
        # Use first row of data (single maturity)
        data = [[0.37819, 0.34177, 0.30394, 0.27832, 0.26453, 0.25916, 0.25941, 0.26127]]
        
        # Setup model
        process = ql.HestonProcess(flat_ts, dividend_ts, ql.QuoteHandle(ql.SimpleQuote(spot)), 
                                 v0_init, kappa_init, theta_init, sigma_init, rho_init)
        model = ql.HestonModel(process)
        engine = ql.AnalyticHestonEngine(model)
        
        # Setup helpers
        helpers = []
        for i, date in enumerate(expiration_dates):
            for j, s in enumerate(strikes):
                t = (date - calc_date_ql)
                p = ql.Period(t, ql.Days)
                vols = data[i][j]
                helper = ql.HestonModelHelper(p, calendar, spot, s, 
                                            ql.QuoteHandle(ql.SimpleQuote(vols)), 
                                            flat_ts, dividend_ts)
                helper.setPricingEngine(engine)
                helpers.append(helper)
        
        print(f"DEBUG: Created {len(helpers)} helpers")
        
        # Run calibration
        if solver_method == 'ql_lm':
            # QuantLib Levenberg-Marquardt
            lm = ql.LevenbergMarquardt(1e-8, 1e-8, 1e-8)
            model.calibrate(helpers, lm, ql.EndCriteria(500, 300, 1.0e-8, 1.0e-8, 1.0e-8))
            print("DEBUG: QuantLib calibration completed")
        else:
            # SciPy methods
            def cost_function(params):
                try:
                    theta, kappa, sigma, rho, v0 = params
                    
                    # Validate parameters
                    if (theta <= 0 or kappa <= 0 or sigma <= 0 or 
                        abs(rho) >= 1 or v0 <= 0 or 
                        2 * kappa * theta < sigma * sigma):
                        return [1e6] * len(helpers)
                    
                    # Set parameters
                    model.setParams(ql.Array(list(params)))
                    
                    # Calculate errors
                    errors = []
                    for helper in helpers:
                        try:
                            error = helper.calibrationError()
                            errors.append(error)
                        except:
                            errors.append(1e6)
                    
                    return errors
                except:
                    return [1e6] * len(helpers)
            
            initial_condition = [theta_init, kappa_init, sigma_init, rho_init, v0_init]
            print(f"DEBUG: Starting {solver_method} with initial: {initial_condition}")
            
            if solver_method == 'scipy_lm':
                sol = root(cost_function, initial_condition, method='lm')
                print(f"DEBUG: SciPy LM result: success={sol.success}, x={sol.x}")
                if sol.success:
                    model.setParams(ql.Array(list(sol.x)))
                    print(f"DEBUG: Model updated with params={list(sol.x)}")
            elif solver_method == 'scipy_ls':
                sol = least_squares(cost_function, initial_condition)
                print(f"DEBUG: SciPy LS result: success={sol.success}, x={sol.x}")
                if sol.success:
                    model.setParams(ql.Array(list(sol.x)))
            elif solver_method == 'scipy_de':
                bounds = [(0.001, 0.5), (0.01, 20), (0.01, 2.0), (-0.99, 0.99), (0.001, 0.5)]
                def scalar_cost(params):
                    errors = cost_function(params)
                    return np.sqrt(np.sum(np.array(errors)**2))
                sol = differential_evolution(scalar_cost, bounds, maxiter=100)
                print(f"DEBUG: SciPy DE result: success={sol.success}, x={sol.x}")
                if sol.success:
                    model.setParams(ql.Array(list(sol.x)))
            elif solver_method == 'scipy_bh':
                bounds = [(0.001, 0.5), (0.01, 20), (0.01, 2.0), (-0.99, 0.99), (0.001, 0.5)]
                def scalar_cost(params):
                    errors = cost_function(params)
                    return np.sqrt(np.sum(np.array(errors)**2))
                sol = basinhopping(scalar_cost, initial_condition, niter=5, 
                                 minimizer_kwargs={"method": "L-BFGS-B", "bounds": bounds})
                print(f"DEBUG: SciPy BH result: success={sol.success}, x={sol.x}")
                if sol.success:
                    model.setParams(ql.Array(list(sol.x)))
        
        # Get calibrated parameters
        theta, kappa, sigma, rho, v0 = model.params()
        print(f"DEBUG: Final params: θ={theta:.4f}, κ={kappa:.4f}, σ={sigma:.4f}, ρ={rho:.4f}, v₀={v0:.4f}")
        
        # Calculate error
        avg_error = 0.0
        for helper in helpers:
            try:
                err = (helper.modelValue() / helper.marketValue() - 1.0)
                avg_error += abs(err)
            except:
                avg_error += 1.0
        avg_error = avg_error * 100.0 / len(helpers)
        print(f"DEBUG: Average error: {avg_error:.4f}%")
        
        # Calculate errors table
        errors_table = []
        for i, helper in enumerate(helpers[:8]):
            try:
                err = (helper.modelValue() / helper.marketValue() - 1.0)
                errors_table.append({
                    'strike': strikes[i % len(strikes)],
                    'market_price': f"{helper.marketValue():.4f}",
                    'model_price': f"{helper.modelValue():.4f}",
                    'rel_error_pct': f"{err*100:.2f}%"
                })
            except Exception as e:
                errors_table.append({
                    'strike': strikes[i % len(strikes)],
                    'market_price': "N/A",
                    'model_price': "N/A",
                    'rel_error_pct': f"Error: {e}"
                })
        
        return {
            'solver_method': solver_method,
            'calibrated_params': {
                'theta': theta,
                'kappa': kappa,
                'sigma': sigma,
                'rho': rho,
                'v0': v0
            },
            'params_string': f"θ={theta:.4f}, κ={kappa:.4f}, σ={sigma:.4f}, ρ={rho:.4f}, v₀={v0:.4f}",
            'avg_error': f"{avg_error:.4f}%",
            'errors_table': errors_table
        }
        
    except Exception as e:
        print(f"ERROR IN HESTON CALIBRATION: {e}")
        import traceback
        traceback.print_exc()
        return {'error': str(e)}
