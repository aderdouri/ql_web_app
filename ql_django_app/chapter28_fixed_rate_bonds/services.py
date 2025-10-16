from datetime import datetime, date
import json

def calculate_bond_price_simple(form_data):
    """
    Calculate bond price using simple mathematical formulas (without QuantLib)
    """
    try:
        # Extract form data with defaults
        face_value = float(form_data.get('face_value', 100))
        coupon_rate = float(form_data.get('coupon_rate', 6)) / 100.0  # Convert percentage to decimal
        issue_date_str = form_data.get('issue_date', '2015-01-15')
        maturity_date_str = form_data.get('maturity_date', '2016-01-15')
        spot_rate_6m = float(form_data.get('spot_rate_6m', 0.5)) / 100.0
        spot_rate_1y = float(form_data.get('spot_rate_1y', 0.7)) / 100.0
        
        # Parse dates - handle both string and date objects
        if isinstance(issue_date_str, str):
            issue_date = datetime.strptime(issue_date_str, '%Y-%m-%d').date()
        else:
            issue_date = issue_date_str
            
        if isinstance(maturity_date_str, str):
            maturity_date = datetime.strptime(maturity_date_str, '%Y-%m-%d').date()
        else:
            maturity_date = maturity_date_str
        
        # Calculate time to maturity in years
        days_to_maturity = (maturity_date - issue_date).days
        years_to_maturity = days_to_maturity / 365.0
        
        # Calculate semi-annual coupon payment
        coupon_payment = face_value * coupon_rate / 2
        
        # Manual NPV calculation (as in the chapter example)
        # First coupon payment (6 months)
        pv_coupon_1 = coupon_payment / (1 + spot_rate_6m) ** 0.5
        
        # Final payment (principal + coupon at maturity)
        pv_final = (face_value + coupon_payment) / (1 + spot_rate_1y)
        
        # Total NPV
        npv = pv_coupon_1 + pv_final
        
        # Calculate bond yield (simplified)
        # Using the formula: Price = C/(1+y)^0.5 + (C+F)/(1+y)^1
        # Solving for y using approximation
        bond_yield = ((coupon_payment + face_value) / npv - 1) * 100
        
        # Calculate accrued interest (simplified - assume no accrual at issue)
        accrued_amount = 0.0
        
        # Clean and dirty prices are the same when no accrual
        clean_price = npv
        dirty_price = npv + accrued_amount
        
        # Schedule dates (simplified)
        from datetime import timedelta
        mid_date = issue_date + timedelta(days=(maturity_date - issue_date).days // 2)
        schedule_dates = [
            issue_date_str if isinstance(issue_date_str, str) else issue_date_str.strftime('%Y-%m-%d'),
            mid_date.strftime('%Y-%m-%d'),
            maturity_date_str if isinstance(maturity_date_str, str) else maturity_date_str.strftime('%Y-%m-%d')
        ]
        
        return {
            'success': True,
            'results': {
                'npv': round(npv, 6),
                'clean_price': round(clean_price, 6),
                'dirty_price': round(dirty_price, 6),
                'accrued_amount': round(accrued_amount, 6),
                'bond_yield': round(bond_yield, 4),
                'manual_npv': round(npv, 6),  # Same as NPV in this simple case
                'schedule_dates': schedule_dates,
                'coupon_payment': round(coupon_payment, 2),
                'face_value': round(face_value, 2),
                'spot_curve_dates': [issue_date_str if isinstance(issue_date_str, str) else issue_date_str.strftime('%Y-%m-%d'), 
                                   schedule_dates[1], 
                                   maturity_date_str if isinstance(maturity_date_str, str) else maturity_date_str.strftime('%Y-%m-%d')],
                'spot_curve_rates': [0.0, round(spot_rate_6m * 100, 3), round(spot_rate_1y * 100, 3)],
                'calculation_method': 'Simple Mathematical Formula'
            }
        }
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            'success': False,
            'error': f"Calculation error: {str(e)}",
            'details': error_details
        }

