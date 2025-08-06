import QuantLib as ql
import numpy as np

def analyze_forward_curve_glitch():
    """
    Builds a forward rate curve and analyzes the interpolation "glitch"
    at the nodes, as shown in the notebook. This function is static and
    does not take user input.
    """
    
    today = ql.Date(15, 5, 2015)
    ql.Settings.instance().evaluationDate = today
    
    # 1. Define the curve nodes and rates from the notebook
    dates_ql = [ today ] + [ today + ql.Period(i, ql.Years) for i in [1, 2, 3, 5, 10, 20] ]
    forwards = [ 0.01, 0.03, 0.02, 0.025, 0.035, 0.05, 0.04 ]
    
    curve = ql.ForwardCurve(dates_ql, forwards, ql.Actual360())
    
    # 2. Generate points for the main "glitched" curve plot
    sample_times = np.linspace(0.0, 20.0, 401)
    plot_points_main = [{'x': t, 'y': curve.forwardRate(t, t, ql.Continuous).rate() * 100} for t in sample_times]
    
    # 3. Generate points for the "true" expected curve and the retrieved nodes
    nodes_original = list(curve.nodes())
    node_dates, expected_rates_raw = zip(*nodes_original)
    node_times = [ curve.dayCounter().yearFraction(today, d) for d in node_dates ]
    retrieved_rates_raw = [ curve.forwardRate(d, d, curve.dayCounter(), ql.Continuous).rate() for d in node_dates]
    
    plot_points_expected = [{'x': t, 'y': r * 100} for t, r in zip(node_times, expected_rates_raw)]
    plot_points_retrieved = [{'x': t, 'y': r * 100} for t, r in zip(node_times, retrieved_rates_raw)]
    
    # 4. Prepare data for the analysis table
    table_data = []
    for i in range(len(node_dates)):
        table_data.append({
            'date': node_dates[i].ISO(),
            'expected': round(expected_rates_raw[i] * 100, 2),
            'retrieved': round(retrieved_rates_raw[i] * 100, 2)
        })

    # 5. Return all the data in a structured dictionary
    return {
        'plot_points_main': plot_points_main,
        'plot_points_expected': plot_points_expected,
        'plot_points_retrieved': plot_points_retrieved,
        'table_data': table_data
    }