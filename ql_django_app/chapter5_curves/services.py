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

def build_term_structures_with_reference_dates(evaluation_date, market_data, day_count='Actual360'):
    """
    Build term structures with different reference dates - Following the original notebook exactly
    """
    try:
        print(f"Building term structures with evaluation_date: {evaluation_date}")
        print(f"Market data: {market_data}")
        print(f"Day count: {day_count}")
        
        # Get day count convention
        day_count_conv = get_day_count_convention(day_count)
        calendar_obj = ql.TARGET()
        
        # Set original evaluation date as in notebook In[2]
        original_eval_date = ql.Date(3, ql.October, 2014)
        ql.Settings.instance().evaluationDate = original_eval_date
        print(f"Set original evaluation date to: {original_eval_date}")
        
        # Build helpers exactly as in notebook In[3]
        helpers = []
        print(f"Building {len(market_data)} helpers...")
        for i, data in enumerate(market_data):
            tenor_years = data['tenor_years']
            rate = data['rate']
            if rate is None or rate == '':
                rate = 0.0
            rate = float(rate)
            
            print(f"Helper {i+1}: {tenor_years}Y at {rate}%")
            
            try:
                # Use SwapRateHelper exactly as in notebook
                helper = ql.SwapRateHelper(
                    ql.QuoteHandle(ql.SimpleQuote(rate/100.0)),
                    ql.Period(tenor_years, ql.Years),
                    ql.TARGET(),
                    ql.Annual,
                    ql.Unadjusted,
                    ql.Thirty360(ql.Thirty360.BondBasis),
                    ql.Euribor6M()
                )
                helpers.append(helper)
                print(f"Helper {i+1} created successfully")
            except Exception as e:
                print(f"Error creating helper {i+1}: {e}")
                raise
        
        # Build curve1 exactly as in notebook In[4]
        print("Building curve1 (PiecewiseFlatForward) with original date...")
        try:
            curve1_original = ql.PiecewiseFlatForward(0, ql.TARGET(), helpers, ql.Actual360())
            print(f"Curve1_original built successfully with {len(curve1_original.nodes())} nodes")
            
            # Get nodes for curve2 as in notebook In[5]
            dates, rates = zip(*curve1_original.nodes())
            print(f"Extracted {len(dates)} nodes from curve1_original")
            
            # Build curve2 exactly as in notebook In[7]
            print("Building curve2 (ForwardCurve) with fixed dates...")
            curve2 = ql.ForwardCurve(dates, rates, ql.Actual360())
            print(f"Curve2 built successfully with {len(dates)} nodes")
            
        except Exception as e:
            print(f"Error building curves: {e}")
            raise
        
        # Now set the actual evaluation date and rebuild curve1
        eval_date = ql.Date(evaluation_date.day, evaluation_date.month, evaluation_date.year)
        ql.Settings.instance().evaluationDate = eval_date
        print(f"Set actual evaluation date to: {eval_date}")
        
        # Rebuild curve1 with the new evaluation date
        print("Building curve1 (PiecewiseFlatForward) with actual date...")
        try:
            curve1 = ql.PiecewiseFlatForward(0, ql.TARGET(), helpers, ql.Actual360())
            print(f"Curve1 built successfully with {len(curve1.nodes())} nodes")
        except Exception as e:
            print(f"Error building curve1: {e}")
            raise
        
        # Generate plot data exactly as in notebook In[12]
        plot_data = {}
        times = np.linspace(0.0, 15.0, 400)
        print(f"Generating plot data for {len(times)} time points...")
        
        if curve1:
            print("Generating curve1 plot data...")
            curve1_rates = []
            for i, t in enumerate(times):
                try:
                    zero_rate = curve1.zeroRate(t, ql.Continuous)
                    rate_value = zero_rate.rate() * 100
                    curve1_rates.append(rate_value)
                    if i % 50 == 0:
                        print(f"Time {t}: rate = {rate_value:.4f}%")
                except Exception as e:
                    print(f"Error calculating zero rate at time {t}: {e}")
                    curve1_rates.append(0.0)
            plot_data['curve1'] = [{'x': float(t), 'y': float(rate)} for t, rate in zip(times, curve1_rates)]
            print(f"Generated {len(plot_data['curve1'])} plot points for curve1")
        else:
            print("No curve1 available for plotting")
        
        # Calculate zero rates exactly as in notebook In[9] and In[10]
        zero_rates = {}
        
        # 5Y rates as in notebook In[9]
        if curve1:
            try:
                zero_rate_5y = curve1.zeroRate(5.0, ql.Continuous)
                zero_rates['curve1_5y'] = zero_rate_5y.rate() * 100
                print(f"Curve1 5Y rate: {zero_rates['curve1_5y']:.6f}%")
            except Exception as e:
                print(f"Error calculating curve1 5Y rate: {e}")
                zero_rates['curve1_5y'] = 0.0
        
        if curve2:
            try:
                zero_rate_5y = curve2.zeroRate(5.0, ql.Continuous)
                zero_rates['curve2_5y'] = zero_rate_5y.rate() * 100
                print(f"Curve2 5Y rate: {zero_rates['curve2_5y']:.6f}%")
            except Exception as e:
                print(f"Error calculating curve2 5Y rate: {e}")
                zero_rates['curve2_5y'] = 0.0
        
        # Specific date rates as in notebook In[10]
        specific_date = ql.Date(7, ql.September, 2019)
        print(f"Calculating rates for specific date: {specific_date}")
        
        if curve1:
            try:
                zero_rate_date = curve1.zeroRate(specific_date, ql.Actual360(), ql.Continuous)
                zero_rates['curve1_date'] = zero_rate_date.rate() * 100
                print(f"Curve1 date rate: {zero_rates['curve1_date']:.6f}%")
            except Exception as e:
                print(f"Error calculating curve1 date rate: {e}")
                zero_rates['curve1_date'] = 0.0
        
        if curve2:
            try:
                zero_rate_date = curve2.zeroRate(specific_date, ql.Actual360(), ql.Continuous)
                zero_rates['curve2_date'] = zero_rate_date.rate() * 100
                print(f"Curve2 date rate: {zero_rates['curve2_date']:.6f}%")
            except Exception as e:
                print(f"Error calculating curve2 date rate: {e}")
                zero_rates['curve2_date'] = 0.0
        
        # Curve ranges as in notebook In[8] and In[14]
        curve_ranges = {}
        if curve1:
            curve_ranges['curve1'] = f"{curve1.referenceDate()} to {curve1.maxDate()}"
        if curve2:
            curve_ranges['curve2'] = f"{curve2.referenceDate()} to {curve2.maxDate()}"
        
        # Curve nodes
        curve_nodes = {}
        if curve1:
            nodes = curve1.nodes()
            curve_nodes['curve1'] = [(str(date_obj), float(rate)) for date_obj, rate in nodes]
        
        # Observer notifications as in notebook In[17] to In[23]
        observer_notifications = []
        
        # Create observers as in notebook In[17]
        def make_observer(i):
            def say():
                message = f"Observer {i} notified"
                observer_notifications.append(message)
                return message
            return ql.Observer(say)
        
        obs1 = make_observer(1)
        obs2 = make_observer(2)
        
        # Connect observers to curves as in notebook In[22]
        if curve1:
            obs1.registerWith(curve1)
            observer_notifications.append("Observer 1 connected to curve1 (relative date)")
        if curve2:
            obs2.registerWith(curve2)
            observer_notifications.append("Observer 2 connected to curve2 (fixed date)")
        
        # Test observers with quotes as in notebook In[18] to In[21]
        q1 = ql.SimpleQuote(1.0)
        obs1.registerWith(q1)
        q2 = ql.SimpleQuote(2.0)
        obs2.registerWith(q2)
        q3 = ql.SimpleQuote(3.0)
        obs1.registerWith(q3)
        obs2.registerWith(q3)
        
        # Trigger changes as in notebook In[19] to In[21]
        q1.setValue(1.5)
        q2.setValue(1.9)
        q3.setValue(3.1)
        
        # Check evaluation date change effect as in notebook In[13] and In[23]
        original_eval_date = ql.Date(3, ql.October, 2014)
        current_eval_date = ql.Date(evaluation_date.day, evaluation_date.month, evaluation_date.year)
        
        if current_eval_date != original_eval_date:
            observer_notifications.append(f"Evaluation date changed from {original_eval_date} to {current_eval_date}")
            observer_notifications.append("Curve1 (relative date) should be notified")
            observer_notifications.append("Curve2 (fixed date) should NOT be notified")
            
            # This should trigger notification from curve1 only
            # The notification happens automatically when the evaluation date changes
        else:
            observer_notifications.append("Evaluation date identical to original - no difference")
        
        # Day count convention effect
        day_count_effects = {
            'Actual360': "Actual/360: Standard day calculation",
            'Actual365': "Actual/365: Full year of 365 days", 
            'Thirty360': "30/360: 30-day month convention",
            'ActualActual': "Actual/Actual: Most precise calculation"
        }
        observer_notifications.append(f"Day count convention: {day_count_effects.get(day_count, day_count)}")
        
        result = {
            'plot_data': plot_data,
            'zero_rates': zero_rates,
            'curve_ranges': curve_ranges,
            'curve_nodes': curve_nodes,
            'observer_notifications': observer_notifications
        }
        
        print(f"Returning result with plot_data keys: {list(plot_data.keys())}")
        print(f"Zero rates: {zero_rates}")
        print(f"Curve ranges: {curve_ranges}")
        print(f"Observer notifications: {len(observer_notifications)} items")
        
        return result
        
    except Exception as e:
        print(f"Error in build_term_structures_with_reference_dates: {e}")
        return None