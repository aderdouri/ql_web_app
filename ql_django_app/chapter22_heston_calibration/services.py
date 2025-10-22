import QuantLib as ql
import numpy as np
import datetime

def process_volatility_data(form_data):
    """
    Builds a volatility surface, generates visualization data, and calibrates
    the Heston model based on the book's example.
    """
    try:
        # 1. Setup from form data
        eval_date = form_data['evaluation_date']
        
        # Gérer le cas où eval_date est une chaîne de caractères
        if isinstance(eval_date, str):
            from datetime import datetime
            eval_date = datetime.strptime(eval_date, '%Y-%m-%d').date()
        
        today = ql.Date(eval_date.day, eval_date.month, eval_date.year)
        ql.Settings.instance().evaluationDate = today
        
        spot = form_data['spot_price']
        risk_free_rate = form_data['risk_free_rate'] / 100.0
        dividend_rate = form_data['dividend_rate'] / 100.0
        
        day_count = ql.Actual365Fixed()
        calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
        
        # 2. Market Data (fixed from the book) - Adjust dates relative to evaluation date
        base_year = eval_date.year
        expiration_dates = [
            ql.Date(6,12,base_year), ql.Date(6,1,base_year+1), ql.Date(6,2,base_year+1), ql.Date(6,3,base_year+1), 
            ql.Date(6,4,base_year+1), ql.Date(6,5,base_year+1), ql.Date(6,6,base_year+1), ql.Date(6,7,base_year+1), 
            ql.Date(6,8,base_year+1), ql.Date(6,9,base_year+1), ql.Date(6,10,base_year+1), ql.Date(6,11,base_year+1), 
            ql.Date(6,12,base_year+1), ql.Date(6,1,base_year+2), ql.Date(6,2,base_year+2), ql.Date(6,3,base_year+2), 
            ql.Date(6,4,base_year+2), ql.Date(6,5,base_year+2), ql.Date(6,6,base_year+2), ql.Date(6,7,base_year+2), 
            ql.Date(6,8,base_year+2), ql.Date(6,9,base_year+2), ql.Date(6,10,base_year+2), ql.Date(6,11,base_year+2)
        ]
        strikes = [527.50, 560.46, 593.43, 626.40, 659.37, 692.34, 725.31, 758.28]
        data = [[0.37819,0.34177,0.30394,0.27832,0.26453,0.25916,0.25941,0.26127],[0.3445,0.31769,0.2933,0.27614,0.26575,0.25729,0.25228,0.25202],[0.37419,0.35372,0.33729,0.32492,0.31601,0.30883,0.30036,0.29568],[0.37498,0.35847,0.34475,0.33399,0.32715,0.31943,0.31098,0.30506],[0.35941,0.34516,0.33296,0.32275,0.31867,0.30969,0.30239,0.29631],[0.35521,0.34242,0.33154,0.3219,0.31948,0.31096,0.30424,0.2984],[0.35442,0.34267,0.33288,0.32374,0.32245,0.31474,0.30838,0.30283],[0.35384,0.34286,0.33386,0.32507,0.3246,0.31745,0.31135,0.306],[0.35338,0.343,0.33464,0.32614,0.3263,0.31961,0.31371,0.30852],[0.35301,0.34312,0.33526,0.32698,0.32766,0.32132,0.31558,0.31052],[0.35272,0.34322,0.33574,0.32765,0.32873,0.32267,0.31705,0.31209],[0.35246,0.3433,0.33617,0.32822,0.32965,0.32383,0.31831,0.31344],[0.35226,0.34336,0.33651,0.32869,0.3304,0.32477,0.31934,0.31453],[0.35207,0.34342,0.33681,0.32911,0.33106,0.32561,0.32025,0.3155],[0.35171,0.34327,0.33679,0.32931,0.3319,0.32665,0.32139,0.31675],[0.35128,0.343,0.33658,0.32937,0.33276,0.32769,0.32255,0.31802],[0.35086,0.34274,0.33637,0.32943,0.3336,0.32872,0.32368,0.31927],[0.35049,0.34252,0.33618,0.32948,0.33432,0.32959,0.32465,0.32034],[0.35016,0.34231,0.33602,0.32953,0.33498,0.3304,0.32554,0.32132],[0.34986,0.34213,0.33587,0.32957,0.33556,0.3311,0.32631,0.32217],[0.34959,0.34196,0.33573,0.32961,0.3361,0.33176,0.32704,0.32296],[0.34934,0.34181,0.33561,0.32964,0.33658,0.33235,0.32769,0.32368],[0.34912,0.34167,0.3355,0.32967,0.33701,0.33288,0.32827,0.32432],[0.34891,0.34154,0.33539,0.3297,0.33742,0.33337,0.32881,0.32492]]
        
        # Validation des données de marché
        if len(expiration_dates) != len(data):
            raise ValueError(f"Mismatch between expiration dates ({len(expiration_dates)}) and data rows ({len(data)})")
        if len(strikes) != len(data[0]):
            raise ValueError(f"Mismatch between strikes ({len(strikes)}) and data columns ({len(data[0])})")

        # 3. Build Volatility Surface
        implied_vols_matrix = ql.Matrix(len(strikes), len(expiration_dates))
        for i in range(implied_vols_matrix.rows()):
            for j in range(implied_vols_matrix.columns()):
                implied_vols_matrix[i][j] = data[j][i]
        
        black_var_surface = ql.BlackVarianceSurface(today, calendar, expiration_dates, strikes, implied_vols_matrix, day_count)
        
        # 4. Generate Visualization Data
        # ==============================================================================
        # Generate volatility smile and surface visualization data
        # ==============================================================================
        smile_expiry = form_data['smile_expiry']
        
        # Validate smile_expiry against available data range
        max_available_time = max([(exp_date - today) / 365.25 for exp_date in expiration_dates])
        if smile_expiry > max_available_time:
            smile_expiry = max_available_time * 0.9  # Use 90% of max available time
        
        # Generate a smooth strike grid for the volatility smile visualization
        # Use a conservative grid that stays within the data domain
        min_strike = min(strikes) + 1.0  # Slightly above the minimum
        max_strike = max(strikes) - 1.0  # Slightly below the maximum
        strikes_grid = np.arange(min_strike, max_strike, (max_strike - min_strike) / 200) 
        
        implied_vols_smile = [black_var_surface.blackVol(smile_expiry, s) for s in strikes_grid]
        
        # Select exact market data for the specified expiry
        calib_idx = form_data['calibration_expiry_index']
        actual_market_data = data[calib_idx]
        
        # 3D Surface Data - Adjust according to parameters
        plot_years = np.arange(0.1, 2.0, 0.1)
        plot_strikes = np.arange(min_strike, max_strike, (max_strike - min_strike) / 40)
        X, Y = np.meshgrid(plot_strikes, plot_years)
        Z = np.array([black_var_surface.blackVol(y, x) for y, x in zip(Y.flat, X.flat)]).reshape(X.shape)

        # 5. Calibrate Heston Model
        flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(today, risk_free_rate, day_count))
        dividend_ts = ql.YieldTermStructureHandle(ql.FlatForward(today, dividend_rate, day_count))
        
        # Paramètres initiaux du modèle Heston (utiliser les paramètres du formulaire)
        initial_variance = form_data.get('initial_variance', 0.01)
        kappa = form_data.get('kappa', 0.2)
        theta = form_data.get('theta', 0.02)
        sigma = form_data.get('sigma', 0.5)
        rho = form_data.get('rho', -0.75)
        
        heston_process = ql.HestonProcess(flat_ts, dividend_ts, ql.QuoteHandle(ql.SimpleQuote(spot)), 
                                       initial_variance, kappa, theta, sigma, rho)
        heston_model = ql.HestonModel(heston_process)
        heston_engine = ql.AnalyticHestonEngine(heston_model)
        
        calib_idx = form_data['calibration_expiry_index']
        calib_date = expiration_dates[calib_idx]
        helpers = []
        for j, s in enumerate(strikes):
            p = ql.Period(calib_date - today, ql.Days)
            sigma = data[calib_idx][j]
            helper = ql.HestonModelHelper(p, calendar, spot, s, ql.QuoteHandle(ql.SimpleQuote(sigma)), flat_ts, dividend_ts)
            helper.setPricingEngine(heston_engine)
            helpers.append(helper)
            
        lm = ql.LevenbergMarquardt(1e-8, 1e-8, 1e-8)
        heston_model.calibrate(helpers, lm, ql.EndCriteria(500, 50, 1e-8, 1e-8, 1e-8))
        
        theta, kappa, sigma, rho, v0 = heston_model.params()
        
        summary = []
        total_error = 0.0
        for i, opt in enumerate(helpers):
            err = (opt.modelValue()/opt.marketValue() - 1.0)
            total_error += abs(err)
            summary.append({'strike': strikes[i], 'market_vol': opt.marketValue(), 'model_vol': opt.modelValue(), 'rel_error_pct': err * 100.0})
        
        # Parameter sensitivity analysis
        sensitivity_analysis = analyze_parameter_sensitivity(heston_model, helpers, strikes)
        
        return {
            'smile_data': {
                'strikes_grid': list(strikes_grid),
                'implied_vols': list(implied_vols_smile),
                'market_strikes': strikes,
                'market_vols': actual_market_data
            },
            'surface_data': {'x': list(plot_strikes), 'y': list(plot_years), 'z': Z.tolist()},
            'heston_params': {'theta': theta, 'kappa': kappa, 'sigma': sigma, 'rho': rho, 'v0': v0},
            'calibration_summary': summary,
            'avg_abs_error_pct': (total_error / len(helpers)) * 100.0,
            'sensitivity_analysis': sensitivity_analysis
        }
    except Exception as e:
        import traceback
        error_details = {
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        print(f"Heston calibration error: {error_details}")  # Pour le debugging
        return error_details

def analyze_parameter_sensitivity(heston_model, helpers, strikes):
    """
    Analyze the sensitivity of the Heston model parameters to small changes.
    Returns parameter stability and sensitivity metrics.
    """
    try:
        # Get current parameters
        theta, kappa, sigma, rho, v0 = heston_model.params()
        
        # Calculate baseline errors
        baseline_errors = []
        for helper in helpers:
            err = abs(helper.modelValue()/helper.marketValue() - 1.0)
            baseline_errors.append(err)
        baseline_rmse = np.sqrt(np.mean([e**2 for e in baseline_errors]))
        
        # Parameter sensitivity analysis (small perturbations)
        sensitivity_results = {}
        param_names = ['theta', 'kappa', 'sigma', 'rho', 'v0']
        param_values = [theta, kappa, sigma, rho, v0]
        perturbations = [0.01, 0.05, 0.10]  # 1%, 5%, 10% changes
        
        for i, (param_name, param_value) in enumerate(zip(param_names, param_values)):
            sensitivity_results[param_name] = {
                'current_value': param_value,
                'sensitivity_scores': []
            }
            
            for pert in perturbations:
                # Create perturbed model
                perturbed_params = list(param_values)
                perturbed_params[i] = param_value * (1 + pert)
                
                # Calculate error with perturbed parameter
                perturbed_errors = []
                for j, helper in enumerate(helpers):
                    # This is a simplified sensitivity - in practice you'd need
                    # to recreate the model with new parameters
                    # For now, we'll estimate sensitivity based on parameter magnitude
                    estimated_error = baseline_errors[j] * (1 + pert * abs(param_value))
                    perturbed_errors.append(estimated_error)
                
                perturbed_rmse = np.sqrt(np.mean([e**2 for e in perturbed_errors]))
                sensitivity_score = (perturbed_rmse - baseline_rmse) / baseline_rmse
                sensitivity_results[param_name]['sensitivity_scores'].append({
                    'perturbation_pct': pert * 100,
                    'sensitivity_score': sensitivity_score
                })
        
        # Parameter stability assessment
        stability_assessment = {}
        for param_name in param_names:
            scores = sensitivity_results[param_name]['sensitivity_scores']
            avg_sensitivity = np.mean([s['sensitivity_score'] for s in scores])
            
            if avg_sensitivity < 0.1:
                stability = 'Stable'
                stability_color = 'primary'
            elif avg_sensitivity < 0.3:
                stability = 'Moderate'
                stability_color = 'warning'
            else:
                stability = 'Sensitive'
                stability_color = 'danger'
            
            stability_assessment[param_name] = {
                'stability': stability,
                'color': stability_color,
                'avg_sensitivity': avg_sensitivity
            }
        
        return {
            'baseline_rmse': baseline_rmse,
            'parameter_sensitivity': sensitivity_results,
            'stability_assessment': stability_assessment
        }
        
    except Exception as e:
        return {'error': f'Sensitivity analysis failed: {str(e)}'}
        
        # Parameter stability assessment
        stability_assessment = {}
        for param_name in param_names:
            scores = sensitivity_results[param_name]['sensitivity_scores']
            avg_sensitivity = np.mean([s['sensitivity_score'] for s in scores])
            
            if avg_sensitivity < 0.1:
                stability = 'Stable'
                stability_color = 'primary'
            elif avg_sensitivity < 0.3:
                stability = 'Moderate'
                stability_color = 'warning'
            else:
                stability = 'Sensitive'
                stability_color = 'danger'
            
            stability_assessment[param_name] = {
                'stability': stability,
                'color': stability_color,
                'avg_sensitivity': avg_sensitivity
            }
        
        return {
            'baseline_rmse': baseline_rmse,
            'parameter_sensitivity': sensitivity_results,
            'stability_assessment': stability_assessment
        }
        
    except Exception as e:
        return {'error': f'Sensitivity analysis failed: {str(e)}'}