def calculate_bond_price_quantlib(form_data):
    """
    Calculate bond price using QuantLib (when available)
    """
    try:
        import QuantLib as ql
        
        # Extract form data with defaults
        face_value = float(form_data.get('face_value', 100))
        coupon_rate = float(form_data.get('coupon_rate', 6)) / 100.0
        issue_date_str = form_data.get('issue_date', '2015-01-15')
        maturity_date_str = form_data.get('maturity_date', '2016-01-15')
        spot_rate_6m = float(form_data.get('spot_rate_6m', 0.5)) / 100.0
        spot_rate_1y = float(form_data.get('spot_rate_1y', 0.7)) / 100.0
        settlement_days = int(form_data.get('settlement_days', 0))
        day_count_choice = form_data.get('day_count', 'Thirty360')
        calendar_choice = form_data.get('calendar', 'UnitedStates')
        
        # Parse dates - handle both string and date objects
        if isinstance(issue_date_str, str):
            issue_date = datetime.strptime(issue_date_str, '%Y-%m-%d').date()
        else:
            issue_date = issue_date_str
            
        if isinstance(maturity_date_str, str):
            maturity_date = datetime.strptime(maturity_date_str, '%Y-%m-%d').date()
        else:
            maturity_date = maturity_date_str
        
        # Convert to QuantLib dates
        ql_issue_date = ql.Date(issue_date.day, issue_date.month, issue_date.year)
        ql_maturity_date = ql.Date(maturity_date.day, maturity_date.month, maturity_date.year)
        
        # Set evaluation date
        ql.Settings.instance().evaluationDate = ql_issue_date
        
        # Create spot curve dates
        spot_dates = [
            ql_issue_date,
            ql_issue_date + ql.Period(6, ql.Months),
            ql_maturity_date
        ]
        spot_rates = [0.0, spot_rate_6m, spot_rate_1y]
        
        # Day count convention
        if day_count_choice == 'Thirty360':
            day_count = ql.Thirty360(ql.Thirty360.BondBasis)
        elif day_count_choice == 'Actual360':
            day_count = ql.Actual360()
        else:
            day_count = ql.Actual365Fixed()
        
        # Calendar
        if calendar_choice == 'UnitedStates':
            calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
        elif calendar_choice == 'UnitedKingdom':
            calendar = ql.UnitedKingdom()
        else:
            calendar = ql.TARGET()
        
        # Create yield curve
        spot_curve = ql.ZeroCurve(
            spot_dates, spot_rates, day_count, calendar,
            ql.Linear(), ql.Compounded, ql.Annual
        )
        spot_curve_handle = ql.YieldTermStructureHandle(spot_curve)
        
        # Create payment schedule
        schedule = ql.Schedule(
            ql_issue_date, ql_maturity_date, ql.Period(ql.Semiannual),
            calendar, ql.Unadjusted, ql.Unadjusted,
            ql.DateGeneration.Backward, False
        )
        
        # Create fixed rate bond
        fixed_rate_bond = ql.FixedRateBond(
            settlement_days, face_value, schedule,
            [coupon_rate], day_count
        )
        
        # Set pricing engine
        bond_engine = ql.DiscountingBondEngine(spot_curve_handle)
        fixed_rate_bond.setPricingEngine(bond_engine)
        
        # Calculate analytics
        npv = float(fixed_rate_bond.NPV())
        clean_price = float(fixed_rate_bond.cleanPrice())
        dirty_price = float(fixed_rate_bond.dirtyPrice())
        accrued_amount = float(fixed_rate_bond.accruedAmount())
        
        # Calculate bond yield
        bond_yield = float(fixed_rate_bond.bondYield(
            day_count, ql.Compounded, ql.Annual
        )) * 100
        
        # Get schedule dates and convert to ISO format
        schedule_dates = []
        for date in list(schedule):
            # Convert QuantLib date to ISO format
            if hasattr(date, 'day') and hasattr(date, 'month') and hasattr(date, 'year'):
                schedule_dates.append(f"{date.year()}-{date.month():02d}-{date.day():02d}")
            else:
                schedule_dates.append(str(date))
        
        # Manual calculation for comparison
        coupon_payment = face_value * coupon_rate / 2
        manual_npv = (
            coupon_payment / (1 + spot_rate_6m) ** 0.5 +
            (face_value + coupon_payment) / (1 + spot_rate_1y)
        )
        
        return {
            'success': True,
            'results': {
                'npv': round(npv, 6),
                'clean_price': round(clean_price, 6),
                'dirty_price': round(dirty_price, 6),
                'accrued_amount': round(accrued_amount, 6),
                'bond_yield': round(bond_yield, 4),
                'manual_npv': round(manual_npv, 6),
                'schedule_dates': schedule_dates,
                'coupon_payment': round(coupon_payment, 2),
                'face_value': round(face_value, 2),
                'spot_curve_dates': [str(d) for d in spot_dates],
                'spot_curve_rates': [round(r * 100, 3) for r in spot_rates],
                'calculation_method': 'QuantLib Framework'
            }
        }
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            'success': False,
            'error': f"QuantLib calculation error: {str(e)}",
            'details': error_details
        }

def calculate_bond_price(form_data):
    """
    Main function that uses simple calculation for reliability
    """
    # Use simple calculation for now to avoid QuantLib date formatting issues
    return calculate_bond_price_simple(form_data)

def calculate_price_sensitivity(form_data, parameter_changes):
    """
    Calculate price sensitivity to parameter changes
    """
    try:
        base_results = calculate_bond_price(form_data)
        if not base_results['success']:
            return base_results
            
        base_price = base_results['results']['npv']
        sensitivities = {}
        
        # Test coupon rate sensitivity
        if 'coupon_rate' in parameter_changes:
            test_data = form_data.copy()
            test_data['coupon_rate'] = float(test_data['coupon_rate']) + parameter_changes['coupon_rate']
            test_results = calculate_bond_price(test_data)
            if test_results['success']:
                sensitivities['coupon_rate'] = {
                    'change': parameter_changes['coupon_rate'],
                    'price_change': round(test_results['results']['npv'] - base_price, 6)
                }
        
        # Test spot rate sensitivity
        if 'spot_rate_6m' in parameter_changes:
            test_data = form_data.copy()
            test_data['spot_rate_6m'] = float(test_data['spot_rate_6m']) + parameter_changes['spot_rate_6m']
            test_results = calculate_bond_price(test_data)
            if test_results['success']:
                sensitivities['spot_rate_6m'] = {
                    'change': parameter_changes['spot_rate_6m'],
                    'price_change': round(test_results['results']['npv'] - base_price, 6)
                }
        
        if 'spot_rate_1y' in parameter_changes:
            test_data = form_data.copy()
            test_data['spot_rate_1y'] = float(test_data['spot_rate_1y']) + parameter_changes['spot_rate_1y']
            test_results = calculate_bond_price(test_data)
            if test_results['success']:
                sensitivities['spot_rate_1y'] = {
                    'change': parameter_changes['spot_rate_1y'],
                    'price_change': round(test_results['results']['npv'] - base_price, 6)
                }
        
        return {
            'success': True,
            'base_price': base_price,
            'sensitivities': sensitivities
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }