# Fichier : ql_web_app/chapter_mc_convergence/services.py (VERSION COMPLÈTE)
import QuantLib as ql
import numpy as np
from scipy.integrate import simpson
import math

# ==============================================================================
# LES FONCTIONS UTILITAIRES MANQUANTES SONT AJOUTÉES ICI
# ==============================================================================

def get_path_generator(timestep, hw_process, length, seed):
    """
    Crée un générateur de chemins Monte Carlo (pseudo-aléatoire).
    """
    usg = ql.UniformRandomSequenceGenerator(timestep, ql.UniformRandomGenerator(seed))
    rng = ql.GaussianRandomSequenceGenerator(usg)
    return ql.GaussianPathGenerator(hw_process, length, timestep, rng, False)

def generate_paths(num_paths, timestep, seq):
    """
    Génère un nombre spécifié de trajectoires à partir d'un générateur de chemins.
    """
    arr = np.zeros((num_paths, timestep + 1))
    for i in range(num_paths):
        path = seq.next().value()
        arr[i, :] = np.array(list(path))
    time = np.array(list(seq.timeGrid()))
    return time, arr


# --- Fonction principale du service (maintenant elle trouvera les fonctions ci-dessus) ---
def run_convergence_experiment(experiment_type: str, a: float, sigma: float, num_paths: int, seed: int):
    """
    Exécute une expérience de convergence Monte Carlo pour Hull-White.
    """
    # --- Setup commun ---
    today = ql.Date(15, 1, 2015)
    ql.Settings.instance().evaluationDate = today
    timestep = 180
    length = 15
    forward_rate = 0.05
    day_count = ql.Thirty360(ql.Thirty360.BondBasis)
    avg_grid_array = np.arange(12, timestep + 1, 12)
    
    spot_curve = ql.FlatForward(today, ql.QuoteHandle(ql.SimpleQuote(forward_rate)), day_count)
    spot_curve_handle = ql.YieldTermStructureHandle(spot_curve)

    if experiment_type == 'vary_sigma':
        plots = []
        sigma_array = np.arange(0.01, 0.1, 0.03)
        for s_exp in sigma_array:
            hw_process = ql.HullWhiteProcess(spot_curve_handle, abs(a), abs(s_exp))
            seq = get_path_generator(timestep, hw_process, length, seed)
            time, paths = generate_paths(num_paths, timestep, seq)
            
            zero_price_theory = np.array([spot_curve.discount(time[j]) for j in avg_grid_array])
            avgs = [np.mean([math.exp(-simpson(paths[i, :j+1], x=time[:j+1])) for i in range(num_paths)]) for j in avg_grid_array]
            term = [time[j] for j in avg_grid_array]
            errors = np.abs(zero_price_theory - np.array(avgs))
            
            plots.append({'label': f'Sigma = {s_exp:.2f}', 'points': [{'x': t, 'y': e} for t, e in zip(term, errors)]})
        return {'title': f'DF Error for a={a:.2f}', 'plots': plots, 'y_axis': 'Absolute Error |ε(T)|'}

    elif experiment_type == 'vol_dist':
        hw_process = ql.HullWhiteProcess(spot_curve_handle, abs(a), abs(sigma))
        seq = get_path_generator(timestep, hw_process, length, seed)
        time, paths = generate_paths(num_paths, timestep, seq)
        
        discount_factor_matrix = np.array([[np.exp(-simpson(paths[i, :j+1], x=time[:j+1])) for j in avg_grid_array] for i in range(num_paths)])
        term = [time[j] for j in avg_grid_array]
        
        vol_empirical = [np.var(discount_factor_matrix[:, i]) for i in range(len(term))]
        vol_empirical_sqrt = 100 * np.sqrt(vol_empirical)

        V = lambda t, T, a_param, sigma_param: sigma_param**2/a_param**2 * (T-t + 2/a_param*math.exp(-a_param*(T-t)) - 1/(2*a_param)*math.exp(-2*a_param*(T-t)) - 3/(2*a_param))
        vol_theory = [100*np.sqrt(math.exp(V(0,T,a,sigma))-1.0) * spot_curve_handle.discount(T) for T in term]

        return {
            'title': f'Discount Factor StdDev (a={a:.2f}, σ={sigma:.2f})',
            'plots': [
                {'label': 'Empirical Vol', 'points': [{'x': t, 'y': v} for t, v in zip(term, vol_empirical_sqrt)]},
                {'label': 'Theoretical Vol', 'points': [{'x': t, 'y': v} for t, v in zip(term, vol_theory)]}
            ],
            'y_axis': 'Std Dev σ_D(0,T) (%)'
        }
    
    return {}