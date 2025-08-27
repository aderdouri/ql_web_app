# File: ql_web_app/interactive_basics/services.py
import QuantLib as ql

def create_ql_date(params: dict):
    try:
        d = ql.Date(params['day'], params['month'], params['year'])
        return {'status': 'success', 'result': f"Success! QuantLib created the date: {d.ISO()}", 'raw_date': d.to_date().isoformat()}
    except Exception as e:
        return {'status': 'error', 'result': f"QuantLib Error: {e}"}

def add_ql_period(params: dict):
    try:
        start_date = ql.Date(params['start_date'].day, params['start_date'].month, params['start_date'].year)
        unit_map = {'Days': ql.Days, 'Weeks': ql.Weeks, 'Months': ql.Months, 'Years': ql.Years}
        period = ql.Period(params['quantity'], unit_map[params['unit']])
        result_date = start_date + period
        return {'status': 'success', 'result': result_date.ISO()}
    except Exception as e:
        return {'status': 'error', 'result': f"Error: {e}"}

def calculate_calendar_dates(params: dict):
    start_date = params['start_date_cal']
    d = ql.Date(start_date.day, start_date.month, start_date.year)
    p = ql.Period(params['period_days'], ql.Days)
    
    # Correction: Ajout de TARGET au dictionnaire
    cal_map = {
        'UnitedStates': ql.UnitedStates(ql.UnitedStates.GovernmentBond),
        'Italy': ql.Italy(),
        'TARGET': ql.TARGET()
    }
    calendar = cal_map.get(params['calendar'])
    
    return {
        'status': 'success',
        'raw_date': (d + p).ISO(),
        'adjusted_date': calendar.advance(d, p).ISO(),
    }

def create_schedule(params: dict):
    eff_date = ql.Date(params['effective_date'].day, params['effective_date'].month, params['effective_date'].year)
    term_date = ql.Date(params['termination_date'].day, params['termination_date'].month, params['termination_date'].year)
    tenor = ql.Period(params['tenor'])
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond) if params['calendar_sched'] == 'UnitedStates' else ql.TARGET()
    schedule = ql.Schedule(eff_date, term_date, tenor, calendar, ql.Unadjusted, ql.Unadjusted, ql.DateGeneration.Forward, False)
    return {'status': 'success', 'result': [d.ISO() for d in schedule]}

def create_interest_rate(params: dict):
    try:
        rate = params['rate'] / 100.0
        dc_map = {
            'ActualActual': ql.ActualActual(ql.ActualActual.ISDA),
            'Thirty360': ql.Thirty360(ql.Thirty360.BondBasis)
        }
        day_count = dc_map.get(params['day_counter'])
        comp_map = {'Compounded': ql.Compounded, 'Simple': ql.Simple}
        compounding = comp_map.get(params['compounding'])
        freq_map = {'Annual': ql.Annual, 'Semiannual': ql.Semiannual}
        frequency = freq_map.get(params['frequency'])
        
        interest_rate = ql.InterestRate(rate, day_count, compounding, frequency)
        
        return {
            'status': 'success',
            'result': {
                'rate': f"{interest_rate.rate() * 100:.6f}%",
                'day_counter': day_count.name(),
                'compounding': str(compounding),
                'frequency': str(frequency),
                'compound_factor_1y': f"{interest_rate.compoundFactor(1.0):.6f}"
            }
        }
    except Exception as e:
        return {'status': 'error', 'result': str(e)}