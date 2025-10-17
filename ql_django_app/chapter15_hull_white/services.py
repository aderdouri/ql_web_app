import QuantLib as ql
import numpy as np
import datetime

def simulate_hull_white_paths(data):
    try:
        today = ql.Date(data['evaluation_date'].day, data['evaluation_date'].month, data['evaluation_date'].year)
        ql.Settings.instance().evaluationDate = today

        sigma = data['sigma']; a = data['a']
        length = data['simulation_length']
        timestep = data['timestep'] # On utilise directement le timestep total
        forward_rate = data['forward_rate']
        num_paths = data['num_paths']
        seed = data['random_seed']
        day_count = ql.Thirty360(ql.Thirty360.BondBasis)

        spot_curve_handle = ql.YieldTermStructureHandle(ql.FlatForward(today, ql.QuoteHandle(ql.SimpleQuote(forward_rate)), day_count))
        hw_process = ql.HullWhiteProcess(spot_curve_handle, a, sigma)

        rng = ql.GaussianRandomSequenceGenerator(ql.UniformRandomSequenceGenerator(timestep, ql.UniformRandomGenerator(seed)))
        seq = ql.GaussianPathGenerator(hw_process, length, timestep, rng, False)

        def generate_paths(num_paths_to_gen, ts):
            arr = np.zeros((num_paths_to_gen, ts + 1))
            time = []
            for i in range(num_paths_to_gen):
                sample_path = seq.next()
                path = sample_path.value()
                if not time: time = [path.time(j) for j in range(len(path))]
                value = [path[j] for j in range(len(path))]
                arr[i, :] = np.array(value)
            return np.array(time), arr

        time, paths = generate_paths(num_paths, timestep)

        simulated_mean = [np.mean(paths[:, i]) for i in range(timestep + 1)]
        simulated_variance = [np.var(paths[:, i]) for i in range(timestep + 1)]

        def theoretical_alpha(fwd, s, mean_rev, t):
            term = s/mean_rev * (1.0 - np.exp(-mean_rev * t))
            return fwd + 0.5 * term * term

        time_array = np.array(time)
        theoretical_mean = theoretical_alpha(forward_rate, sigma, a, time_array)
        theoretical_variance = (sigma*sigma)/(2*a)*(1.0 - np.exp(-2.0 * a * time_array))

        return {
            'simulation_paths': paths[:10].tolist(),
            'time_grid': list(time),
            'analysis': {
                'simulated_mean': list(simulated_mean),
                'theoretical_mean': list(theoretical_mean),
                'simulated_variance': list(simulated_variance),
                'theoretical_variance': list(theoretical_variance),
            }
        }
    except Exception as e:
        return {'error': str(e)}