import QuantLib as ql
import numpy as np
from datetime import date

def analyze_forward_curve_glitch():
    """
    Builds a forward curve and extracts data to demonstrate the interpolation glitch.
    """
    today = ql.Date(24, ql.August, 2015)
    ql.Settings.instance().evaluationDate = today
    
    # 1. Curve data from the notebook
    dates_ql = [ today ] + [ today + ql.Period(i, ql.Years) for i in [1, 2, 3, 5, 10, 20] ]
    forwards = [ 0.01, 0.03, 0.02, 0.025, 0.035, 0.05, 0.04 ]
    
    curve = ql.ForwardCurve(dates_ql, forwards, ql.Actual360())
    
    # 2. Calculate points for the main "glitched" curve plot
    sample_times = np.linspace(0.0, 20.0, 401)
    sample_rates = [curve.forwardRate(t, t, ql.Continuous).rate() * 100 for t in sample_times]
    
    plot_points = [{'x': t, 'y': s} for t, s in zip(sample_times, sample_rates)]
    
    # 3. Calculate the "stepped" true forward curve for comparison
    true_nodes = list(curve.nodes())
    true_plot_points = []
    for i in range(len(true_nodes)-1):
        d1, r1 = true_nodes[i]
        d2, _ = true_nodes[i+1]
        t1 = curve.dayCounter().yearFraction(today, d1)
        t2 = curve.dayCounter().yearFraction(today, d2)
        true_plot_points.append({'x': t1, 'y': r1 * 100})
        true_plot_points.append({'x': t2, 'y': r1 * 100})

    # 4. Prepare data for the analysis table
    node_dates, expected_rates = zip(*true_nodes)
    retrieved_rates = [curve.forwardRate(d, d, curve.dayCounter(), ql.Continuous).rate() for d in node_dates]
    
    table_data = []
    for i in range(len(node_dates)):
        table_data.append({
            'date': node_dates[i].ISO(),
            'expected': round(expected_rates[i] * 100, 4),
            'retrieved': round(retrieved_rates[i] * 100, 4)
        })

    return {
        'plot_points': plot_points,
        'true_plot_points': true_plot_points,
        'table_data': table_data
    }