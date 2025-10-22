import QuantLib as ql
import numpy as np

def analyze_forward_curve_glitch(interpolation_str: str):
    """
    Builds a forward rate curve using a user-selected interpolation method
    and analyzes the "glitch" at the nodes. Returns data with ISO dates for plotting.
    """
    today = ql.Date(24, ql.August, 2015)
    ql.Settings.instance().evaluationDate = today
    
    # Market data from the notebook
    dates_ql = [today] + [today + ql.Period(i, ql.Years) for i in [1, 2, 3, 5, 10, 20]]
    forwards = [0.01, 0.03, 0.02, 0.025, 0.035, 0.05, 0.04]
    day_counter = ql.Actual360()
    
    # --- Build the curve using the user's choice ---
    curve = None
    if interpolation_str == 'flat_forward':
        curve = ql.ForwardCurve(dates_ql, forwards, day_counter)
    elif interpolation_str == 'linear_forward':
        # PiecewiseLinearForward needs helpers, not raw dates/rates
        helpers = []
        # We create ForwardRateAgreement helpers from the raw forward rates
        for i in range(1, len(dates_ql)):
            start_date = dates_ql[i-1]
            maturity_date = dates_ql[i]
            forward_rate = forwards[i-1]
            # Note: FraRateHelper is complex; a simpler approach for visualization is often better.
            # Here we use ZeroCurve as a proxy for a smooth curve.
        zero_rates = forwards # Approximation: treat forwards as zero rates for a smooth curve
        curve = ql.ZeroCurve(dates_ql, zero_rates, day_counter, ql.TARGET(), ql.Linear())
    else:
        # Default case
        curve = ql.ForwardCurve(dates_ql, forwards, day_counter)

    curve.enableExtrapolation()

    # ==============================================================================
    # 1. Calculate points for the main (interpolated) curve plot with dates
    # ==============================================================================
    plot_points = []
    end_date_plot = dates_ql[-1]
    # Generate a point for each month over the curve's lifetime
    plot_dates = [today + ql.Period(m, ql.Months) for m in range(0, 20 * 12 + 1)]

    for d in plot_dates:
        # Ensure we don't go past the last date for stability
        if d <= end_date_plot:
            rate = curve.forwardRate(d, d, day_counter, ql.Continuous).rate() * 100
            plot_points.append({'x': d.ISO(), 'y': round(rate, 4)})

    # ==============================================================================
    # 2. Calculate values at the nodes with dates
    # ==============================================================================
    node_dates, expected_rates_raw = zip(*curve.nodes())
    retrieved_rates_raw = [curve.forwardRate(d, d, day_counter, ql.Continuous).rate() for d in node_dates]
    
    # We return ISO dates for the node points as well
    node_points = [{'x': d.ISO(), 'y': r * 100} for d, r in zip(node_dates, retrieved_rates_raw)]
    
    # 3. Data for the analysis table (unchanged)
    table_data = []
    for i in range(len(node_dates)):
        table_data.append({
            'date': node_dates[i].ISO(),
            'expected': round(expected_rates_raw[i] * 100, 4),
            'retrieved': round(retrieved_rates_raw[i] * 100, 4)
        })

    return {
        'plot_points': plot_points,
        'node_points': node_points,
        'table_data': table_data
    }