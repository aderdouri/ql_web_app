# hw_convergence/services.py (VERSION EXACTE DU LIVRE)

import QuantLib as ql
import numpy as np
from scipy.integrate import simpson
import datetime
import math

def analyze_hull_white_convergence(data):
    try:
        print(f"DEBUG: Starting analysis with data: {data}")
        
        # 1. Setup from form data
        experiment_type = data['experiment_type']; eval_date = data['evaluation_date']
        today = ql.Date(eval_date.day, eval_date.month, eval_date.year); ql.Settings.instance().evaluationDate = today
        num_paths = data['num_paths']; length = data['simulation_length']
        timestep = data['time_steps']; forward_rate = data['forward_rate']; seed = data['random_seed']
        day_count = ql.Thirty360(ql.Thirty360.BondBasis)
        spot_curve_handle = ql.YieldTermStructureHandle(ql.FlatForward(today, ql.QuoteHandle(ql.SimpleQuote(forward_rate)), day_count))
        
        print(f"DEBUG: experiment_type={experiment_type}, num_paths={num_paths}, timestep={timestep}")

        # ==============================================================================
        # CORRECTION EXACTE : Grille du livre (commence à 1 pour std_dev, 12 pour les autres)
        # ==============================================================================
        if experiment_type == 'std_dev':
            avg_grid_array = np.arange(1, timestep + 1, 12, dtype=int)
        else:
            avg_grid_array = np.arange(12, timestep + 1, 12, dtype=int)

        def get_path_generator(hw_process):
            usg = ql.UniformRandomSequenceGenerator(timestep, ql.UniformRandomGenerator())
            rng = ql.GaussianRandomSequenceGenerator(usg)
            return ql.GaussianPathGenerator(hw_process, length, timestep, rng, False)

        def generate_paths(seq, num_paths_gen):
            time, paths = [], np.zeros((num_paths_gen, timestep + 1))
            for i in range(num_paths_gen):
                sample_path = seq.next().value()
                if not time: time = [sample_path.time(j) for j in range(len(sample_path))]
                paths[i, :] = np.array([sample_path[j] for j in range(len(sample_path))])
            return np.array(time), paths

        def generate_paths_zero_price(hw_process, num_paths_gen):
            seq = get_path_generator(hw_process)
            time, paths = generate_paths(seq, num_paths_gen)
            
            # ==============================================================================
            # CORRECTION EXACTE : Reproduire exactement la fonction du livre
            # ==============================================================================
            avgs = [(time[j], np.mean([math.exp(-simpson(paths[i][0:j], x=time[0:j])) for i in range(num_paths_gen)])) for j in avg_grid_array]
            return zip(*avgs)

        def generate_paths_discount_factors(hw_process, num_paths_gen):
            seq = get_path_generator(hw_process)
            time, paths = generate_paths(seq, num_paths_gen)
            
            arr = np.zeros((num_paths_gen, len(avg_grid_array)))
            for i in range(num_paths_gen):
                arr[i, :] = [math.exp(-simpson(paths[i][0:j], x=time[0:j])) for j in avg_grid_array]
            
            t_array = [time[j] for j in avg_grid_array]
            return t_array, arr

        # ==============================================================================
        # CORRECTION EXACTE : Fonction V(t,T) du livre
        # ==============================================================================
        def V(t, T, a, sigma):
            return sigma*sigma/a/a*(T-t + 2.0/a*math.exp(-a*(T-t)) - 1.0/(2.0*a)*math.exp(-2.0*a*(T-t)) - 3.0/(2.0*a))

        results = {'experiment_type': experiment_type, 'plots': []}
        print(f"DEBUG: Created results dict: {results}")

        if experiment_type == 'vary_sigma':
            print("DEBUG: Processing vary_sigma experiment")
            a = data['a']
            sigma_array = np.arange(0.01, 0.1, 0.03)
            # Calcul théorique exact du livre
            zero_price_theory = np.array([spot_curve_handle.discount(j*float(length)/float(timestep)) for j in avg_grid_array])
            for s in sigma_array:
                hw_process = ql.HullWhiteProcess(spot_curve_handle, a, s)
                time, zero_price_empirical = generate_paths_zero_price(hw_process, num_paths)
                error = np.abs(zero_price_theory - np.array(zero_price_empirical))
                results['plots'].append({'label': f'σ = {s:.2f}', 'time': list(time), 'error': list(error)})

        elif experiment_type == 'vary_a':
            print("DEBUG: Processing vary_a experiment")
            sigma = data['sigma']
            a_array = np.arange(0.1, 0.51, 0.1)
            # Calcul théorique exact du livre
            zero_price_theory = np.array([spot_curve_handle.discount(j*float(length)/float(timestep)) for j in avg_grid_array])
            for mean_rev in a_array:
                hw_process = ql.HullWhiteProcess(spot_curve_handle, mean_rev, sigma)
                time, zero_price_empirical = generate_paths_zero_price(hw_process, num_paths)
                error = np.abs(zero_price_theory - np.array(zero_price_empirical))
                results['plots'].append({'label': f'a = {mean_rev:.2f}', 'time': list(time), 'error': list(error)})
        
        elif experiment_type == 'std_dev':
            a = data['a']; sigma = data['sigma']
            hw_process = ql.HullWhiteProcess(spot_curve_handle, a, sigma)
            term, discount_factor_matrix = generate_paths_discount_factors(hw_process, num_paths)
            
            # Calcul empirique
            vol = [np.var(discount_factor_matrix[:, i]) for i in range(len(term))]
            empirical_std_dev = [100*np.sqrt(v) for v in vol]
            
            # Calcul théorique
            theory_std_dev = [100*np.sqrt(math.exp(V(0,T,a,sigma))-1.0) * spot_curve_handle.discount(T) for T in term]
            
            results['plots'] = [
                {'label': 'Empirical', 'time': list(term), 'values': empirical_std_dev},
                {'label': 'Theory', 'time': list(term), 'values': theory_std_dev}
            ]

        print(f"DEBUG: Final results: {results}")
        return results
    except Exception as e:
        print(f"DEBUG: Exception occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'error': str(e)}