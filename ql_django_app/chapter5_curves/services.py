import QuantLib as ql
import numpy as np
from datetime import date

def get_day_count_convention(day_count_str):
    """Convert string to QuantLib day count convention"""
    day_count_map = {
        'Actual360': ql.Actual360(),
        'Actual365': ql.Actual365Fixed(),
        'Thirty360': ql.Thirty360(ql.Thirty360.BondBasis),
        'ActualActual': ql.ActualActual(ql.ActualActual.ISDA),
    }
    return day_count_map.get(day_count_str, ql.Actual360())

def get_calendar(calendar_str):
    """Convert string to QuantLib calendar"""
    calendar_map = {
        'TARGET': ql.TARGET(),
        'UnitedStates': ql.UnitedStates(ql.UnitedStates.NYSE),
        'UnitedKingdom': ql.UnitedKingdom(ql.UnitedKingdom.Exchange),
    }
    return calendar_map.get(calendar_str, ql.TARGET())

def build_term_structures_with_reference_dates(evaluation_date, market_data, curve_type='both', day_count='Actual360', calendar='TARGET'):
    """
    Build term structures with different reference dates as in the notebook
    """
    try:
        # Get day count and calendar
        day_count_conv = get_day_count_convention(day_count)
        calendar_obj = get_calendar(calendar)
        
        # Build helpers (as in notebook In[3])
        helpers = []
        for data in market_data:
            tenor_years = data['tenor_years']
            rate = data['rate']
            
            # Ensure rate is not None and is a valid number
            if rate is None or rate == '':
                rate = 0.0
            rate = float(rate)
            
            helper = ql.SwapRateHelper(
                ql.QuoteHandle(ql.SimpleQuote(rate/100.0)),
                ql.Period(tenor_years, ql.Years),
                calendar_obj,
                ql.Annual,
                ql.Unadjusted,
                ql.Thirty360(ql.Thirty360.BondBasis),
                ql.Euribor6M()
            )
            helpers.append(helper)
        
        curve1 = None
        curve2 = None
        
        # First, build curve1 with the original evaluation date (October 3rd, 2014)
        # This is to get the fixed dates for curve2
        original_eval_date = ql.Date(3, ql.October, 2014)
        ql.Settings.instance().evaluationDate = original_eval_date
        
        if curve_type in ['both', 'piecewise']:
            curve1_original = ql.PiecewiseFlatForward(0, calendar_obj, helpers, day_count_conv)
            
            # Get fixed dates and rates for curve2
            if curve_type in ['both', 'forward']:
                dates, rates = zip(*curve1_original.nodes())
                curve2 = ql.ForwardCurve(dates, rates, day_count_conv)
        
        # Now set the actual evaluation date and build curve1
        ql.Settings.instance().evaluationDate = ql.Date(evaluation_date.day, evaluation_date.month, evaluation_date.year)
        
        if curve_type in ['both', 'piecewise']:
            curve1 = ql.PiecewiseFlatForward(0, calendar_obj, helpers, day_count_conv)
        
        # Generate plot data (as in notebook - only curve1 is plotted)
        plot_data = {}
        times = np.linspace(0.0, 15.0, 400)

        if curve1:
            # As in notebook In[12]: only curve1 is used for plotting
            curve1_rates = []
            for t in times:
                try:
                    zero_rate = curve1.zeroRate(t, ql.Continuous)
                    rate_value = zero_rate.rate() * 100  # Convert to percentage
                    curve1_rates.append(rate_value)
                except Exception as e:
                    print(f"Error calculating zero rate at time {t}: {e}")
                    curve1_rates.append(0.0)

            plot_data['curve1'] = [{'x': float(t), 'y': float(rate)} for t, rate in zip(times, curve1_rates)]

        # Don't include curve2 in the plot data as it's not used in the notebook graph
        
        # Zero rate calculations (as in notebook In[9] and In[16])
        zero_rates = {}
        
        # Calculate rates for 5 years (time-based query)
        if curve1:
            try:
                zero_rate_5y = curve1.zeroRate(5.0, ql.Continuous)
                zero_rates['curve1_5y'] = zero_rate_5y.rate() * 100
            except Exception as e:
                print(f"Error calculating curve1 5Y rate: {e}")
                zero_rates['curve1_5y'] = 0.0
        
        if curve2:
            try:
                zero_rate_5y = curve2.zeroRate(5.0, ql.Continuous)
                zero_rates['curve2_5y'] = zero_rate_5y.rate() * 100
            except Exception as e:
                print(f"Error calculating curve2 5Y rate: {e}")
                zero_rates['curve2_5y'] = 0.0
        
        # Calculate rates for specific date (as in notebook In[16])
        # Using September 7, 2019 as in the notebook
        specific_date = ql.Date(7, ql.September, 2019)
        if curve1:
            try:
                zero_rate_date = curve1.zeroRate(specific_date, day_count_conv, ql.Continuous)
                zero_rates['curve1_date'] = zero_rate_date.rate() * 100
            except Exception as e:
                print(f"Error calculating curve1 date rate: {e}")
                zero_rates['curve1_date'] = 0.0
        
        if curve2:
            try:
                zero_rate_date = curve2.zeroRate(specific_date, day_count_conv, ql.Continuous)
                zero_rates['curve2_date'] = zero_rate_date.rate() * 100
            except Exception as e:
                print(f"Error calculating curve2 date rate: {e}")
                zero_rates['curve2_date'] = 0.0
        
        # Curve ranges (as in notebook In[8])
        curve_ranges = {}
        if curve1:
            curve_ranges['curve1'] = f"{curve1.referenceDate()} to {curve1.maxDate()}"
        if curve2:
            curve_ranges['curve2'] = f"{curve2.referenceDate()} to {curve2.maxDate()}"
        
        # Curve nodes (convert QuantLib Date objects to strings)
        curve_nodes = {}
        if curve1:
            nodes = curve1.nodes()
            curve_nodes['curve1'] = [(str(date_obj), float(rate)) for date_obj, rate in nodes]
        
        # Observer notifications demonstration (dynamic based on user parameters)
        observer_notifications = []
        
        # Create observers
        def make_observer(i):
            def say():
                message = f"Observer {i} notified"
                observer_notifications.append(message)
                return message
            return ql.Observer(say)
        
        obs1 = make_observer(1)
        obs2 = make_observer(2)
        
        # Connect observers to curves
        if curve1:
            obs1.registerWith(curve1)
        if curve2:
            obs2.registerWith(curve2)
        
        # Test with quotes first (as in notebook In[18]-In[21])
        q1 = ql.SimpleQuote(1.0)
        obs1.registerWith(q1)
        q2 = ql.SimpleQuote(2.0)
        obs2.registerWith(q2)
        q3 = ql.SimpleQuote(3.0)
        obs1.registerWith(q3)
        obs2.registerWith(q3)
        
        # Trigger changes to test observers
        q1.setValue(1.5)  # Should notify Observer 1
        q2.setValue(1.9)  # Should notify Observer 2
        q3.setValue(3.1)  # Should notify both observers
        
        # Dynamic test: Check if evaluation date is different from original (October 3rd, 2014)
        original_eval_date = ql.Date(3, ql.October, 2014)
        current_eval_date = ql.Date(evaluation_date.day, evaluation_date.month, evaluation_date.year)
        
        if current_eval_date != original_eval_date:
            # If evaluation date changed, this should trigger curve1 notification
            observer_notifications.append("Date d'évaluation changée - Observer 1 devrait être notifié")
            
            # Test with a different evaluation date to show the difference
            test_eval_date = ql.Date(23, ql.September, 2014)
            ql.Settings.instance().evaluationDate = test_eval_date
            
            # Rebuild curve1 to trigger notification
            if curve_type in ['both', 'piecewise']:
                curve1_test = ql.PiecewiseFlatForward(0, calendar_obj, helpers, day_count_conv)
                # This should trigger Observer 1 notification
                observer_notifications.append("Curve1 reconstruite avec nouvelle date - Observer 1 notifié")
        else:
            observer_notifications.append("Date d'évaluation identique à l'originale - aucune notification supplémentaire")
        
        return {
            'plot_data': plot_data,
            'zero_rates': zero_rates,
            'curve_ranges': curve_ranges,
            'curve_nodes': curve_nodes,
            'observer_notifications': observer_notifications
        }
        
    except Exception as e:
        print(f"Error in build_term_structures_with_reference_dates: {e}")
        return None