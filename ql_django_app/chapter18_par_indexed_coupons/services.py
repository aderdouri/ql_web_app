import QuantLib as ql
import pandas as pd
from datetime import datetime, date
from decimal import Decimal

def setup_market_data(evaluation_date):
    """Set up the market data and LIBOR curve as described in the book"""
    # Convert evaluation date to QuantLib Date
    if isinstance(evaluation_date, str):
        eval_date = datetime.strptime(evaluation_date, '%Y-%m-%d').date()
    else:
        eval_date = evaluation_date
    
    ql_date = ql.Date(eval_date.day, eval_date.month, eval_date.year)
    ql.Settings.instance().evaluationDate = ql_date
    
    # Forward rates from the book example - extended to support very long swaps (25+ years)
    dates_forwards = [
        (ql.Date(7, 1, 2013), 0.03613672438543303),
        (ql.Date(8, 4, 2013), 0.03613672438543303),
        (ql.Date(8, 7, 2013), 0.033849133719219514),
        (ql.Date(7, 1, 2014), 0.03573931373272106),
        (ql.Date(7, 7, 2014), 0.03445303757052511),
        (ql.Date(7, 1, 2015), 0.03500000000000000),
        (ql.Date(7, 7, 2015), 0.03450000000000000),
        (ql.Date(7, 1, 2016), 0.03520000000000000),
        (ql.Date(7, 7, 2016), 0.03480000000000000),
        (ql.Date(7, 1, 2017), 0.03550000000000000),
        (ql.Date(7, 7, 2017), 0.03500000000000000),
        (ql.Date(7, 1, 2018), 0.03600000000000000),
        (ql.Date(7, 7, 2018), 0.03550000000000000),
        (ql.Date(7, 1, 2019), 0.03620000000000000),
        (ql.Date(7, 7, 2019), 0.03570000000000000),
        (ql.Date(7, 1, 2020), 0.03650000000000000),
        (ql.Date(7, 7, 2020), 0.03600000000000000),
        (ql.Date(7, 1, 2021), 0.03700000000000000),
        (ql.Date(7, 7, 2021), 0.03650000000000000),
        (ql.Date(7, 1, 2022), 0.03750000000000000),
        (ql.Date(7, 7, 2022), 0.03700000000000000),
        (ql.Date(7, 1, 2023), 0.03800000000000000),
        (ql.Date(7, 7, 2023), 0.03750000000000000),
        (ql.Date(7, 1, 2024), 0.03850000000000000),
        (ql.Date(7, 7, 2024), 0.03800000000000000),
        (ql.Date(7, 1, 2025), 0.03900000000000000),
        (ql.Date(7, 7, 2025), 0.03850000000000000),
        (ql.Date(7, 1, 2026), 0.03950000000000000),
        (ql.Date(7, 7, 2026), 0.03900000000000000),
        (ql.Date(7, 1, 2027), 0.04000000000000000),
        (ql.Date(7, 7, 2027), 0.03950000000000000),
        (ql.Date(7, 1, 2028), 0.04050000000000000),
        (ql.Date(7, 7, 2028), 0.04000000000000000),
        (ql.Date(7, 1, 2029), 0.04100000000000000),
        (ql.Date(7, 7, 2029), 0.04050000000000000),
        (ql.Date(7, 1, 2030), 0.04150000000000000),
        (ql.Date(7, 7, 2030), 0.04100000000000000),
        (ql.Date(7, 1, 2031), 0.04200000000000000),
        (ql.Date(7, 7, 2031), 0.04150000000000000),
        (ql.Date(7, 1, 2032), 0.04250000000000000),
        (ql.Date(7, 7, 2032), 0.04200000000000000),
        (ql.Date(7, 1, 2033), 0.04300000000000000),
        (ql.Date(7, 7, 2033), 0.04250000000000000),
        (ql.Date(7, 1, 2034), 0.04350000000000000),
        (ql.Date(7, 7, 2034), 0.04300000000000000),
        (ql.Date(7, 1, 2035), 0.04400000000000000),
        (ql.Date(7, 7, 2035), 0.04350000000000000),
        (ql.Date(7, 1, 2036), 0.04450000000000000),
        (ql.Date(7, 7, 2036), 0.04400000000000000),
        (ql.Date(7, 1, 2037), 0.04500000000000000),
        (ql.Date(7, 7, 2037), 0.04450000000000000),
        (ql.Date(7, 1, 2038), 0.04550000000000000),
        (ql.Date(7, 7, 2038), 0.04500000000000000),
        (ql.Date(7, 1, 2039), 0.04600000000000000),
        (ql.Date(7, 7, 2039), 0.04550000000000000),
        (ql.Date(7, 1, 2040), 0.04650000000000000),
        (ql.Date(7, 7, 2040), 0.04600000000000000)
    ]
    
    dates, forwards = zip(*dates_forwards)
    libor_curve = ql.ForwardCurve(dates, forwards, ql.Actual365Fixed())
    
    return ql_date, libor_curve

