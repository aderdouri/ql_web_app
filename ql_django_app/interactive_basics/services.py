# interactive_basics/services.py

import QuantLib as ql
from datetime import date

# --- Mappings from form strings to QuantLib objects ---

WEEKDAY_MAP = {
    1: 'Sunday', 2: 'Monday', 3: 'Tuesday', 4: 'Wednesday',
    5: 'Thursday', 6: 'Friday', 7: 'Saturday'
}

CALENDAR_MAP = {
    'us': ql.UnitedStates(ql.UnitedStates.GovernmentBond),
    'italy': ql.Italy(),
}
TENOR_MAP = {
    'monthly': ql.Period(ql.Monthly),
    'quarterly': ql.Period(ql.Quarterly),
    'semiannual': ql.Period(ql.Semiannual),
    'annual': ql.Period(ql.Annual)
}
CONVENTION_MAP = {
    'following': ql.Following,
    'modified_following': ql.ModifiedFollowing,
    'preceding': ql.Preceding
}
DATE_GEN_MAP = {
    'forward': ql.DateGeneration.Forward,
    'backward': ql.DateGeneration.Backward
}
DAY_COUNT_MAP = {
    'actual_actual_isda': ql.ActualActual(ql.ActualActual.ISDA),
    'thirty_360': ql.Thirty360(ql.Thirty360.USA),
    'actual_360': ql.Actual360()
}
COMPOUND_MAP = {
    'compounded': ql.Compounded,
    'simple': ql.Simple,
    'continuous': ql.Continuous
}
FREQUENCY_MAP = {
    'annual': ql.Annual,
    'semiannual': ql.Semiannual,
    'quarterly': ql.Quarterly,
    'monthly': ql.Monthly
}


def to_ql_date(d: date) -> ql.Date:
    """Helper function to convert python date to QuantLib Date."""
    return ql.Date(d.day, d.month, d.year)


def process_date_module(day: int, month: int, year: int) -> dict:
    results = {}
    try:
        ql_date = ql.Date(day, month, year)
        results['created_date'] = str(ql_date)
        weekday_number = ql_date.weekday()
        results['properties'] = {
            'day': ql_date.dayOfMonth(),
            'month': ql_date.month(),
            'year': ql_date.year(),
            'weekday': WEEKDAY_MAP.get(weekday_number, 'Unknown')
        }
        results['arithmetic'] = {
            'add_day': str(ql_date + 1),
            'subtract_day': str(ql_date - 1),
            'add_week': str(ql_date + ql.Period(1, ql.Weeks)),
            'add_month': str(ql_date + ql.Period(1, ql.Months)),
            'add_year': str(ql_date + ql.Period(1, ql.Years)),
        }
    except Exception as e:
        results['error'] = f"Erreur QuantLib : {e}"
    return results


def process_calendar_module(start_date: date, period_days: int, calendar_choice: str) -> dict:
    results = {}
    try:
        ql_start_date = to_ql_date(start_date)
        period = ql.Period(period_days, ql.Days)
        
        if calendar_choice == 'joint':
            calendar = ql.JointCalendar(CALENDAR_MAP['us'], CALENDAR_MAP['italy'])
        else:
            calendar = CALENDAR_MAP.get(calendar_choice)
        
        if not calendar:
            raise ValueError("Calendrier non valide.")
            
        advanced_date = calendar.advance(ql_start_date, period)
        
        results = {
            'start_date': str(ql_start_date),
            'period': f"{period_days} jours",
            'raw_date': str(ql_start_date + period),
            'advanced_date': str(advanced_date),
            'calendar_used': calendar.name()
        }
    except Exception as e:
        results['error'] = f"Erreur QuantLib : {e}"
    return results


def process_schedule_module(data: dict) -> dict:
    results = {}
    try:
        effective_date = to_ql_date(data['schedule_effective_date'])
        termination_date = to_ql_date(data['schedule_termination_date'])
        tenor = TENOR_MAP[data['schedule_tenor']]
        
        # --- CORRECTION APPLIQUÉE ICI ---
        calendar_choice = data['schedule_calendar']
        if calendar_choice == 'joint':
            calendar = ql.JointCalendar(CALENDAR_MAP['us'], CALENDAR_MAP['italy'])
        else:
            calendar = CALENDAR_MAP.get(calendar_choice)
        
        if not calendar:
            raise ValueError(f"Calendrier non valide : {calendar_choice}")
        # --- FIN DE LA CORRECTION ---
        
        convention = CONVENTION_MAP[data['schedule_convention']]
        date_generation = DATE_GEN_MAP[data['schedule_date_generation']]
        end_of_month = data['schedule_end_of_month']
        
        schedule = ql.Schedule(
            effective_date,
            termination_date,
            tenor,
            calendar,
            convention,
            convention, # terminationDateConvention
            date_generation,
            end_of_month
        )
        
        results['dates'] = [str(dt) for dt in schedule]
        
    except Exception as e:
        results['error'] = f"Erreur QuantLib : {e}"
    return results


def process_interest_rate_module(data: dict) -> dict:
    results = {}
    try:
        rate = ql.InterestRate(
            data['ir_annual_rate'],
            DAY_COUNT_MAP[data['ir_day_count']],
            COMPOUND_MAP[data['ir_compound_type']],
            FREQUENCY_MAP[data['ir_frequency']]
        )
        
        t = data['ir_time_years']
        
        results['created_rate'] = str(rate)
        results['compound_factor'] = rate.compoundFactor(t)
        results['discount_factor'] = rate.discountFactor(t)
        
        # Equivalent Rate
        new_freq = FREQUENCY_MAP[data['ir_new_frequency']]
        new_rate = rate.equivalentRate(
            COMPOUND_MAP[data['ir_compound_type']],
            new_freq,
            t
        )
        results['equivalent_rate'] = str(new_rate)
        results['equivalent_discount_factor'] = new_rate.discountFactor(t)

    except Exception as e:
        results['error'] = f"Erreur QuantLib : {e}"
    return results