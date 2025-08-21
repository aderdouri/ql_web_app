# File: ql_web_app/chapter_hull_white/services.py

import QuantLib as ql
from collections import namedtuple
import math
import numpy as np

# --- FUNCTION 1: For the Calibration Lab ---
def calibrate_hull_white_model():
    """
    Calibrates a Hull-White model to a set of market swaption volatilities.
    """
    today = ql.Date(15, 2, 2002)
    settlement = ql.Date(19, 2, 2002)
    ql.Settings.instance().evaluationDate = today
    term_structure = ql.YieldTermStructureHandle(
        ql.FlatForward(settlement, 0.04875825, ql.Actual365Fixed())
    )
    index = ql.Euribor1Y(term_structure)

    CalibrationData = namedtuple("CalibrationData", "start, length, volatility")
    data = [
        CalibrationData(1, 5, 0.1148), CalibrationData(2, 4, 0.1108),
        CalibrationData(3, 3, 0.1070), CalibrationData(4, 2, 0.1021),
        CalibrationData(5, 1, 0.1000)
    ]

    model = ql.HullWhite(term_structure)
    engine = ql.JamshidianSwaptionEngine(model)
    
    helpers = [
        ql.SwaptionHelper(
            ql.Period(d.start, ql.Years), ql.Period(d.length, ql.Years),
            ql.QuoteHandle(ql.SimpleQuote(d.volatility)),
            index, ql.Period(1, ql.Years), ql.Actual360(),
            ql.Actual360(), term_structure
        ) for d in data
    ]

    for h in helpers:
        h.setPricingEngine(engine)

    method = ql.LevenbergMarquardt()
    end_criteria = ql.EndCriteria(1000, 100, 1e-6, 1e-8, 1e-8)
    model.calibrate(helpers, method, end_criteria)

    alpha, sigma = model.params()
    
    errors = []
    for i, s in enumerate(helpers):
        model_price = s.modelValue()
        market_price = s.marketValue()
        error = model_price - market_price
        errors.append({
            'instrument': f"{data[i].start}Y into {data[i].length}Y Swaption",
            'market_vol': f"{data[i].volatility*100:.2f}%",
            'model_price': f"{model_price:.4f}",
            'market_price': f"{market_price:.4f}",
            'error': f"{error:.6f}"
        })
    
    return {
        'calibrated_alpha': round(alpha, 4),
        'calibrated_sigma': round(sigma, 4),
        'errors': errors
    }

# --- FUNCTION 2: For the Simulation Lab ---
def simulate_hull_white_paths(alpha, sigma, num_paths, num_years, seed):
    """
    Simulates multiple future paths for the short-term interest rate
    according to the Hull-White model.
    """
    today = ql.Date(15, 5, 2015)
    ql.Settings.instance().evaluationDate = today
    
    # 1. Initial flat yield curve
    risk_free_curve = ql.FlatForward(today, 0.005, ql.Actual365Fixed())
    risk_free_handle = ql.YieldTermStructureHandle(risk_free_curve)
    
    # 2. Hull-White process with user parameters
    process = ql.HullWhiteProcess(risk_free_handle, alpha, sigma)
    
    # 3. Time grid for the simulation
    timestep = 360 # Number of steps per year
    length = num_years # Number of years
    times = ql.TimeGrid(length, timestep)
    
    # 4. Random sequence generator
    # ==============================================================================
    # THE CORRECTION IS HERE: The dimensionality must be equal to 'timestep'
    # ==============================================================================
    rng = ql.GaussianRandomSequenceGenerator(
        ql.UniformRandomSequenceGenerator(timestep, ql.UniformRandomGenerator(seed))
    )
    
    # 5. Path generator
    seq = ql.GaussianPathGenerator(process, length, timestep, rng, False)
    
    # 6. Simulate the paths
    paths = []
    for i in range(num_paths):
        path = seq.next().value()
        paths.append([risk_free_curve.zeroRate(0, ql.Continuous).rate()] + list(path))

    # 7. Prepare data for plotting
    time_points = list(times)
    plot_data = []
    for i in range(num_paths):
        # We take a sample of points to keep the chart light
        path_points = [{'x': t, 'y': p * 100} for t, p in zip(time_points, paths[i])][::10]
        plot_data.append({'path_name': f'Path {i+1}', 'points': path_points})

    return plot_data