def create_swap_legs(notional, swap_length, evaluation_date):
    """Create the floating leg of the swap as described in the book"""
    ql_date, libor_curve = setup_market_data(evaluation_date)
    
    # Create GBP LIBOR 6-month index
    index = ql.GBPLibor(ql.Period(6, ql.Months), ql.YieldTermStructureHandle(libor_curve))
    calendar = index.fixingCalendar()
    adjustment = index.businessDayConvention()
    
    # Calculate maturity date - ensure we have a proper period
    if swap_length < 1.0:
        # For periods less than 1 year, use months
        months = int(swap_length * 12)
        maturity = calendar.advance(ql_date, ql.Period(months, ql.Months))
    else:
        # For periods 1 year or more, use years
        years = int(swap_length)
        months = int((swap_length - years) * 12)
        if months > 0:
            maturity = calendar.advance(ql_date, ql.Period(years, ql.Years) + ql.Period(months, ql.Months))
        else:
            maturity = calendar.advance(ql_date, ql.Period(years, ql.Years))
    
    # Create schedule
    schedule = ql.Schedule(
        ql_date, maturity,
        index.tenor(), calendar,
        adjustment, adjustment,
        ql.DateGeneration.Backward, False
    )
    
    # Create floating leg
    floating_leg = ql.IborLeg([notional], schedule, index, index.dayCounter())
    
    return floating_leg, index, libor_curve, schedule

def analyze_par_coupons(floating_leg, index, notional):
    """Analyze par coupons - rate calculated over coupon period"""
    coupon_data = []
    total_amount = 0
    
    for i, coupon in enumerate(floating_leg):
        coupon_obj = ql.as_floating_rate_coupon(coupon)
        
        # Par coupon calculation: rate over coupon period
        coupon_start = coupon_obj.accrualStartDate()
        coupon_end = coupon_obj.accrualEndDate()
        accrual_period = coupon_obj.accrualPeriod()
        
        # Get the rate and amount
        rate = coupon_obj.rate()
        amount = coupon_obj.amount()
        
        # Calculate days between dates
        coupon_days = coupon_end - coupon_start
        
        coupon_data.append({
            'coupon_number': i + 1,
            'fixing_date': str(coupon_obj.fixingDate()),
            'start_date': str(coupon_start),
            'end_date': str(coupon_end),
            'coupon_days': coupon_days,
            'accrual_period': accrual_period,
            'rate': rate,
            'amount': amount,
            'method': 'par_coupon'
        })
        
        total_amount += amount
    
    return coupon_data, total_amount

def analyze_indexed_coupons(floating_leg, index, libor_curve, notional):
    """Analyze indexed coupons - rate calculated over LIBOR tenor"""
    coupon_data = []
    total_amount = 0
    
    for i, coupon in enumerate(floating_leg):
        coupon_obj = ql.as_floating_rate_coupon(coupon)
        
        # Indexed coupon calculation: rate over LIBOR tenor
        fixing_date = coupon_obj.fixingDate()
        start_date = index.valueDate(fixing_date)
        end_date = index.maturityDate(start_date)
        
        # Get the index fixing (rate over LIBOR tenor)
        index_fixing = index.fixing(fixing_date)
        
        # Calculate amount using coupon accrual period but index rate
        accrual_period = coupon_obj.accrualPeriod()
        amount = index_fixing * notional * accrual_period
        
        # Calculate days between dates
        libor_days = end_date - start_date
        coupon_start = coupon_obj.accrualStartDate()
        coupon_end = coupon_obj.accrualEndDate()
        coupon_days = coupon_end - coupon_start
        
        coupon_data.append({
            'coupon_number': i + 1,
            'fixing_date': str(fixing_date),
            'libor_start_date': str(start_date),
            'libor_end_date': str(end_date),
            'libor_days': libor_days,
            'coupon_start_date': str(coupon_start),
            'coupon_end_date': str(coupon_end),
            'coupon_days': coupon_days,
            'accrual_period': accrual_period,
            'rate': index_fixing,
            'amount': amount,
            'method': 'indexed_coupon'
        })
        
        total_amount += amount
    
    return coupon_data, total_amount

