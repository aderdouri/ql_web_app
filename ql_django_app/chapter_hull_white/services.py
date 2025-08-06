import QuantLib as ql
import numpy as np

def run_hull_white_simulation(a, sigma, forward_rate, length_years, num_paths, timestep):
    """
    Simule des chemins de taux courts en utilisant le modèle de Hull-White.
    """
    day_count = ql.Thirty360(ql.Thirty360.BondBasis)
    todays_date = ql.Date(15, 1, 2015)
    ql.Settings.instance().evaluationDate = todays_date

    spot_curve = ql.FlatForward(todays_date, ql.QuoteHandle(ql.SimpleQuote(forward_rate)), day_count)
    spot_curve_handle = ql.YieldTermStructureHandle(spot_curve)

    hw_process = ql.HullWhiteProcess(spot_curve_handle, a, sigma)
    
    rng = ql.GaussianRandomSequenceGenerator(ql.UniformRandomSequenceGenerator(timestep, ql.UniformRandomGenerator(42)))
    seq = ql.GaussianPathGenerator(hw_process, length_years, timestep, rng, False)

    # Génération des chemins
    paths = np.zeros((num_paths, timestep + 1))
    for i in range(num_paths):
        sample_path = seq.next().value()
        paths[i, :] = np.array(list(sample_path))
    
    # Récupération de l'axe du temps
    time_grid = np.array([sample_path.time(j) for j in range(timestep + 1)])
    
    # Calculs statistiques
    avg_path = np.mean(paths, axis=0)
    var_path = np.var(paths, axis=0)
    
    def alpha(t):
        return forward_rate + 0.5 * np.power(sigma/a * (1.0 - np.exp(-a*t)), 2)
    
    theoretical_mean = alpha(time_grid)
    theoretical_var = sigma * sigma / (2*a) * (1.0 - np.exp(-2.0 * a * time_grid))

    return {
        'time_grid': list(time_grid),
        'paths': paths.tolist(),
        'avg_path': list(avg_path),
        'var_path': list(var_path),
        'theoretical_mean': list(theoretical_mean),
        'theoretical_var': list(theoretical_var)
    }