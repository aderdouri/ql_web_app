# Fichier : ql_web_app/interactive_basics/services.py
import QuantLib as ql

def create_date_from_form(day, month, year):
    """Crée un objet ql.Date et retourne ses propriétés de manière conviviale."""
    
    date = ql.Date(day, month, year)
    
    # =====================================================================
    # LA CORRECTION EST ICI
    # =====================================================================
    # On crée un dictionnaire de traduction pour les jours de la semaine
    weekday_map = {
        1: "Sunday",
        2: "Monday",
        3: "Tuesday",
        4: "Wednesday",
        5: "Thursday",
        6: "Friday",
        7: "Saturday"
    }
    
    # On récupère le numéro du jour...
    weekday_number = date.weekday()
    # ... et on le traduit en nom. On prévoit un cas par défaut si le numéro est inattendu.
    weekday_name = weekday_map.get(weekday_number, "Unknown")

    return {
        "date_str": str(date),
        "weekday": weekday_name  # <-- On renvoie maintenant le nom
    }

def add_period_from_form(start_date_str, quantity, unit_str):
    """Ajoute une période à une date."""
    day, month, year = map(int, start_date_str.split('-'))
    start_date = ql.Date(day, month, year)
    
    unit_map = {'Days': ql.Days, 'Weeks': ql.Weeks, 'Months': ql.Months, 'Years': ql.Years}
    period = ql.Period(quantity, unit_map[unit_str])
    
    end_date = start_date + period
    return {"end_date_str": str(end_date)}

def advance_with_calendar_from_form(start_date_str, period_days, calendar_str):
    """Avance une date en utilisant un calendrier de jours ouvrés."""
    day, month, year = map(int, start_date_str.split('-'))
    start_date = ql.Date(day, month, year)
    period = ql.Period(period_days, ql.Days)
    
    calendar_map = {
        'UnitedStates': ql.UnitedStates(ql.UnitedStates.GovernmentBond),
        'TARGET': ql.TARGET(),
        'UnitedKingdom': ql.UnitedKingdom()
    }
    calendar = calendar_map[calendar_str]
    
    end_date = calendar.advance(start_date, period)
    return {"end_date_str": str(end_date)}