def compare_coupon_methods(par_data, indexed_data):
    """Compare the two coupon calculation methods"""
    comparison = []
    max_rate_diff = 0
    total_diff = 0
    
    for i in range(len(par_data)):
        par_coupon = par_data[i]
        indexed_coupon = indexed_data[i]
        
        rate_diff = abs(par_coupon['rate'] - indexed_coupon['rate'])
        amount_diff = par_coupon['amount'] - indexed_coupon['amount']
        
        max_rate_diff = max(max_rate_diff, rate_diff)
        total_diff += amount_diff
        
        comparison.append({
            'coupon_number': i + 1,
            'par_rate': par_coupon['rate'],
            'indexed_rate': indexed_coupon['rate'],
            'rate_difference': rate_diff,
            'par_amount': par_coupon['amount'],
            'indexed_amount': indexed_coupon['amount'],
            'amount_difference': amount_diff,
            'percentage_diff': (rate_diff / indexed_coupon['rate']) * 100 if indexed_coupon['rate'] != 0 else 0,
            'par_coupon_days': par_coupon['coupon_days'],
            'indexed_libor_days': indexed_coupon['libor_days'],
            'indexed_coupon_days': indexed_coupon['coupon_days'],
            'days_difference': par_coupon['coupon_days'] - indexed_coupon['libor_days']
        })
    
    return comparison, max_rate_diff, total_diff

def analyze_swap_coupons(notional, swap_length, evaluation_date, use_par=True, use_indexed=True):
    """Main analysis function"""
    try:
        # Create swap legs
        floating_leg, index, libor_curve, schedule = create_swap_legs(notional, swap_length, evaluation_date)
        
        results = {
            'success': True,
            'swap_info': {
                'notional': notional,
                'swap_length': swap_length,
                'evaluation_date': str(evaluation_date),
                'num_coupons': len(floating_leg)
            }
        }
        
        # Analyze par coupons
        if use_par:
            par_data, par_total = analyze_par_coupons(floating_leg, index, notional)
            results['par_coupons'] = {
                'data': par_data,
                'total_amount': par_total
            }
        
        # Analyze indexed coupons
        if use_indexed:
            indexed_data, indexed_total = analyze_indexed_coupons(floating_leg, index, libor_curve, notional)
            results['indexed_coupons'] = {
                'data': indexed_data,
                'total_amount': indexed_total
            }
        
        # Compare methods if both are used
        if use_par and use_indexed:
            comparison, max_rate_diff, total_diff = compare_coupon_methods(par_data, indexed_data)
            results['comparison'] = {
                'data': comparison,
                'max_rate_difference': max_rate_diff,
                'total_amount_difference': total_diff,
                'par_total': par_total,
                'indexed_total': indexed_total
            }
        
        return results
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def get_analysis_descriptions():
    """Get descriptions for different analysis types"""
    return {
        'par_coupons': {
            'title': 'Par Coupons Analysis',
            'description': 'Analyzes coupon calculations using the par coupon method, where the floating rate is calculated over the duration of the coupon period.',
            'key_points': [
                'Rate calculated over coupon accrual period',
                'Common in textbook examples',
                'May introduce small errors due to period mismatch',
                'Swap value jumps when coupon rate is fixed'
            ]
        },
        'indexed_coupons': {
            'title': 'Indexed Coupons Analysis',
            'description': 'Analyzes coupon calculations using the indexed coupon method, where the rate is calculated over the LIBOR tenor period.',
            'key_points': [
                'Rate calculated over LIBOR tenor period',
                'More theoretically correct',
                'Requires convexity adjustment for period mismatch',
                'Consistent with market fixing methodology'
            ]
        },
        'comparison': {
            'title': 'Comparison Analysis',
            'description': 'Compares both par and indexed coupon methods to highlight the differences and their implications.',
            'key_points': [
                'Shows rate and amount differences',
                'Highlights theoretical vs practical approaches',
                'Demonstrates impact on swap valuation',
                'Helps understand QuantLib configuration options'
            ]
        }
    }
